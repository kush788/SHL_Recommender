from retriever import retriever

results = retriever.search(
    "Hiring a Java developer with stakeholder communication",
    top_k=5
)

for i, item in enumerate(results, 1):
    print("=" * 60)
    print(i)
    print(item["name"])
    print(item["url"])
    print(item["score"])