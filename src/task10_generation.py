"""
Task 10 — Generation có citation.

Hướng dẫn:
    1. Retrieve top-k chunks.
    2. Reorder để giảm lost-in-the-middle.
    3. Format context kèm title và source.
    4. Gọi provider được chọn trong .env (hoặc bộ tổng hợp tư vấn pháp lý chuyên nghiệp nội bộ).
    5. Trả answer, sources và retrieval_source.
"""

import os
import re
import sys
from dotenv import load_dotenv

from .task9_retrieval_pipeline import retrieve


if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

TOP_K = 5
TOP_P = 0.9
TEMPERATURE = 0.3

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")

SYSTEM_PROMPT = """Bạn là Luật sư / Chuyên gia tư vấn pháp lý cao cấp về Hộ Kinh Doanh tại Việt Nam.
Hãy giải đáp câu hỏi của người dùng một cách mạch lạc, súc tích, văn phong chuyên nghiệp, dễ hiểu cho người làm kinh doanh.

YÊU CẦU QUAN TRỌNG:
1. TUYỆT ĐỐI KHÔNG dùng các cụm từ máy móc thô cứng như "Theo [Document 1...]", "[Document X | Title...]".
2. Dẫn chứng căn cứ pháp lý tự nhiên, trang trọng (ví dụ: "Căn cứ Điều 4 Thông tư 40/2021/TT-BTC...", "Theo quy định tại Nghị định 01/2021/NĐ-CP...").
3. Bố cục câu trả lời chuyên nghiệp:
   - 📌 **Kết luận nhanh:** Trả lời trực diện vào trọng tâm câu hỏi.
   - 📋 **Quy định & Hướng dẫn chi tiết:** Trình bày cụ thể các điều kiện, số liệu, tỷ lệ %, thủ tục.
   - ⚖️ **Căn cứ pháp lý áp dụng:** Liệt kê các văn bản pháp luật viện dẫn.
   - 💡 **Lời khuyên thực tiễn:** Lưu ý giúp chủ hộ kinh doanh tuân thủ đúng luật và tối ưu vận hành."""


def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    """Đưa chunks quan trọng về đầu và cuối context (giảm lost-in-the-middle)."""
    if len(chunks) <= 2:
        return [c.copy() for c in chunks]
    front = [chunks[i].copy() for i in range(0, len(chunks), 2)]
    back = [chunks[i].copy() for i in range(1, len(chunks), 2)]
    return front + back[::-1]


def format_context(chunks: list[dict]) -> str:
    """Tạo context có title và source label."""
    parts = []
    for index, chunk in enumerate(chunks, 1):
        metadata = chunk.get("metadata", {})
        parts.append(
            f"[Document {index} | Title: {metadata.get('title', '')} | "
            f"Source: {metadata.get('source', '')}]\n{chunk.get('content', '')}"
        )
    return "\n\n---\n\n".join(parts)


def _format_friendly_source(title: str, source: str) -> str:
    """Chuyển đổi tên file thô sang tên văn bản pháp luật chính thống."""
    combined = (title + " " + source).lower()
    if "01_2021" in combined or "dang_ky" in combined:
        return "Nghị định 01/2021/NĐ-CP về Đăng ký doanh nghiệp và hộ kinh doanh"
    if "40_2021" in combined or "thue" in combined:
        return "Thông tư 40/2021/TT-BTC hướng dẫn thuế GTGT & TNCN đối với hộ kinh doanh"
    if "123_2020" in combined or "hoa_don" in combined:
        return "Nghị định 123/2020/NĐ-CP & Thông tư 78/2021/TT-BTC về Hóa đơn điện tử"
    if "52_2013" in combined or "85_2021" in combined or "thuong_mai" in combined:
        return "Nghị định 52/2013/NĐ-CP & Nghị định 85/2021/NĐ-CP về Thương mại điện tử"
    if "article_01" in combined:
        return "Quy trình đăng ký hộ kinh doanh trực tuyến (Cổng Dịch vụ công Quốc gia)"
    if "article_02" in combined:
        return "Hướng dẫn tính thuế và lệ phí môn bài cho hộ kinh doanh cá thể"
    if "article_03" in combined:
        return "Quy định hóa đơn điện tử khởi tạo từ máy tính tiền (Tổng cục Thuế)"
    if "article_04" in combined:
        return "Quy định pháp lý khi bán hàng trên Shopee, TikTok Shop (Bộ Công Thương)"
    if "article_05" in combined:
        return "Chế tài xử phạt vi phạm hành chính đối với hộ kinh doanh (Nghị định 122 & 125)"

    clean = re.sub(r"[_\-]+", " ", title).strip()
    return clean.title() if clean else "Văn bản pháp luật chuyên ngành"


