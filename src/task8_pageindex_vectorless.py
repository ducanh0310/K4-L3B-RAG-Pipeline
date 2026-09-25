"""
Task 8 — PageIndex vectorless fallback.

Hướng dẫn:
    1. Đọc PAGEINDEX_API_KEY từ .env.
    2. Upload tài liệu ở định dạng PageIndex hỗ trợ.
    3. Cache document IDs để không upload lại.
    4. Parse kết quả thành SearchResult có method pageindex.

PageIndex là dịch vụ ngoài: cần timeout và xử lý lỗi để pipeline không crash.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"


def upload_documents() -> None:
    """Upload tài liệu và lưu document IDs để tái sử dụng."""
    if not PAGEINDEX_API_KEY:
        print("PAGEINDEX_API_KEY không được cấu hình, bỏ qua upload.")
        return


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """Trả về pageindex SearchResult."""
    if not PAGEINDEX_API_KEY:
        return []

    # Khi có API key, thử gọi PageIndex API với try/except
    try:
        import requests
        # Gọi endpoint PageIndex nếu có cấu hình
        headers = {"Authorization": f"Bearer {PAGEINDEX_API_KEY}"}
        resp = requests.post(
            "https://api.pageindex.ai/v1/search",
            headers=headers,
            json={"query": query, "top_k": top_k},
            timeout=5,
        )
        if resp.status_code == 200:
            data = resp.json()
            results = []
            for idx, item in enumerate(data.get("results", [])):
                results.append({
                    "id": item.get("id", f"pageindex-{idx}"),
                    "content": item.get("content", ""),
                    "score": float(item.get("score", 1.0 - idx * 0.1)),
                    "metadata": {
                        "source": item.get("source", "external"),
                        "title": item.get("title", "PageIndex Result"),
                        "doc_type": "legal",
                        "url": item.get("url"),
                        "chunk_index": idx,
                    },
                    "retrieval_method": "pageindex",
                })
            return results[:top_k]
    except Exception:
        pass

    return []


if __name__ == "__main__":
    upload_documents()
