
"""Vérifie les fichiers produits par l'extraction Fakeddit."""

import json
from pathlib import Path


def main() -> None:
    """Contrôle le JSONL et le rapport d'extraction."""

    data_file = Path(
        "/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/"
        "interim/fakeddit/fakeddit_publications.jsonl"
    )

    report_file = Path(
        "/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/"
        "reports/fakeddit/fakeddit_extraction_report.json"
    )

    with data_file.open(encoding="utf-8") as file:
        records = [
            json.loads(line)
            for line in file
            if line.strip()
        ]

    with report_file.open(encoding="utf-8") as file:
        report = json.load(file)

    print("Nombre de lignes JSONL :", len(records))

    print(
        "Nombre d'identifiants :",
        len({
            record["publication_id"]
            for record in records
        }),
    )

    print("Champs du premier enregistrement :")
    print(sorted(records[0].keys()))

    print("\nContenu du rapport :")
    print(json.dumps(report, indent=2, ensure_ascii=False))

    assert len(records) == 100, "Le nombre de publications est incorrect."
    assert all(
        record.get("publication_id")
        for record in records
    ), "Un identifiant de publication est manquant."

    print("\nVérification des fichiers réussie.")


if __name__ == "__main__":
    main()

