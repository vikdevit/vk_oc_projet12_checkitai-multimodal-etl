
import argparse
import gzip
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from rdflib import Graph, Namespace, RDF, URIRef

SCHEMA = Namespace("http://schema.org/")
CIMPLE = Namespace("http://data.cimple.eu/ontology#")

LOGGER = logging.getLogger(__name__)

KNOWN_VERDICTS = {
    "not_credible",
    "credible",
    "uncertain",
    "not_verifiable",
    "mostly_credible",
}


def load_config(config_path: Path) -> dict[str, Any]:
    with config_path.open(encoding="utf-8") as file:
        config = yaml.safe_load(file)

    required = {"paths", "logging", "sources"}
    missing = required - config.keys()
    if missing:
        raise ValueError(f"Sections manquantes dans la configuration : {missing}")

    if "cimple" not in config["sources"]:
        raise ValueError("Configuration sources.cimple absente")

    return config


def setup_logging(config: dict[str, Any]) -> None:
    log_dir = Path(config["paths"]["data_root"]) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config["logging"].get("level", "INFO").upper()),
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(
                log_dir / "cimple_extraction.log",
                encoding="utf-8",
            ),
            logging.StreamHandler(),
        ],
        force=True,
    )


def get_literal(graph: Graph, subject: Any, predicate: Any) -> str | None:
    value = graph.value(subject, predicate)
    return str(value) if value is not None else None


def get_uri(graph: Graph, subject: Any, predicate: Any) -> str | None:
    value = graph.value(subject, predicate)
    return str(value) if isinstance(value, URIRef) else None


def get_verdict(graph: Graph, review_uri: URIRef) -> tuple[str | None, dict]:
    normalized_uri = get_uri(graph, review_uri, CIMPLE.normalizedReviewRating)
    rating_uri = get_uri(graph, review_uri, SCHEMA.reviewRating)

    verdict = None
    if normalized_uri:
        candidate = normalized_uri.rstrip("/").split("/")[-1]
        if candidate in KNOWN_VERDICTS:
            verdict = candidate

    rating_value = None
    rating_name = None
    rating_same_as = None

    if rating_uri:
        rating_node = URIRef(rating_uri)
        rating_value = get_literal(graph, rating_node, SCHEMA.ratingValue)
        rating_name = get_literal(graph, rating_node, SCHEMA.name)
        rating_same_as = get_uri(graph, rating_node, SCHEMA.sameAs)

        if verdict is None and rating_same_as:
            candidate = rating_same_as.rstrip("/").split("/")[-1]
            if candidate in KNOWN_VERDICTS:
                verdict = candidate

    metadata = {
        "rating_uri": rating_uri,
        "normalized_rating_uri": normalized_uri,
        "rating_value": rating_value,
        "rating_name": rating_name,
        "rating_same_as": rating_same_as,
    }
    return verdict, metadata


def normalize_review(graph: Graph, review_uri: URIRef) -> dict[str, Any]:
    claim_uri = get_uri(graph, review_uri, SCHEMA.itemReviewed)
    claim_text = None

    if claim_uri:
        claim_text = get_literal(graph, URIRef(claim_uri), SCHEMA.text)

    fact_check_url = get_literal(graph, review_uri, SCHEMA.url)
    review_text = get_literal(graph, review_uri, SCHEMA.text)
    published_at = get_literal(graph, review_uri, SCHEMA.datePublished)
    language = get_literal(graph, review_uri, SCHEMA.inLanguage)

    author_uri = get_uri(graph, review_uri, SCHEMA.author)
    author_name = None
    if author_uri:
        author_name = get_literal(graph, URIRef(author_uri), SCHEMA.name)

    verdict, rating_metadata = get_verdict(graph, review_uri)

    return {
        "publication_id": str(review_uri),
        "source_name": "CIMPLE",
        "title": claim_text,
        "text_content": claim_text,
        "article_url": None,
        "fact_check_url": fact_check_url,
        "image_url": None,
        "image_path": None,
        "published_at": published_at,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "language": language,
        "label": verdict,
        "label_source": "CIMPLE ClaimReview Knowledge Graph",
        "label_status": "fact_checked" if verdict else "unlabeled",
        "source_labels": {
            "normalized_verdict": verdict,
            **rating_metadata,
        },
        "source_metadata": {
            "claim_uri": claim_uri,
            "review_uri": str(review_uri),
            "review_text": review_text,
            "author_uri": author_uri,
            "author_name": author_name,
        },
        "image_valid": None,
        "extraction_status": "metadata_extracted",
    }


