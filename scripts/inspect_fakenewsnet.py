"""Inspecte les colonnes et quelques exemples des CSV FakeNewsNet."""

from pathlib import Path

import pandas as pd


DATA_DIRECTORY = Path(
    "/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/fakenewsnet"
)


def main() -> None:
    """Affiche la structure des fichiers CSV FakeNewsNet."""
    if not DATA_DIRECTORY.exists():
        raise FileNotFoundError(
            f"Répertoire introuvable : {DATA_DIRECTORY}"
        )

    csv_files = sorted(DATA_DIRECTORY.glob("*.csv"))

    if not csv_files:
        print("Aucun fichier CSV trouvé.")
        return

    for file in csv_files:
        dataframe = pd.read_csv(file, nrows=3)

        print("\n" + "=" * 60)
        print(f"FICHIER : {file.name}")
        print("Colonnes :", list(dataframe.columns))
        print("Exemples :")
        print(dataframe.head(2).to_string(index=False))


if __name__ == "__main__":
    main()
