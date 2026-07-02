import pickle
import faiss

from sentence_transformers import SentenceTransformer


class Retriever:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.index = faiss.read_index("data/faiss.index")

        with open("data/metadata.pkl", "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query, top_k=10):

        embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        scores, indices = self.index.search(embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            item = self.metadata[idx].copy()

            item["score"] = float(score)

            results.append(item)

        return results


retriever = Retriever()