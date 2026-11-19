"""Load transformed CheckIt.AI records into a relational SQLite database."""

import argparse
import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


LOGGER = logging.getLogger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
    source_name TEXT PRIMARY KEY,
    source_category TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS content_records (
    publication_id TEXT PRIMARY KEY,
    source_name TEXT NOT NULL,
    title TEXT,
    text_content TEXT,
    published_at TEXT,
    collected_at TEXT,
    language TEXT,
    article_url TEXT,
    has_text INTEGER NOT NULL DEFAULT 0,
    transformation_status TEXT,
    source_metadata TEXT,
    FOREIGN KEY (source_name) REFERENCES sources(source_name)
);

CREATE TABLE IF NOT EXISTS image_assets (
    publication_id TEXT PRIMARY KEY,
    image_url TEXT,
    image_path TEXT,
    image_valid INTEGER,
    image_status TEXT,
    FOREIGN KEY (publication_id)
        REFERENCES content_records(publication_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS label_assessments (
    publication_id TEXT PRIMARY KEY,
    label_value TEXT,
    label_type TEXT,
    label_source TEXT,
    label_status TEXT,
    fact_check_url TEXT,
    source_labels TEXT,
    FOREIGN KEY (publication_id)
        REFERENCES content_records(publication_id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_content_source
ON content_records(source_name);

CREATE INDEX IF NOT EXISTS idx_content_published_at
ON content_records(published_at);

CREATE INDEX IF NOT EXISTS idx_labels_type
ON label_assessments(label_type);
"""


def load_config(config_path: str) -> dict[str, Any]:
    """Load and validate the project YAML configuration."""
    path = Path(config_path)

    if not path.is_file():
        raise FileNotFoundError(f"Configuration introuvable : {path}")

    with path.open(encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("La configuration YAML doit être un dictionnaire.")

    for section in ("paths", "transformation"):
        if section not in config:
            raise ValueError(f"Section manquante : {section}")

    if not config["transformation"].get("input_files"):
        raise ValueError("Aucun fichier transformé configuré.")

    return config


def json_value(value: Any) -> str | None:
    """Serialize a value as JSON for SQLite storage."""
    if value is None:
        return None
    return json.dumps(value, ensure_ascii=False, default=str)


def boolean_value(value: Any) -> int | None:
    """Convert a nullable Python boolean to SQLite integer."""
    if value is None:
        return None
    return int(bool(value))


def upsert_record(
    connection: sqlite3.Connection,
    record: dict[str, Any],
    source_key: str,
) -> None:
    """Insert or update one publication and its related records."""
    publication_id = record.get("publication_id")
    source_name = record.get("source_name") or source_key

    if not publication_id:
        raise ValueError("Enregistrement sans publication_id.")

    connection.execute(
        """
        INSERT INTO sources (source_name, source_category, description)
        VALUES (?, ?, ?)
        ON CONFLICT(source_name) DO UPDATE SET
            source_category = COALESCE(
                excluded.source_category, sources.source_category
            )
        """,
        (
            source_name,
            record.get("source_category"),
            f"Source de données : {source_name}",
        ),
    )

    connection.execute(
        """
        INSERT INTO content_records (
            publication_id, source_name, title, text_content,
            published_at, collected_at, language, article_url,
            has_text, transformation_status, source_metadata
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(publication_id) DO UPDATE SET
            source_name = excluded.source_name,
            title = excluded.title,
            text_content = excluded.text_content,
            published_at = excluded.published_at,
            collected_at = excluded.collected_at,
            language = excluded.language,
            article_url = excluded.article_url,
            has_text = excluded.has_text,
            transformation_status = excluded.transformation_status,
            source_metadata = excluded.source_metadata
        """,
        (
            publication_id,
            source_name,
            record.get("title"),
            record.get("text_content"),
            record.get("published_at"),
            record.get("collected_at"),
            record.get("language"),
            record.get("article_url"),
            int(bool(record.get("has_text"))),
            record.get("transformation_status"),
            json_value(record.get("source_metadata")),
        ),
    )

    connection.execute(
        """
        INSERT INTO image_assets (
            publication_id, image_url, image_path, image_valid, image_status
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(publication_id) DO UPDATE SET
            image_url = excluded.image_url,
            image_path = excluded.image_path,
            image_valid = excluded.image_valid,
            image_status = excluded.image_status
        """,
        (
            publication_id,
            record.get("image_url"),
            record.get("image_path"),
            boolean_value(record.get("image_valid")),
            record.get("image_status"),
        ),
    )

    connection.execute(
        """
        INSERT INTO label_assessments (
            publication_id, label_value, label_type, label_source,
            label_status, fact_check_url, source_labels
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(publication_id) DO UPDATE SET
            label_value = excluded.label_value,
            label_type = excluded.label_type,
            label_source = excluded.label_source,
            label_status = excluded.label_status,
            fact_check_url = excluded.fact_check_url,
            source_labels = excluded.source_labels
        """,
        (
            publication_id,
            str(record["label"]) if record.get("label") is not None else None,
            record.get("label_type"),
            record.get("label_source"),
            record.get("label_status"),
            record.get("fact_check_url"),
            json_value(record.get("source_labels")),
        ),
    )


def run_loader(config: dict[str, Any]) -> dict[str, Any]:
    """Load all configured transformed JSONL files into SQLite."""
    processed_dir = Path(config["paths"]["processed"])
    database_path = processed_dir / "checkitai.db"
    database_path.parent.mkdir(parents=True, exist_ok=True)

    results: dict[str, int] = {}
    total_records = 0

    connection = sqlite3.connect(database_path)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA)

        with connection:
            for source, relative_path in (
                config["transformation"]["input_files"].items()
            ):
                input_path = (
                    processed_dir / source / f"{source}_transformed.jsonl"
                )

                if not input_path.is_file():
                    raise FileNotFoundError(
                        f"Fichier transformé introuvable : {input_path}"
                    )

                source_count = 0

                with input_path.open(encoding="utf-8") as input_file:
                    for line_number, line in enumerate(input_file, start=1):
                        if not line.strip():
                            continue

                        try:
                            record = json.loads(line)
                        except json.JSONDecodeError as error:
                            raise ValueError(
                                f"JSON invalide dans {input_path}, "
                                f"ligne {line_number}."
                            ) from error

                        if not isinstance(record, dict):
                            raise ValueError(
                                f"Enregistrement invalide dans "
                                f"{input_path}, ligne {line_number}."
                            )

                        upsert_record(connection, record, source)
                        source_count += 1

                results[source] = source_count
                total_records += source_count
                LOGGER.info(
                    "%s : %d enregistrements chargés.",
                    source,
                    source_count,
                )

    finally:
        connection.close()

    database_path.chmod(0o600)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "database": str(database_path),
        "total_records_loaded": total_records,
        "sources": results,
    }

    LOGGER.info(
        "Chargement terminé : %d enregistrements dans %s",
        total_records,
        database_path,
    )

    return report


def main() -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description="Chargement SQLite des données CheckIt.AI"
    )
    parser.add_argument(
        "--config",
        default="config/settings.yaml",
        help="Chemin vers le fichier de configuration YAML.",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    config = load_config(args.config)
    report = run_loader(config)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