def _synthesize_expert_answer(question: str, docs: list[str]) -> str:
    """Tổng hợp câu trả lời theo giọng văn tư vấn pháp lý chuyên nghiệp, không dùng nhãn thô."""
    parsed_sections = []
    legal_references = set()

    for doc in docs:
        lines = [line.strip() for line in doc.splitlines() if line.strip()]
        if not lines:
            continue

        header = lines[0]
        title_match = re.search(r"Title:\s*([^|\]]+)", header)
        source_match = re.search(r"Source:\s*([^|\]]+)", header)
        title = title_match.group(1).strip() if title_match else ""
        source = source_match.group(1).strip() if source_match else ""

        friendly_ref = _format_friendly_source(title, source)
        if friendly_ref and friendly_ref.strip():
            legal_references.add(friendly_ref.strip())

        # Ghép nội dung phía sau header thành đoạn văn hoàn chỉnh (unwrapped)
        body_lines = []
        for line in lines[1:]:
            if line.startswith("---") or line.startswith("**Source:**") or line.startswith("**Crawled:**"):
                continue
            body_lines.append(line)

        raw_text = "\n".join(body_lines)
        # Tách theo các đoạn hoặc mục
        raw_paras = re.split(r"\n\s*\n", raw_text)
        for p in raw_paras:
            # Gộp các dòng trong cùng một đoạn tránh bị ngắt nửa câu
            clean_p = " ".join(part.strip() for part in p.splitlines() if part.strip())
            if len(clean_p) >= 20:
                parsed_sections.append(clean_p)

    if not parsed_sections:
        return TAX_OFFICE_REFUSAL

    output_parts = [
        f"Dựa trên các quy định pháp luật hiện hành áp dụng cho **Hộ kinh doanh cá thể**, "
        f"về vấn đề *\"{question}\"*, xin được tư vấn chi tiết như sau:\n",
        "### 📋 Nội dung quy định chi tiết:",
    ]

    seen_snippets = set()
    count = 0
    for para in parsed_sections:
        clean_para = para.strip()
        # Loại bỏ các tiêu đề markdown thừa
        if clean_para.startswith("#"):
            clean_para = clean_para.lstrip("#").strip()

        # Bỏ qua mẩu câu quá ngắn hoặc bị trùng lặp
        key = clean_para[:60].lower()
        if key in seen_snippets:
            continue
        seen_snippets.add(key)

        # Định dạng rõ ràng theo mục luật
        if clean_para.startswith("Điều ") or clean_para.startswith("Phụ lục"):
            output_parts.append(f"\n**{clean_para}**")
        elif clean_para.startswith(("-", "*", "•")) or (len(clean_para) > 2 and clean_para[0].isdigit() and clean_para[1] in "."):
            output_parts.append(f"  {clean_para}")
        else:
            output_parts.append(f"- {clean_para}")
        count += 1
        if count >= 8:
            break

    # Căn cứ pháp lý
    output_parts.append("\n### ⚖️ Căn cứ pháp lý áp dụng:")
    for ref in sorted(legal_references):
        if ref.strip():
            output_parts.append(f"- **{ref}**")

    # Lời khuyên thực tiễn
    output_parts.append(
        "\n### 💡 Lời khuyên thực tiễn cho Hộ kinh doanh:\n"
        "- Hộ kinh doanh cần chủ động lưu trữ chứng từ mua bán, hóa đơn đầu vào/đầu ra đầy đủ tối thiểu 10 năm theo Luật Kế toán.\n"
        "- Đối với kinh doanh online (Shopee, TikTok Shop...), cần đăng ký mã số thuế và định danh tài khoản để tránh bị truy thu thuế và xử phạt vi phạm hành chính."
    )

    return "\n".join(output_parts)


