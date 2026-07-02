import json

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


class Retriever:

    def search(self, query, top_k=10):

        query = query.lower()

        scored = []

        for item in catalog:

            text = (
                item.get("name", "")
                + " "
                + item.get("description", "")
                + " "
                + " ".join(item.get("keys", []))
            ).lower()

            score = sum(word in text for word in query.split())

            if score > 0:
                scored.append((score, item))

        scored.sort(reverse=True, key=lambda x: x[0])

        return [x[1] for x in scored[:top_k]]


retriever = Retriever()
