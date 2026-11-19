"""Transformation pipeline for CheckIt.AI extracted publications."""

import argparse
import json
import logging
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


LOGGER = logging.getLogger("checkitai.transformation")


def load_config(config_path: str) -> dict[str, Any]:
    """Load and validate the project configuration."""
    path = Path(config_path)

    if not path.is_file():
        raise FileNotFoundError(f"Configuration introuvable : {path}")

    with path.open(encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("La configuration YAML doit être un dictionnaire.")

    for section in ("paths", "logging", "transformation"):
        if section not in config:
            raise ValueError(f"Section manquante dans la configuration : {section}")

    if not config["transformation"].get("input_files"):
        raise ValueError("Aucun fichier d'entrée configuré.")

    return config


def setup_logging(config: dict[str, Any]) -> None:
    """Configure console and file logging."""
    log_dir = Path(config["logging"]["directory"])
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "transformation.log"
    level = getattr(logging, config["logging"].get("level", "INFO").upper())

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )


def clean_text(value: Any) -> Any:
    """Normalize whitespace without changing the meaning of text."""
    if not isinstance(value, str):
        return value

    value = value.replace("\u00a0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalize_date(value: Any) -> Any:
    """Convert recognized dates to ISO 8601; preserve unrecognized values."""
    if not isinstance(value, str) or not value.strip():
        return value

    candidate = value.strip()

    try:
        parsed = datetime.fromisoformat(candidate.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = datetime.strptime(candidate, "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            return value

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed.isoformat()


def determine_image_status(record: dict[str, Any]) -> tuple[bool, str]:
    """Determine image availability from the local file, not from its URL."""
    image_path = record.get("image_path")

    if not image_path:
        return False, "url_only" if record.get("image_url") else "missing"

    path = Path(image_path)

    if not path.is_absolute():
        data_root = Path(
            "/mnt/data/vk_oc_projet12_checkitai-multimodal-etl"
        )
        path = data_root / path

    if not path.is_file():
        return False, "invalid"

    if record.get("image_valid") is False:
        return False, "invalid"

    return True, "downloaded"


def determine_label_type(record: dict[str, Any]) -> str:
    """Classify the nature of the label without changing its value."""
    label = record.get("label")

    if label is None or label == "":
        return "unlabeled"

    source = str(record.get("source_name", "")).lower()
    if "cimple" in source:
        return "fact_check"

    if record.get("label_status") == "fact_checked":
        return "fact_check"

    return "binary"


def transform_record(
    original: dict[str, Any],
    clean_text_enabled: bool = True,
    normalize_dates_enabled: bool = True,
) -> dict[str, Any]:
    """Transform one record while preserving its original fields."""
    record = dict(original)

    if clean_text_enabled:
        record["title"] = clean_text(record.get("title"))
        record["text_content"] = clean_text(record.get("text_content"))

    if normalize_dates_enabled:
        record["published_at"] = normalize_date(record.get("published_at"))
        record["collected_at"] = normalize_date(record.get("collected_at"))

    has_text = bool(
        (record.get("title") and record["title"].strip())
        or (record.get("text_content") and record["text_content"].strip())
    )

    has_image, image_status = determine_image_status(record)

    record["has_text"] = has_text
    record["has_image"] = has_image
    record["image_status"] = image_status
    record["label_type"] = determine_label_type(record)
    record["transformation_status"] = "success"

    return record


def transform_source(
    source: str,
    input_path: Path,
    output_path: Path,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Transform a JSONL source and write its output incrementally."""
    if not input_path.is_file():
        raise FileNotFoundError(f"Fichier source introuvable : {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    settings = config["transformation"]
    clean_enabled = settings.get("clean_text", True)
    dates_enabled = settings.get("normalize_dates", True)

    stats: Counter[str] = Counter()
    label_counts: Counter[str] = Counter()
    image_counts: Counter[str] = Counter()

    LOGGER.info("Début transformation : %s", source)
    LOGGER.info("Lecture : %s", input_path)

    with input_path.open(encoding="utf-8") as source_file, output_path.open(
        "w", encoding="utf-8"
    ) as output_file:
        for line_number, line in enumerate(source_file, start=1):
            if not line.strip():
                continue

            try:
                original = json.loads(line)
                if not isinstance(original, dict):
                    raise ValueError("L'enregistrement JSON n'est pas un objet.")

                record = transform_record(
                    original,
                    clean_text_enabled=clean_enabled,
                    normalize_dates_enabled=dates_enabled,
                )

                output_file.write(
                    json.dumps(record, ensure_ascii=False, default=str) + "\n"
                )

                stats["records_transformed"] += 1
                stats["records_with_text"] += int(record["has_text"])
                stats["records_with_image"] += int(record["has_image"])
                stats["records_without_text"] += int(not record["has_text"])

                label_counts[str(record.get("label"))] += 1
                image_counts[record["image_status"]] += 1

            except (json.JSONDecodeError, ValueError, TypeError) as error:
                stats["records_rejected"] += 1
                LOGGER.warning(
                    "Enregistrement ignoré (%s, ligne %d) : %s",
                    source,
                    line_number,
                    error,
                )

    LOGGER.info(
        "%s : %d transformés, %d rejetés",
        source,
        stats["records_transformed"],
        stats["records_rejected"],
    )

    return {
        "source": source,
        "input_file": str(input_path),
        "output_file": str(output_path),
        "statistics": dict(stats),
        "labels": dict(label_counts),
        "images": dict(image_counts),
    }


def run_pipeline(config: dict[str, Any]) -> dict[str, Any]:
    """Transform all configured sources and generate a global report."""
    interim_dir = Path(config["paths"]["interim"])
    processed_dir = Path(config["paths"]["processed"])

    results = []

    for source, relative_path in config["transformation"]["input_files"].items():
        input_path = interim_dir / relative_path
        output_path = processed_dir / source / f"{source}_transformed.jsonl"

        result = transform_source(
            source,
            input_path,
            output_path,
            config,
        )
        results.append(result)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_records_transformed": sum(
            item["statistics"].get("records_transformed", 0)
            for item in results
        ),
        "total_records_rejected": sum(
            item["statistics"].get("records_rejected", 0)
            for item in results
        ),
        "sources": results,
    }

    report_dir = Path(config["paths"]["reports"]) / "transformation"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / "transformation_report.json"
    with report_path.open("w", encoding="utf-8") as report_file:
        json.dump(report, report_file, ensure_ascii=False, indent=2)

    LOGGER.info("Rapport global enregistré : %s", report_path)
    LOGGER.info(
        "Pipeline terminé : %d enregistrements transformés.",
        report["total_records_transformed"],
    )

    return report


def main() -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description="Pipeline de transformation CheckIt.AI"
    )
    parser.add_argument(
        "--config",
        default="config/settings.yaml",
        help="Chemin vers le fichier de configuration YAML.",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    setup_logging(config)
    run_pipeline(config)


if __name__ == "__main__":
    main()
