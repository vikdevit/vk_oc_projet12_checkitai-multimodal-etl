"""Test de lecture et de normalisation de 5 publications Fakeddit."""

from pathlib import Path

from checkitai.extraction.fakeddit import (
    load_config,
    normalize_record,
    read_fakeddit,
)


def main() -> None:
    """Lit et normalise cinq publications Fakeddit."""
    project_root = Path(__file__).resolve().parents[1]
    config = load_config(project_root / "config/settings.yaml")

    source = config["sources"]["fakeddit"]
    input_file = Path(config["paths"]["raw"]) / source["input_file"]

    records_processed = 0

    for chunk in read_fakeddit(
        input_file=input_file,
        chunk_size=5,
        max_records=5,
    ):
        for _, row in chunk.iterrows():
            normalized = normalize_record(row.to_dict())

            assert normalized["publication_id"] is not None
            assert normalized["title"] is not None
            assert "source_labels" in normalized

            records_processed += 1

            print(f"\nPublication {records_processed}")
            print("Identifiant :", normalized["publication_id"])
            print("Titre :", normalized["title"])
            print("Label :", normalized["label"])
            print("Image :", normalized["image_url"])

    print("\nTest de normalisation terminé.")
    print("Publications traitées :", records_processed)

    assert records_processed == 5, (
        f"5 publications attendues, {records_processed} obtenues."
    )


if __name__ == "__main__":
    main()
