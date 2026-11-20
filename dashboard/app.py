"""Tableau de bord KPI du pipeline ETL CheckIt.AI."""

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = Path("/mnt/data/vk_oc_projet12_checkitai-multimodal-etl")
DB_PATH = DATA_ROOT / "processed" / "checkitai.db"

AIRFLOW_DB_PATH = Path(
    "/mnt/projects/envs/airflow_home/airflow.db"
)


@st.cache_data(ttl=60)
def load_airflow_data():
    """Charge l'historique des exécutions et des tâches Airflow."""
    if not AIRFLOW_DB_PATH.exists():
        return pd.DataFrame(), pd.DataFrame()

    uri = f"file:{AIRFLOW_DB_PATH}?mode=ro"

    with sqlite3.connect(uri, uri=True) as connection:
        runs = pd.read_sql_query(
            """
            SELECT run_id, state, start_date, end_date
            FROM dag_run
            WHERE dag_id = 'checkitai_etl_pipeline'
            ORDER BY start_date DESC
            """,
            connection,
        )

        tasks = pd.read_sql_query(
            """
            SELECT run_id, task_id, state, duration, start_date, end_date
            FROM task_instance
            WHERE dag_id = 'checkitai_etl_pipeline'
            ORDER BY start_date DESC
            """,
            connection,
        )

    return runs, tasks

st.set_page_config(
    page_title="CheckIt.AI — Performance ETL",
    page_icon="📊",
    layout="wide",
)

st.title("📊 CheckIt.AI — Tableau de bord ETL")
st.caption("Suivi de la qualité, des volumes et du stockage des données.")

if not DB_PATH.exists():
    st.error(f"Base SQLite introuvable : {DB_PATH}")
    st.stop()


