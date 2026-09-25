"""
Task 5 — Semantic search.

Embed query bằng chính hàm của Task 4, query ChromaDB và đổi cosine distance
thành similarity. Output phải theo SearchResult, sort giảm dần và không quá top_k.
"""

from .task4_chunking_indexing import embed_texts, get_collection


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """Trả về dense SearchResult theo score giảm dần."""
    query_vector = embed_texts([query])[0]
    collection = get_collection()

    response = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    results = []
    if (
        response
        and response.get("ids")
        and len(response["ids"]) > 0
        and len(response["ids"][0]) > 0
    ):
        ids = response["ids"][0]
        documents = response.get("documents", [[]])[0]
        metadatas = response.get("metadatas", [[]])[0]
        distances = response.get("distances", [[]])[0]

        seen_ids = set()
        for item_id, content, metadata, distance in zip(ids, documents, metadatas, distances):
            if item_id in seen_ids:
                continue
            seen_ids.add(item_id)
            meta = dict(metadata) if metadata else {}
            if "chunk_index" in meta:
                meta["chunk_index"] = int(meta["chunk_index"])
            if meta.get("url") == "":
                meta["url"] = None

            sim_score = max(0.0, 1.0 - float(distance))
            results.append({
                "id": str(item_id),
                "content": str(content),
                "score": float(sim_score),
                "metadata": meta,
                "retrieval_method": "dense",
            })

    # Sort descending by score
    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    for result in semantic_search("thủ tục đăng ký hộ kinh doanh", top_k=3):
        print(result["id"], result["score"], result["metadata"]["title"])
