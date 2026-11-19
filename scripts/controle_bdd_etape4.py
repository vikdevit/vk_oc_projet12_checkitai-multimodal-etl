import sqlite3
from pathlib import Path

db = Path("/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/processed/checkitai.db")

with sqlite3.connect(db) as conn:
    print("ÉTAT DE LA BASE")
    print("Intégrité :", conn.execute("PRAGMA integrity_check").fetchone()[0])
    print("Clés étrangères :", conn.execute("PRAGMA foreign_key_check").fetchall())

    print("\nNOMBRE D'ENREGISTREMENTS")
    for table in ("sources", "content_records", "image_assets", "label_assessments"):
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {count}")

    print("\nRÉPARTITION PAR SOURCE")
    for source, count in conn.execute(
        "SELECT source_name, COUNT(*) FROM content_records GROUP BY source_name ORDER BY source_name"
    ):
        print(f"{source}: {count}")