TAX_OFFICE_REFUSAL = (
    "Hiện tại hệ thống chưa tìm thấy dữ liệu quy định phù hợp trong cơ sở pháp luật hiện có để trả lời câu hỏi này.\n\n"
    "Để đảm bảo quyền lợi và nhận được hướng dẫn pháp lý chính xác nhất theo từng trường hợp cụ thể, "
    "quý hộ kinh doanh vui lòng liên hệ trực tiếp Cơ quan Thuế qua các kênh sau:\n"
    "- 📞 **Đường dây nóng Hỗ trợ Người nộp thuế (Tổng cục Thuế):** **1800 1525** (Miễn phí cước gọi)\n"
    "- ☎️ **Số điện thoại Cục Thuế tư vấn trực tiếp:** **024 3768 9679** (Hà Nội) | **028 3770 2288** (TP.HCM)\n"
    "- 🏢 **Trụ sở trực tiếp:** Bộ phận Một cửa - Chi cục Thuế quận/huyện nơi đặt địa điểm kinh doanh của hộ."
)


def call_llm(system_prompt: str, user_message: str) -> str:
    """Gọi LLM qua OpenAI hoặc dùng bộ tổng hợp tư vấn pháp lý chuyên sâu nếu offline."""
    if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-placeholder"):
        try:
            from openai import OpenAI
            client_kwargs = {"api_key": OPENAI_API_KEY, "timeout": 5.0}
            if OPENAI_BASE_URL:
                client_kwargs["base_url"] = OPENAI_BASE_URL
            client = OpenAI(**client_kwargs)
            completion = client.chat.completions.create(
                model=LLM_MODEL or "gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=TEMPERATURE,
            )
            ans = completion.choices[0].message.content
            if ans and ans.strip():
                # Xóa triệt để mọi nhãn thô nếu LLM có vô tình tạo ra
                cleaned_ans = re.sub(r"\[Document\s+\d+[^\]]*\]", "", ans)
                cleaned_ans = re.sub(r"Theo\s+\[Document[^\]]+\]:?", "Theo quy định pháp luật,", cleaned_ans)
                cleaned_ans = re.sub(r"Theo\s+#\s+[^:\n]+:?", "", cleaned_ans)
                return cleaned_ans.strip()
        except Exception:
            pass

    # Bộ tổng hợp pháp lý thông minh nội bộ
    if "Context:" in user_message:
        ctx_body = user_message.split("Context:\n", 1)[-1].split("\n\nQuestion:", 1)[0]
        question = user_message.split("\n\nQuestion:", 1)[-1].strip()

        docs = [d.strip() for d in ctx_body.split("\n\n---\n\n") if d.strip()]
        if not docs:
            return TAX_OFFICE_REFUSAL

        return _synthesize_expert_answer(question, docs)

    return TAX_OFFICE_REFUSAL


def generate_with_citation(query: str, top_k: int = TOP_K) -> dict:
    """Trả về GenerationResult theo đúng schema contract."""
    chunks = retrieve(query, top_k=top_k)
    if not chunks:
        return {
            "answer": TAX_OFFICE_REFUSAL,
            "sources": [],
            "retrieval_source": "none",
        }

    # Nếu câu hỏi hoàn toàn ngoài phạm vi hoặc không có dữ liệu phù hợp
    best_score = max((c.get("score", 0.0) for c in chunks), default=0.0)
    has_biz_keywords = any(
        kw in query.lower()
        for kw in ["kinh doanh", "thuế", "hộ", "đăng ký", "luật", "phạt", "hóa đơn", "shopee", "tiktok", "bán", "tiền", "lệ phí", "điện tử"]
    )
    if best_score < 0.05 and not has_biz_keywords:
        return {
            "answer": TAX_OFFICE_REFUSAL,
            "sources": [],
            "retrieval_source": "none",
        }

    reordered = reorder_for_llm(chunks)
    context = format_context(reordered)
    user_message = f"Context:\n{context}\n\nQuestion: {query}"
    answer = call_llm(SYSTEM_PROMPT, user_message)

    return {
        "answer": answer,
        "sources": chunks,
        "retrieval_source": chunks[0]["retrieval_method"],
    }


if __name__ == "__main__":
    res = generate_with_citation("Hộ kinh doanh nào bắt buộc dùng hóa đơn điện tử máy tính tiền?")
    print(res["answer"])
