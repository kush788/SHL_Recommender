import json

with open("catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    if item["name"] == "Virtual Assessment and Development Centers":
        import pprint
        pprint.pprint(item)