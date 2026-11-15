"""Test d'écriture et de relecture de 5 publications Fakeddit en JSONL."""

import json
from pathlib import Path

from checkitai.extraction.fakeddit import (
    load_config,
    normalize_record,
    read_fakeddit,
    save_records,
)


def main() -> None:
    """Extrait cinq publications, les sauvegarde et vérifie le JSONL."""
    project_root = Path(__file__).resolve().parents[1]
    config = load_config(project_root / "config/settings.yaml")

    source = config["sources"]["fakeddit"]

    input_file = Path(config["paths"]["raw"]) / source["input_file"]
    output_file = (
        Path(config["paths"]["interim"])
        / "fakeddit"
        / "fakeddit_test.jsonl"
    )

    normalized_records = []

    for chunk in read_fakeddit(
        input_file=input_file,
        chunk_size=5,
        max_records=5,
    ):
        for _, row in chunk.iterrows():
            normalized_records.append(normalize_record(row.to_dict()))

    saved = save_records(normalized_records, output_file)

    assert saved == 5, f"5 publications attendues, {saved} enregistrées."

    # Relecture et validation du fichier JSONL.
    records_read = []

    with output_file.open("r", encoding="utf-8") as jsonl_file:
        for line_number, line in enumerate(jsonl_file, start=1):
            record = json.loads(line)

            assert isinstance(record, dict), (
                f"La ligne {line_number} n'est pas un objet JSON."
            )
            assert record.get("publication_id"), (
                f"Identifiant absent à la ligne {line_number}."
            )

            records_read.append(record)

    assert len(records_read) == 5

    print("\nTest JSONL terminé avec succès.")
    print("Publications enregistrées :", saved)
    print("Publications relues :", len(records_read))
    print("Fichier :", output_file)
    print("Taille :", output_file.stat().st_size, "octets")


if __name__ == "__main__":
    main()
