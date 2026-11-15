
import json
from pathlib import Path

JSONL_FILE = Path(
    "/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/"
    "interim/cimplekg/cimple_claim_reviews.jsonl"
)


def main():
    if not JSONL_FILE.is_file():
        raise FileNotFoundError(f"Fichier introuvable : {JSONL_FILE}")

    with JSONL_FILE.open(encoding="utf-8") as file:
        records = [json.loads(line) for line in file if line.strip()]

    print(f"Nombre de fiches : {len(records)}")

    required_fields = [
        "publication_id",
        "source_name",
        "title",
        "text_content",
        "fact_check_url",
        "label",
        "label_status",
    ]

    for index, record in enumerate(records[:3], start=1):
        print(f"\nFiche {index}")
        for field in (
            "publication_id",
            "title",
            "fact_check_url",
            "language",
            "label",
            "label_status",
        ):
            print(f"{field} : {record.get(field)}")

    missing_fields = {
        field: sum(record.get(field) is None for record in records)
        for field in required_fields
    }

    print("\nChamps manquants :")
    for field, count in missing_fields.items():
        print(f"  {field} : {count}")

    assert records, "Aucune fiche extraite"

    for record in records:
        assert record.get("publication_id"), "Identifiant manquant"
        assert record.get("source_name") == "CIMPLE"
        assert record.get("label_status") in {"fact_checked", "unlabeled"}

    print("\nValidation structurelle : OK")


if __name__ == "__main__":
    main()

