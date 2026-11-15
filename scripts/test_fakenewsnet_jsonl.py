import json
from pathlib import Path

path = Path("/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/interim/fakenewsnet/fakenewsnet_publications.jsonl")
records = [json.loads(line) for line in path.open(encoding="utf-8")]

ids = [r["publication_id"] for r in records]

print("Nombre d'enregistrements :", len(records))
print("Identifiants uniques :", len(set(ids)))
print("Labels :", {label: sum(r["label"] == label for r in records) for label in ("fake", "true")})
print("Champs principaux présents :", all(
    all(key in r for key in ("publication_id", "title", "article_url", "label"))
    for r in records
))
print("Validation :", "OK" if len(records) == 40 and len(set(ids)) == 40 else "À vérifier")
