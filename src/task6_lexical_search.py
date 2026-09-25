"""
Task 6 — Lexical search bằng BM25.

Dùng cùng corpus chunks với Task 5. BM25 phù hợp với từ khóa chính xác, mã tài
liệu và tên riêng. Output phải theo SearchResult và sort score giảm dần.
"""

from rank_bm25 import BM25Okapi


CORPUS: list[dict] = []


def build_bm25_index(corpus: list[dict]) -> BM25Okapi:
    """Tạo BM25 index từ danh sách chunks."""
    tokenized = [item["content"].lower().split() for item in corpus]
    return BM25Okapi(tokenized)


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """Trả về BM25 SearchResult theo score giảm dần."""
    global CORPUS
    if not CORPUS:
        try:
            from .task4_chunking_indexing import chunk_documents, load_documents
            CORPUS = chunk_documents(load_documents())
        except Exception:
            CORPUS = []

    if not CORPUS:
        return []

    bm25 = build_bm25_index(CORPUS)
    query_tokens = query.lower().split()
    if not query_tokens:
        scores = [0.0] * len(CORPUS)
    else:
        scores = bm25.get_scores(query_tokens)

    # Sort indices by score descending
    indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

    results = []
    seen_ids = set()
    for idx in indices:
        item = CORPUS[idx]
        item_id = item["id"]
        if item_id in seen_ids:
            continue
        seen_ids.add(item_id)

        meta = dict(item["metadata"])
        if "chunk_index" in meta:
            meta["chunk_index"] = int(meta["chunk_index"])
        if meta.get("url") == "":
            meta["url"] = None

        results.append({
            "id": item_id,
            "content": item["content"],
            "score": float(scores[idx]),
            "metadata": meta,
            "retrieval_method": "bm25",
        })
        if len(results) >= top_k:
            break

    return results


if __name__ == "__main__":
    for res in lexical_search("thuế hộ kinh doanh Thông tư 40", top_k=3):
        print(res["id"], res["score"], res["metadata"]["title"])
