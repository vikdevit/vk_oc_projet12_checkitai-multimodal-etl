"""Extraction d'actualités depuis l'API NewsData.io."""

import argparse
import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import yaml
from dotenv import load_dotenv

API_URL = "https://newsdata.io/api/1/latest"


def load_config(config_path: str) -> dict[str, Any]:
    """Charge et vérifie la configuration YAML."""
    path = Path(config_path)
    if not path.is_file():
        raise FileNotFoundError(f"Configuration introuvable : {path}")

    with path.open(encoding="utf-8") as file:
        config = yaml.safe_load(file)

    for section in ("paths", "logging", "extraction", "sources"):
        if section not in config:
            raise ValueError(f"Section absente de la configuration : {section}")

    if "newsdata" not in config["sources"]:
        raise ValueError("Configuration sources.newsdata absente")

    return config


def setup_logging(config: dict[str, Any]) -> None:
    """Configure les journaux de collecte."""
    log_dir = Path(config["logging"]["directory"])
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config["logging"].get("level", "INFO").upper()),
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "newsdata_extraction.log"),
            logging.StreamHandler(),
        ],
        force=True,
    )


def fetch_articles(
    api_key: str,
    params: dict[str, Any],
    timeout: int,
    max_retries: int,
) -> list[dict[str, Any]]:
    """Interroge l'API NewsData.io avec quelques tentatives en cas d'erreur."""
    request_params = {"apikey": api_key, **params}

    for attempt in range(max_retries):
        try:
            response = requests.get(
                API_URL,
                params=request_params,
                timeout=timeout,
            )

            if response.status_code in (429, 500, 502, 503, 504):
                logging.warning(
                    "Erreur temporaire HTTP %s (tentative %s/%s)",
                    response.status_code,
                    attempt + 1,
                    max_retries,
                )
                if attempt + 1 < max_retries:
                    time.sleep(2 ** attempt)
                    continue

            response.raise_for_status()
            data = response.json()

            if data.get("status") != "success":
                error = data.get("results", {})
                if isinstance(error, dict):
                    error_code = error.get("code", "erreur API")
                else:
                    error_code = "erreur API"
                raise RuntimeError(f"NewsData.io : {error_code}")

            return data.get("results", [])

        except requests.RequestException as exc:
            logging.error("Erreur réseau : %s", type(exc).__name__)
            if attempt + 1 == max_retries:
                raise RuntimeError("Échec de la requête NewsData.io") from exc
            time.sleep(2 ** attempt)

    raise RuntimeError("Nombre maximal de tentatives atteint")


def normalize_article(article: dict[str, Any]) -> dict[str, Any]:
    """Convertit un article API dans le format commun du projet."""
    collected_at = datetime.now(timezone.utc).isoformat()

    return {
        "publication_id": article.get("article_id"),
        "source_name": "NewsData.io",
        "title": article.get("title"),
        "text_content": article.get("content") or article.get("description"),
        "article_url": article.get("link"),
        "image_url": article.get("image_url"),
        "image_path": None,
        "published_at": article.get("pubDate"),
        "collected_at": collected_at,
        "language": article.get("language"),
        "label": None,
        "label_source": None,
        "label_status": "unlabeled",
        "source_labels": {},
        "source_metadata": {
            "publisher": article.get("source_name"),
            "source_id": article.get("source_id"),
            "country": article.get("country"),
            "category": article.get("category"),
            "keywords": article.get("keywords"),
            "creator": article.get("creator"),
            "source_priority": article.get("source_priority"),
            "datatype": article.get("datatype"),
            "sentiment": article.get("sentiment"),
        },
        "image_valid": None,
        "extraction_status": "metadata_extracted",
    }


def save_jsonl(records: list[dict[str, Any]], output_file: Path) -> None:
    """Enregistre les articles au format JSON Lines."""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def generate_report(
    records: list[dict[str, Any]],
    report_file: Path,
) -> None:
    """Génère un bilan simple de la collecte."""
    report_file.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "source": "NewsData.io",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "total_records": len(records),
        "missing_titles": sum(not r["title"] for r in records),
        "missing_article_urls": sum(not r["article_url"] for r in records),
        "missing_image_urls": sum(not r["image_url"] for r in records),
        "unlabeled_records": len(records),
    }

    with report_file.open("w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extraction d'actualités depuis NewsData.io"
    )
    parser.add_argument("--config", default="config/settings.yaml")
    parser.add_argument("--max-records", type=int, default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    setup_logging(config)
    load_dotenv()

    api_key = os.getenv("NEWSDATA_API_KEY")
    if not api_key:
        raise RuntimeError("Variable NEWSDATA_API_KEY absente du fichier .env")

    source_config = config["sources"]["newsdata"]
    max_records = args.max_records or source_config.get("max_records", 10)

    if max_records <= 0:
        raise ValueError("--max-records doit être supérieur à zéro")

    params = {
        "language": source_config.get("language"),
        "country": source_config.get("country"),
        "category": source_config.get("category"),
    }

    if source_config.get("query"):
        params["q"] = source_config["query"]

    params = {key: value for key, value in params.items() if value is not None}

    logging.info("Démarrage de la collecte NewsData.io")
    articles = fetch_articles(
        api_key=api_key,
        params=params,
        timeout=config["extraction"].get("request_timeout", 30),
        max_retries=config["extraction"].get("max_retries", 3),
    )

    records = [
        normalize_article(article)
        for article in articles[:max_records]
    ]

    data_root = Path(config["paths"]["data_root"])
    output_file = data_root / "interim/newsdata/newsdata_publications.jsonl"
    report_file = data_root / "reports/newsdata/newsdata_extraction_report.json"

    save_jsonl(records, output_file)
    generate_report(records, report_file)

    logging.info("Articles extraits : %s", len(records))
    logging.info("Articles sans titre : %s", sum(not r["title"] for r in records))
    logging.info("Articles sans image : %s", sum(not r["image_url"] for r in records))
    logging.info("Fichier JSONL : %s", output_file)
    logging.info("Rapport : %s", report_file)


if __name__ == "__main__":
    main()
