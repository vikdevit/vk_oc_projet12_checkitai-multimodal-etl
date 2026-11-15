"""
Connecteur d'extraction pour le dataset Fakeddit.

Ce module lit les données brutes TSV, normalise les publications
et prépare leur sauvegarde au format JSONL.
"""

from __future__ import annotations

import argparse
import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from checkitai.extraction.common.image_validator import download_image

LOGGER = logging.getLogger("checkitai.extraction.fakeddit")


def load_config(config_path: Path) -> dict[str, Any]:
    """Charge et vérifie la configuration YAML du projet."""
    with config_path.open("r", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    if not isinstance(config, dict):
        raise TypeError("La configuration YAML est invalide.")

    required_sections = {"paths", "logging", "extraction", "sources"}
    missing = required_sections - config.keys()

    if missing:
        raise ValueError(
            f"Sections manquantes dans la configuration : {sorted(missing)}"
        )

    if "fakeddit" not in config["sources"]:
        raise ValueError("La configuration de la source Fakeddit est absente.")

    return config


def setup_logging(config: dict[str, Any]) -> None:
    """Configure les journaux dans un fichier et dans le terminal."""
    log_config = config["logging"]
    log_directory = Path(log_config["directory"])
    log_directory.mkdir(parents=True, exist_ok=True)

    log_file = log_directory / "fakeddit_extraction.log"

    logging.basicConfig(
        level=getattr(logging, log_config.get("level", "INFO").upper()),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )


def read_fakeddit(
    input_file: Path,
    chunk_size: int,
    max_records: int | None = None,
):
    """Lit le fichier TSV Fakeddit progressivement, par lots."""
    if not input_file.is_file():
        raise FileNotFoundError(
            f"Fichier source introuvable : {input_file}"
        )

    if chunk_size <= 0:
        raise ValueError("La taille des lots doit être supérieure à zéro.")

    if max_records is not None and max_records <= 0:
        raise ValueError("La limite de publications doit être positive.")

    LOGGER.info("Début de lecture du fichier : %s", input_file)

    records_read = 0

    for chunk in pd.read_csv(
        input_file,
        sep="\t",
        chunksize=chunk_size,
        dtype={"id": "string", "image_url": "string"},
    ):
        if max_records is not None:
            remaining = max_records - records_read
            if remaining <= 0:
                break
            chunk = chunk.head(remaining)

        records_read += len(chunk)
        LOGGER.info("%s publications lues", records_read)

        yield chunk

        if max_records is not None and records_read >= max_records:
            break

    LOGGER.info("Lecture terminée : %s publications", records_read)


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    """Normalise une publication Fakeddit sans perdre ses données sources."""

    def clean_value(value: Any) -> Any:
        """Convertit les valeurs pandas manquantes en None."""
        if pd.isna(value):
            return None
        return value

    created_utc = clean_value(record.get("created_utc"))
    published_at = None

    if created_utc is not None:
        published_at = datetime.fromtimestamp(
            float(created_utc),
            tz=UTC,
        ).isoformat()

    binary_label = clean_value(record.get("2_way_label"))
    label_mapping = {
        0: "fake",
        1: "true",
    }

    return {
        "publication_id": clean_value(record.get("id")),
        "source_name": "Fakeddit",
        "title": clean_value(record.get("title")),
        "text_content": clean_value(record.get("clean_title")),
        "image_url": clean_value(record.get("image_url")),
        "image_path": None,
        "published_at": published_at,
        "collected_at": datetime.now(UTC).isoformat(),
        "language": None,
        "label": label_mapping.get(binary_label),
        "label_source": "Fakeddit - distant supervision",
        "label_status": (
            "available" if binary_label is not None else "missing"
        ),
        "source_labels": {
            "2_way_label": binary_label,
            "3_way_label": clean_value(record.get("3_way_label")),
            "6_way_label": clean_value(record.get("6_way_label")),
        },
        "source_metadata": {
            "author": clean_value(record.get("author")),
            "domain": clean_value(record.get("domain")),
            "subreddit": clean_value(record.get("subreddit")),
            "score": clean_value(record.get("score")),
            "num_comments": clean_value(record.get("num_comments")),
            "upvote_ratio": clean_value(record.get("upvote_ratio")),
            "hasImage": clean_value(record.get("hasImage")),
            "linked_submission_id": clean_value(
                record.get("linked_submission_id")
            ),
        },
        "image_valid": None,
        "extraction_status": "metadata_extracted",
    }


def save_records(
    records,
    output_file: Path,
) -> int:
    """Enregistre les publications normalisées au format JSONL."""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    records_saved = 0

    with output_file.open("w", encoding="utf-8") as jsonl_file:
        for record in records:
            jsonl_file.write(
                json.dumps(record, ensure_ascii=False, allow_nan=False)
                + "\n"
            )
            records_saved += 1

    LOGGER.info(
        "%s publications enregistrées dans %s",
        records_saved,
        output_file,
    )

    return records_saved


def generate_report(
    report_data: dict[str, Any],
    report_file: Path,
) -> Path:
    """Génère un rapport JSON décrivant une extraction Fakeddit."""
    report_file.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "source_name": "Fakeddit",
        **report_data,
    }

    with report_file.open("w", encoding="utf-8") as json_file:
        json.dump(
            report,
            json_file,
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        )

    LOGGER.info("Rapport d'extraction enregistré : %s", report_file)

    return report_file


