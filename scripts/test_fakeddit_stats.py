from pathlib import Path

from checkitai.extraction.fakeddit import (
    load_config,
    read_fakeddit,
    normalize_record,
    calculate_statistics,
)

config = load_config(Path("config/settings.yaml"))
source = config["sources"]["fakeddit"]

input_file = Path(config["paths"]["raw"]) / source["input_file"]

records = []

for chunk in read_fakeddit(
    input_file=input_file,
    chunk_size=5,
    max_records=5,
):
    for _, row in chunk.iterrows():
        records.append(normalize_record(row.to_dict()))

statistics = calculate_statistics(records)

print("Statistiques des cinq publications :")
print(statistics)

assert statistics["total_records"] == 5
assert (
    statistics["label_distribution"]["fake"]
    + statistics["label_distribution"]["true"]
    + statistics["label_distribution"]["missing"]
    == 5
)

print("\nContrôle des statistiques réussi.")