@st.cache_data(ttl=60)
def load_data():
    """Charge les indicateurs depuis la base SQLite."""
    with sqlite3.connect(DB_PATH) as connection:
        sources = pd.read_sql_query(
            """
            SELECT source_name, COUNT(*) AS total
            FROM content_records
            GROUP BY source_name
            ORDER BY total DESC
            """,
            connection,
        )

        images = pd.read_sql_query(
            """
            SELECT image_status, COUNT(*) AS total
            FROM image_assets
            GROUP BY image_status
            """,
            connection,
        )

        quality = pd.read_sql_query(
            """
            SELECT
                COUNT(*) AS total,
                SUM(has_text) AS with_text
            FROM content_records
            """,
            connection,
        ).iloc[0]

        image_quality = pd.read_sql_query(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN image_path IS NOT NULL
                         AND image_valid = 1 THEN 1 ELSE 0 END)
                    AS downloaded,
                SUM(CASE WHEN image_url IS NOT NULL
                         AND image_url != '' THEN 1 ELSE 0 END)
                    AS with_url
            FROM image_assets
            """,
            connection,
        ).iloc[0]

    return sources, images, quality, image_quality


sources, images, quality, image_quality = load_data()

total_records = int(quality["total"])
records_with_text = int(quality["with_text"] or 0)
images_with_url = int(image_quality["with_url"] or 0)
images_downloaded = int(image_quality["downloaded"] or 0)

text_rate = (
    records_with_text / total_records * 100 if total_records else 0
)
url_rate = (
    images_with_url / total_records * 100 if total_records else 0
)
download_rate = (
    images_downloaded / total_records * 100 if total_records else 0
)
db_size_mb = DB_PATH.stat().st_size / (1024 * 1024)

st.subheader("Vue d'ensemble")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Publications en base", f"{total_records:,}".replace(",", " "))
col2.metric("Textes disponibles", f"{text_rate:.1f}%")
col3.metric("Images avec URL", f"{url_rate:.1f}%")
col4.metric("Images téléchargées", f"{download_rate:.1f}%")

st.divider()

st.subheader("Qualité des données")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Répartition des publications par source**")
    fig_sources = px.bar(
        sources,
        x="source_name",
        y="total",
        labels={
            "source_name": "Source",
            "total": "Nombre de publications",
        },
        text="total",
    )
    fig_sources.update_layout(xaxis_title=None, yaxis_title="Publications")
    st.plotly_chart(fig_sources, use_container_width=True)

with col2:
    st.markdown("**Disponibilité des images**")
    fig_images = px.pie(
        images,
        names="image_status",
        values="total",
        hole=0.45,
        labels={
            "image_status": "Statut de l'image",
            "total": "Nombre de publications",
        },
    )
    st.plotly_chart(fig_images, use_container_width=True)

st.info(
    "Une URL d'image disponible ne signifie pas que l'image a été "
    "téléchargée ou validée. Ces indicateurs sont présentés séparément."
)

st.subheader("Stockage")

col1, col2 = st.columns(2)
col1.metric("Taille de la base SQLite", f"{db_size_mb:.2f} Mo")
col2.metric(
    "Publications sans texte",
    f"{total_records - records_with_text:,}".replace(",", " "),
)

with st.expander("Détail des volumes par source"):
    st.dataframe(sources, use_container_width=True, hide_index=True)

st.caption("Source des indicateurs : base SQLite CheckIt.AI.")
st.caption("Actualisation automatique des données toutes les 60 secondes.")

st.divider()
st.subheader("Performance du pipeline Airflow")

runs, tasks = load_airflow_data()

if runs.empty:
    st.warning("Aucune exécution Airflow disponible.")
else:
    runs["start_date"] = pd.to_datetime(runs["start_date"])
    runs["end_date"] = pd.to_datetime(runs["end_date"])
    runs["duration_seconds"] = (
        runs["end_date"] - runs["start_date"]
    ).dt.total_seconds()

    total_runs = len(runs)
    successful_runs = int((runs["state"] == "success").sum())
    failed_runs = int((runs["state"] == "failed").sum())
    success_rate = successful_runs / total_runs * 100

    latest_run = runs.iloc[0]
    latest_duration = latest_run["duration_seconds"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Exécutions", total_runs)
    col2.metric("Taux de réussite", f"{success_rate:.1f}%")
    col3.metric("Échecs", failed_runs)
    col4.metric(
        "Dernière exécution",
        f"{latest_duration:.2f} s"
        if pd.notna(latest_duration)
        else "Non disponible",
    )

    if failed_runs:
        st.error("Au moins une exécution du pipeline a échoué.")
    else:
        st.success("Aucun échec enregistré dans l'historique disponible.")

    st.markdown("**Durée des exécutions du DAG**")
    history = runs.dropna(subset=["duration_seconds"]).copy()
    history["execution"] = history["start_date"].dt.strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    if not history.empty:
        fig_runs = px.bar(
            history.sort_values("start_date"),
            x="execution",
            y="duration_seconds",
            color="state",
            labels={
                "execution": "Date d'exécution",
                "duration_seconds": "Durée (secondes)",
                "state": "État",
            },
            text_auto=".2f",
        )
        st.plotly_chart(fig_runs, width="stretch")

    st.markdown("**Durée des tâches — dernière exécution**")
    latest_run_id = latest_run["run_id"]
    latest_tasks = tasks[tasks["run_id"] == latest_run_id].copy()

    if not latest_tasks.empty:
        latest_tasks["duration"] = pd.to_numeric(
            latest_tasks["duration"], errors="coerce"
        )
        latest_tasks = latest_tasks.dropna(subset=["duration"])

        fig_tasks = px.bar(
            latest_tasks.sort_values("duration", ascending=True),
            x="duration",
            y="task_id",
            orientation="h",
            color="state",
            labels={
                "duration": "Durée (secondes)",
                "task_id": "Tâche",
                "state": "État",
            },
            text_auto=".3f",
        )
        st.plotly_chart(fig_tasks, width="stretch")
    else:
        st.info("Aucune durée de tâche disponible pour cette exécution.")

    with st.expander("Historique détaillé des exécutions"):
        st.dataframe(
            runs[["run_id", "state", "start_date", "end_date", "duration_seconds"]],
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "Mesures issues de l'historique réel Airflow. "
        "Le nombre d'exécutions disponibles reste limité."
    )
