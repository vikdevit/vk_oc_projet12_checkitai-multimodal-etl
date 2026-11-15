import json
from pathlib import Path

base = Path("/mnt/data/vk_oc_projet12_checkitai-multimodal-etl")
jsonl = base / "interim/fakeddit/fakeddit_publications.jsonl"
report = base / "reports/fakeddit/fakeddit_extraction_report.json"

records = [json.loads(line) for line in jsonl.open(encoding="utf-8")]
stats = json.loads(report.read_text(encoding="utf-8"))

images = [
    record for record in records
    if record.get("image_path") and Path(record["image_path"]).is_file()
]

print("Publications JSONL :", len(records))
print("Images présentes sur disque :", len(images))
print("Statistiques du rapport :", stats["statistics"])
print("Vérification :", "OK" if len(records) == 5 and len(images) == 3 else "À vérifier")

