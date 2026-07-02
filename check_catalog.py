import json

with open("catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data[0].keys())