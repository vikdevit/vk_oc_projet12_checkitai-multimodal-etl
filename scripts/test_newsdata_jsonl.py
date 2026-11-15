import json
from pathlib import Path

path = Path(
    "/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/"
    "interim/newsdata/newsdata_publications.jsonl"
)

records = [json.loads(line) for line in path.open(encoding="utf-8")]

ids = [r["publication_id"] for r in records]

required_fields = (
    "publication_id",
    "title",
    "article_url",
    "image_url",
    "label",
    "source_name",
)

print("Nombre d'enregistrements :", len(records))
print("Identifiants présents :", sum(bool(value) for value in ids))
print("Titres présents :", sum(bool(r["title"]) for r in records))
print("URLs d'images présentes :", sum(bool(r["image_url"]) for r in records))
print("Labels non renseignés :", sum(r["label"] is None for r in records))
print(
    "Champs principaux présents :",
    all(all(key in r for key in required_fields) for r in records),
)

valid = (
    len(records) == 10
    and all(ids)
    and all(all(key in r for key in required_fields) for r in records)
)

print("Validation :", "OK" if valid else "À vérifier")