def extract_reviews(
    input_file: Path,
    output_file: Path,
    max_records: int | None = None,
) -> dict[str, Any]:
    if not input_file.is_file():
        raise FileNotFoundError(f"Archive CIMPLE introuvable : {input_file}")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    LOGGER.info("Lecture de l'archive CIMPLE : %s", input_file)
    graph = Graph()

    with gzip.open(input_file, "rb") as archive:
        graph.parse(source=archive, format="nt")

    LOGGER.info("Graphe RDF chargé : %s triplets", len(graph))

    reviews = sorted(
        graph.subjects(RDF.type, SCHEMA.ClaimReview),
        key=str,
    )

    LOGGER.info("Fiches ClaimReview trouvées : %s", len(reviews))

    counts = {
        "total": 0,
        "with_claim_text": 0,
        "without_claim_text": 0,
        "with_fact_check_url": 0,
        "with_verdict": 0,
        "without_verdict": 0,
        "verdicts": {},
    }

    with output_file.open("w", encoding="utf-8") as output:
        for review_uri in reviews:
            if max_records is not None and counts["total"] >= max_records:
                break

            record = normalize_review(graph, review_uri)
            output.write(json.dumps(record, ensure_ascii=False) + "\n")

            counts["total"] += 1

            if record["text_content"]:
                counts["with_claim_text"] += 1
            else:
                counts["without_claim_text"] += 1

            if record["fact_check_url"]:
                counts["with_fact_check_url"] += 1

            verdict = record["label"]
            if verdict:
                counts["with_verdict"] += 1
                counts["verdicts"][verdict] = (
                    counts["verdicts"].get(verdict, 0) + 1
                )
            else:
                counts["without_verdict"] += 1

    return counts


def generate_report(
    counts: dict[str, Any],
    report_file: Path,
    input_file: Path,
) -> None:
    report_file.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "source": "CIMPLE",
        "input_file": str(input_file),
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "statistics": counts,
    }

    with report_file.open("w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extraction des fiches ClaimReview de CIMPLE"
    )
    parser.add_argument("--config", default="config/settings.yaml")
    parser.add_argument("--max-records", type=int, default=None)
    args = parser.parse_args()

    config = load_config(Path(args.config))
    setup_logging(config)

    paths = config["paths"]
    source_config = config["sources"]["cimple"]

    input_file = Path(paths["raw"]) / source_config["input_file"]
    output_file = (
        Path(paths["interim"])
        / "cimplekg"
        / "cimple_claim_reviews.jsonl"
    )
    report_file = (
        Path(paths["reports"])
        / "cimplekg"
        / "cimple_extraction_report.json"
    )

    max_records = (
        args.max_records
        if args.max_records is not None
        else source_config.get("max_records")
    )

    if max_records is not None and max_records <= 0:
        parser.error("--max-records doit être supérieur à zéro")

    counts = extract_reviews(input_file, output_file, max_records)
    generate_report(counts, report_file, input_file)

    LOGGER.info("Extraction terminée : %s fiches", counts["total"])
    LOGGER.info("Fichier JSONL : %s", output_file)
    LOGGER.info("Rapport : %s", report_file)
    LOGGER.info("Statistiques : %s", counts)


if __name__ == "__main__":
    main()

