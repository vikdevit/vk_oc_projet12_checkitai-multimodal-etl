"""Airflow DAG orchestrating the CheckIt.AI ETL pipeline."""

import logging
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


LOGGER = logging.getLogger(__name__)

PROJECT_ROOT = Path(
    "/mnt/projects/vk_oc_projet12_checkitai-multimodal-etl"
)
PROJECT_PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"
CONFIG_PATH = "config/settings.yaml"


def run_project_module(
    module: str,
    extra_args: list[str] | None = None,
) -> None:
    """Execute an existing CheckIt.AI Python module."""
    if not PROJECT_PYTHON.is_file():
        raise FileNotFoundError(
            f"Environnement Python du projet introuvable : {PROJECT_PYTHON}"
        )

    command = [
        str(PROJECT_PYTHON),
        "-m",
        module,
        "--config",
        CONFIG_PATH,
    ]

    if extra_args:
        command.extend(extra_args)

    LOGGER.info("Exécution de la commande : %s", " ".join(command))

    subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=True,
        text=True,
    )

    LOGGER.info("Module terminé avec succès : %s", module)


default_args = {
    "owner": "checkitai",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id="checkitai_etl_pipeline",
    description="Extraction, transformation et chargement des données CheckIt.AI",
    default_args=default_args,
    start_date=datetime(2026, 11, 19, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    tags=["checkitai", "etl", "multimodal"],
) as dag:

    extract_fakeddit = PythonOperator(
        task_id="extract_fakeddit",
        python_callable=run_project_module,
        op_kwargs={
            "module": "checkitai.extraction.fakeddit",
            "extra_args": ["--max-records", "100"],
        },
    )

    extract_fakenewsnet = PythonOperator(
        task_id="extract_fakenewsnet",
        python_callable=run_project_module,
        op_kwargs={
            "module": "checkitai.extraction.fakenewsnet",
            "extra_args": ["--max-records", "10"],
        },
    )

    extract_newsdata = PythonOperator(
        task_id="extract_newsdata",
        python_callable=run_project_module,
        op_kwargs={
            "module": "checkitai.extraction.newsdata",
            "extra_args": ["--max-records", "10"],
        },
    )

    extract_cimple = PythonOperator(
        task_id="extract_cimple",
        python_callable=run_project_module,
        op_kwargs={
            "module": "checkitai.extraction.cimple",
        },
    )

    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=run_project_module,
        op_kwargs={
            "module": "checkitai.transformation.pipeline",
        },
    )

    load_data = PythonOperator(
        task_id="load_data",
        python_callable=run_project_module,
        op_kwargs={
            "module": "checkitai.storage.sqlite_loader",
        },
    )

    [
        extract_fakeddit,
        extract_fakenewsnet,
        extract_newsdata,
        extract_cimple,
    ] >> transform_data >> load_data
