
"""Teste le téléchargement réel d'un maximum de cinq images Fakeddit."""

import logging
from pathlib import Path

from checkitai.extraction.common.image_validator import download_image
from checkitai.extraction.fakeddit import (
    load_config,
    normalize_record,
    read_fakeddit,
)


def main() -> None:
    """Télécharge un petit échantillon d'images pour validation."""

    logging.basicConfig(level=logging.INFO)

    project_root = Path(__file__).resolve().parents[1]
    config = load_config(project_root / "config/settings.yaml")

    source_config = config["sources"]["fakeddit"]

    input_file = (
        Path(config["paths"]["raw"])
        / source_config["input_file"]
    )

    output_dir = (
        Path(config["paths"]["images"])
        / "fakeddit"
        / "test_real"
    )

    extraction_config = config["extraction"]

    successful = 0
    failed = 0
    skipped = 0

    print("Test réel limité aux cinq premières publications Fakeddit.")

    for chunk in read_fakeddit(
        input_file=input_file,
        chunk_size=5,
        max_records=5,
    ):
        for _, row in chunk.iterrows():
            record = normalize_record(row.to_dict())

            image_url = record["image_url"]
            publication_id = record["publication_id"]

            if not image_url:
                skipped += 1
                print(f"URL absente : {publication_id}")
                continue

            print(f"\nPublication : {publication_id}")
            print("URL :", image_url)

            result = download_image(
                url=image_url,
                output_dir=output_dir,
                publication_id=publication_id,
                config=extraction_config,
            )

            if result["image_valid"]:
                successful += 1
                print("Résultat : image téléchargée")
                print("Fichier :", result["image_path"])
                print("Taille :", result["image_size_bytes"], "octets")
            else:
                failed += 1
                print("Résultat : échec")
                print("Motif :", result["download_error"])

    print("\nBilan du test")
    print("Images téléchargées :", successful)
    print("Échecs :", failed)
    print("URL absentes :", skipped)
    print("Dossier :", output_dir)


if __name__ == "__main__":
    main()