def calculate_statistics(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Calcule les indicateurs de qualité des publications extraites."""
    total_records = len(records)

    label_counts = {"fake": 0, "true": 0, "missing": 0}

    missing_titles = 0
    missing_image_urls = 0
    missing_labels = 0

    for record in records:
        if not record.get("title"):
            missing_titles += 1

        if not record.get("image_url"):
            missing_image_urls += 1

        label = record.get("label")

        if label not in {"fake", "true"}:
            missing_labels += 1
            label_counts["missing"] += 1
        else:
            label_counts[label] += 1

    return {
        "total_records": total_records,
        "missing_titles": missing_titles,
        "missing_image_urls": missing_image_urls,
        "missing_labels": missing_labels,
        "label_distribution": label_counts,
    }


def iter_normalized_records(
    input_file: Path,
    chunk_size: int,
    max_records: int | None = None,
):
    """Produit les publications normalisées progressivement."""
    for chunk in read_fakeddit(
        input_file=input_file,
        chunk_size=chunk_size,
        max_records=max_records,
    ):
        for _, row in chunk.iterrows():
            yield normalize_record(row.to_dict())


def parse_arguments() -> argparse.Namespace:
    """Définit et récupère les arguments de lancement du connecteur."""
    parser = argparse.ArgumentParser(
        description="Extraction automatisée des données Fakeddit."
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/settings.yaml"),
        help="Chemin vers le fichier de configuration YAML.",
    )

    extraction_group = parser.add_mutually_exclusive_group()

    extraction_group.add_argument(
        "--max-records",
        type=int,
        default=None,
        help="Nombre maximal de publications à extraire.",
    )

    extraction_group.add_argument(
        "--all",
        action="store_true",
        help="Extraire toutes les publications du fichier source.",
    )

    parser.add_argument(
        "--download-images",
        action="store_true",
        help="Télécharger les images associées aux publications.",
    )

    args = parser.parse_args()

    if args.max_records is not None and args.max_records <= 0:
        parser.error("--max-records doit être supérieur à zéro.")

    return args


def main() -> int:
    """Orchestre l'extraction complète des données Fakeddit."""
    args = parse_arguments()

    try:
        config = load_config(args.config)
        setup_logging(config)

        source_config = config["sources"]["fakeddit"]

        input_file = (
            Path(config["paths"]["raw"])
            / source_config["input_file"]
        )

        output_file = (
            Path(config["paths"]["interim"])
            / "fakeddit"
            / "fakeddit_publications.jsonl"
        )

        report_file = (
            Path(config["paths"]["reports"])
            / "fakeddit"
            / "fakeddit_extraction_report.json"
        )

        if args.all:
            max_records = None
        elif args.max_records is not None:
            max_records = args.max_records
        else:
            max_records = source_config.get("max_records")

        chunk_size = int(source_config["chunk_size"])

        statistics = {
            "total_records": 0,
            "missing_titles": 0,
            "missing_image_urls": 0,
            "missing_labels": 0,
            "label_distribution": {
                "fake": 0,
                "true": 0,
                "missing": 0,
            },
            "image_downloads_attempted": 0,
            "image_downloads_succeeded": 0,
            "image_downloads_failed": 0,
            "image_downloads_skipped_limit": 0,
        }

        def tracked_records():
            """Normalise les publications et télécharge les images si demandé."""
            image_limit = int(
                config["extraction"].get("image_download_batch_size", 5)
            )
            images_directory = Path(config["paths"]["images"]) / "fakeddit"

            for record in iter_normalized_records(
                input_file=input_file,
                chunk_size=chunk_size,
                max_records=max_records,
            ):
                statistics["total_records"] += 1

                if not record.get("title"):
                    statistics["missing_titles"] += 1

                if not record.get("image_url"):
                    statistics["missing_image_urls"] += 1

                label = record.get("label")
                if label not in {"fake", "true"}:
                    statistics["missing_labels"] += 1
                    statistics["label_distribution"]["missing"] += 1
                else:
                    statistics["label_distribution"][label] += 1

                if args.download_images:
                    if not record.get("image_url"):
                        record["image_download_status"] = "missing_url"
                    elif statistics["image_downloads_attempted"] < image_limit:
                        result = download_image(
                            url=record["image_url"],
                            output_dir=images_directory,
                            publication_id=record["publication_id"],
                            config=config["extraction"],
                        )
                        statistics["image_downloads_attempted"] += 1
                        record.update({
                            "image_valid": result["image_valid"],
                            "image_path": result["image_path"],
                            "image_content_type": result.get("image_content_type"),
                            "image_size_bytes": result.get("image_size_bytes"),
                            "image_download_status": result["download_status"],
                            "image_download_error": result["download_error"],
                            "image_download_attempts": result["download_attempts"],
                        })
                        if result["image_valid"]:
                            statistics["image_downloads_succeeded"] += 1
                        else:
                            statistics["image_downloads_failed"] += 1
                    else:
                        statistics["image_downloads_skipped_limit"] += 1
                        record["image_download_status"] = (
                            "not_attempted_limit_reached"
                        )
                else:
                    record["image_download_status"] = "disabled"

                yield record

        LOGGER.info("Démarrage de l'extraction Fakeddit.")

        records_saved = save_records(
            tracked_records(),
            output_file,
        )

        report_data = {
            "source_file": str(input_file),
            "output_file": str(output_file),
            "records_saved": records_saved,
            "chunk_size": chunk_size,
            "max_records": max_records,
            "statistics": statistics,
        }

        generate_report(report_data, report_file)

        LOGGER.info("Extraction Fakeddit terminée avec succès.")
        LOGGER.info("Rapport disponible : %s", report_file)

        print("\nExtraction terminée.")
        print("Publications enregistrées :", records_saved)
        print("Fichier JSONL :", output_file)
        print("Rapport JSON :", report_file)
        print("Statistiques :", statistics)

        return 0

    except Exception:
        LOGGER.exception("Échec de l'extraction Fakeddit.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
