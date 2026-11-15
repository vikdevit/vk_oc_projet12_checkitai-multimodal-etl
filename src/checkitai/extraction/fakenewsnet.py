"""Connecteur d'extraction des métadonnées FakeNewsNet."""

import argparse
import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pandas as pd
import yaml

LOGGER = logging.getLogger("checkitai.extraction.fakenewsnet")


def load_config(config_path: str) -> dict[str, Any]:
    """Charge la configuration YAML."""
    with Path(config_path).open(encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("Configuration YAML invalide.")

    return config


def setup_logging(config: dict[str, Any]) -> None:
    """Configure les logs."""
    log_dir = Path(config["logging"]["directory"])
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=config["logging"].get("level", "INFO"),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(
                log_dir / "fakenewsnet_extraction.log",
                encoding="utf-8",
            ),
            logging.StreamHandler(),
        ],
        force=True,
    )


def normalize_url(value: Any) -> str | None:
    """Normalise une URL sans inventer de domaine."""
    if pd.isna(value) or not str(value).strip():
        return None

    url = str(value).strip()

    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    parsed = urlparse(url)

    if not parsed.hostname:
        return None

    return url


def normalize_record(
    row: dict[str, Any],
    source_file: str,
) -> dict[str, Any]:
    """Convertit une ligne CSV au format commun du projet."""
    label = "fake" if "_fake" in source_file else "true"

    title = row.get("title")
    news_url = normalize_url(row.get("news_url"))

    return {
        "publication_id": str(row.get("id", "")),
        "source_name": "FakeNewsNet",
        "source_category": source_file.split("_")[0],
        "title": str(title).strip() if pd.notna(title) else None,
        "text_content": None,
        "article_url": news_url,
        "image_url": None,
        "image_path": None,
        "published_at": None,
        "collected_at": datetime.now(UTC).isoformat(),
        "language": None,
        "label": label,
        "label_source": "FakeNewsNet - nom du fichier source",
        "label_status": "source_label",
        "source_labels": {"file": source_file},
        "source_metadata": {
            "tweet_ids": (
                str(row["tweet_ids"])
                if pd.notna(row.get("tweet_ids"))
                else None
            )
        },
        "image_valid": None,
        "extraction_status": "metadata_extracted",
    }


def extract_file(
    input_file: Path,
    output_file,
    chunk_size: int,
    max_records: int | None,
) -> dict[str, int]:
    """Extrait un CSV par lots et écrit les enregistrements JSONL."""
    label_counts = {"fake": 0, "true": 0}
    total = 0
    missing_titles = 0
    missing_urls = 0

    for chunk in pd.read_csv(
        input_file,
        chunksize=chunk_size,
        dtype=str,
        keep_default_na=True,
    ):
        for row in chunk.to_dict(orient="records"):
            if max_records is not None and total >= max_records:
                return {
                    "records": total,
                    "missing_titles": missing_titles,
                    "missing_urls": missing_urls,
                    "fake": label_counts["fake"],
                    "true": label_counts["true"],
                }

            record = normalize_record(row, input_file.name)

            if not record["title"]:
                missing_titles += 1

            if not record["article_url"]:
                missing_urls += 1

            label_counts[record["label"]] += 1

            output_file.write(
                json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n"
            )
            total += 1

    return {
        "records": total,
        "missing_titles": missing_titles,
        "missing_urls": missing_urls,
        "fake": label_counts["fake"],
        "true": label_counts["true"],
    }


def main() -> int:
    """Orchestre l'extraction FakeNewsNet."""
    parser = argparse.ArgumentParser(
        description="Extraction automatisée des données FakeNewsNet."
    )
    parser.add_argument(
        "--config",
        default="config/settings.yaml",
        help="Chemin du fichier de configuration.",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=None,
        help="Limite de publications par fichier CSV.",
    )
    args = parser.parse_args()

    if args.max_records is not None and args.max_records <= 0:
        parser.error("--max-records doit être supérieur à zéro.")

    try:
        config = load_config(args.config)
        setup_logging(config)

        input_dir = Path(config["paths"]["raw"]) / "fakenewsnet"
        output_file = (
            Path(config["paths"]["interim"])
            / "fakenewsnet"
            / "fakenewsnet_publications.jsonl"
        )
        report_file = (
            Path(config["paths"]["reports"])
            / "fakenewsnet"
            / "fakenewsnet_extraction_report.json"
        )

        csv_files = sorted(input_dir.glob("*.csv"))

        if not csv_files:
            raise FileNotFoundError(
                f"Aucun CSV FakeNewsNet dans {input_dir}"
            )

        output_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.parent.mkdir(parents=True, exist_ok=True)

        chunk_size = int(
            config["sources"].get("fakenewsnet", {}).get("chunk_size", 1000)
        )

        total_stats = {
            "records": 0,
            "missing_titles": 0,
            "missing_urls": 0,
            "fake": 0,
            "true": 0,
            "files": {},
        }

        LOGGER.info("Démarrage de l'extraction FakeNewsNet.")

        with output_file.open("w", encoding="utf-8") as output:
            for csv_file in csv_files:
                LOGGER.info("Lecture du fichier : %s", csv_file.name)

                stats = extract_file(
                    csv_file,
                    output,
                    chunk_size,
                    args.max_records,
                )

                total_stats["files"][csv_file.name] = stats

                for key in (
                    "records",
                    "missing_titles",
                    "missing_urls",
                    "fake",
                    "true",
                ):
                    total_stats[key] += stats[key]

        report = {
            "source_name": "FakeNewsNet",
            "generated_at": datetime.now(UTC).isoformat(),
            "output_file": str(output_file),
            "statistics": total_stats,
        }

        report_file.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        LOGGER.info(
            "Extraction terminée : %s publications.",
            total_stats["records"],
        )
        print("Publications extraites :", total_stats["records"])
        print("JSONL :", output_file)
        print("Rapport :", report_file)
        print("Statistiques :", total_stats)

        return 0

    except Exception:
        LOGGER.exception("Échec de l'extraction FakeNewsNet.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
