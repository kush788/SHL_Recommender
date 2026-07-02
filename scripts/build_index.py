import os
import json
import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

CATALOG_PATH = "catalog.json"
INDEX_PATH = "data/faiss.index"
META_PATH = "data/metadata.pkl"

os.makedirs("data", exist_ok=True)

print("Loading catalog...")

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

print(f"Loaded {len(catalog)} assessments")

documents = []
metadata = []

for item in catalog:

    text = f"""
Name: {item.get("name","")}

Description:
{item.get("description","")}

Job Levels:
{', '.join(item.get("job_levels", []))}

Keys:
{', '.join(item.get("keys", []))}

Languages:
{', '.join(item.get("languages", []))}

Duration:
{item.get("duration","")}

Remote:
{item.get("remote","")}

Adaptive:
{item.get("adaptive","")}
"""

    documents.append(text)

    metadata.append({
        "name": item.get("name"),
        "url": item.get("link"),
        "description": item.get("description"),
        "keys": item.get("keys"),
        "job_levels": item.get("job_levels")
    })

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    normalize_embeddings=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

faiss.write_index(index, INDEX_PATH)

with open(META_PATH, "wb") as f:
    pickle.dump(metadata, f)

print("Done!")
print("Index saved.")