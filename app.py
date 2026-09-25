import html
import importlib
from pathlib import Path
import re
import streamlit as st
from dotenv import load_dotenv

import src.task10_generation as gen_mod
importlib.reload(gen_mod)
from src.task10_generation import generate_with_citation
from src.task5_semantic_search import semantic_search
from src.task6_lexical_search import lexical_search
from src.task9_retrieval_pipeline import retrieve


def sanitize_display(text: str) -> str:
    """Loại bỏ hoàn toàn các tiền tố thô cứng 'Theo [Document...]' hoặc 'Theo #' nếu còn sót lại."""
    cleaned = re.sub(r"Theo\s+\[Document\s+\d+[^\]]*\]:?", "", text)
    cleaned = re.sub(r"\[Document\s+\d+[^\]]*\]", "", cleaned)
    cleaned = re.sub(r"Theo\s+#\s+[^:\n]+:?", "", cleaned)
    return cleaned.strip()


load_dotenv()

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="LawBiz AI — Trợ lý Pháp lý Hộ Kinh Doanh",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS giao diện hiện đại, sang trọng
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        padding: 28px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.25);
    }
    .main-header h1 {
        color: white !important;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .main-header p {
        color: #e0f2fe;
        font-size: 0.95rem;
        margin-top: 8px;
        margin-bottom: 0;
    }

    .badge-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-legal {
        background-color: #dbeafe;
        color: #1e40af;
        border: 1px solid #bfdbfe;
    }
    .badge-news {
        background-color: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
    }
    .badge-hybrid {
        background-color: #dcfce7;
        color: #166534;
        border: 1px solid #bbf7d0;
    }

    .source-card {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(226, 232, 240, 0.15);
        border-radius: 10px;
        padding: 12px 16px;
        margin-top: 8px;
        margin-bottom: 8px;
        transition: all 0.2s ease-in-out;
    }
    .source-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }

    .quick-chip-btn {
        margin-bottom: 8px;
    }

    .stButton>button {
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        border-color: #3b82f6;
        color: #3b82f6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Khởi tạo session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Xin chào! Tôi là **LawBiz AI** — Trợ lý thông minh hỗ trợ giải đáp pháp luật chuyên sâu "
                "dành cho **Hộ Kinh Doanh**.\n\n"
                "Tôi có thể hỗ trợ bạn các vấn đề chính sau:\n"
                "- 📋 **Đăng ký kinh doanh:** Thủ tục cấp phép, địa điểm, hồ sơ tại UBND cấp huyện.\n"
                "- 💰 **Thuế & Lệ phí:** Thuế khoán, thuế kê khai, ngưỡng miễn thuế 100 triệu, lệ phí môn bài.\n"
                "- 🧾 **Hóa đơn điện tử:** Quy định hóa đơn khởi tạo từ máy tính tiền.\n"
                "- 🌐 **Thương mại điện tử:** Nghĩa vụ thuế khi bán hàng trên TikTok Shop, Shopee, website TMĐT.\n\n"
                "Bạn có thể chọn một trong các câu hỏi gợi ý bên dưới hoặc gõ câu hỏi của mình."
            ),
            "sources": [],
            "retrieval_source": "none",
        }
    ]

# Sidebar Cấu hình & Kiểm soát
with st.sidebar:
    st.markdown("### ⚖️ LawBiz AI Config")
    st.caption("Hệ thống RAG Pipeline Pháp luật Hộ kinh doanh")

    st.markdown("---")
    st.markdown("#### ⚙️ Chế độ truy xuất (Retrieval)")
    retrieval_mode = st.radio(
        "Thuật toán tìm kiếm:",
        ["Hybrid (RRF Fusion) ⭐", "Dense (Semantic Search)", "BM25 (Lexical Search)"],
        index=0,
        help="RRF kết hợp độ chính xác từ khóa của BM25 và ngữ nghĩa của Dense Vector Search.",
    )

    top_k = st.slider(
        "Số lượng trích đoạn (Top-K Chunks):",
        min_value=2,
        max_value=8,
        value=4,
        help="Số lượng phân đoạn tài liệu đưa vào ngữ cảnh trả lời.",
    )

    show_sources_detail = st.checkbox("Hiển thị chi tiết trích dẫn nguồn", value=True)

    st.markdown("---")
    st.markdown("#### 📊 Cơ sở tri thức (Knowledge Base)")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Văn bản luật", "4 files")
        st.metric("Khoản mục", "44 chunks")
    with col2:
        st.metric("Bài viết/Tin", "5 files")
        st.metric("Độ phủ", "100%")

    with st.expander("📚 Danh mục tài liệu trong hệ thống"):
        st.markdown(
            """
            **1. Văn bản chính sách (Legal):**
            - `Nghị định 01/2021/NĐ-CP`: Đăng ký kinh doanh hộ cá thể.
            - `Thông tư 40/2021/TT-BTC`: Thuế GTGT & TNCN hộ kinh doanh.
            - `Nghị định 123/2020/NĐ-CP`: Hóa đơn điện tử máy tính tiền.
            - `Nghị định 52 & 85`: Quy định thương mại điện tử.
            
            **2. Hướng dẫn thực tiễn (News):**
            - Thủ tục đăng ký online qua Cổng Dịch vụ công.
            - Cách tính thuế khoán & kê khai thực tế.
            - Bắt buộc hóa đơn máy tính tiền cho nhà hàng, bán lẻ.
            - Kê khai thuế bán hàng Shopee, TikTok Shop.
            - Mức phạt vi phạm hành chính thường gặp.
            """
        )

    if st.button("🗑️ Xóa lịch sử hội thoại", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

# Header chính
st.markdown(
    """
    <div class="main-header">
        <h1>⚖️ Trợ Lý Pháp Lý Hộ Kinh Doanh</h1>
        <p>Hệ thống RAG Pipeline chuyên sâu: Đăng ký kinh doanh • Thuế GTGT & TNCN • Hóa đơn điện tử • Thương mại điện tử</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Gợi ý câu hỏi nhanh (Quick Suggestion Chips)
st.markdown("##### 💡 Câu hỏi gợi ý phổ biến:")
quick_queries = [
    "Hồ sơ đăng ký hộ kinh doanh cá thể gồm những gì?",
    "Ngưỡng doanh thu nào được miễn thuế GTGT và TNCN?",
    "Bán hàng trên TikTok Shop, Shopee phải nộp bao nhiêu % thuế?",
    "Hộ kinh doanh nào bắt buộc dùng hóa đơn điện tử máy tính tiền?",
    "Không đăng ký hộ kinh doanh bị phạt bao nhiêu tiền?",
    "Tra cứu quy định chưa có (Test case liên hệ Cục Thuế & SDT)",
]

selected_chip = None
chip_cols = st.columns(3)
for idx, q_text in enumerate(quick_queries):
    col = chip_cols[idx % 3]
    with col:
        if st.button(f"📌 {q_text}", key=f"chip_{idx}", use_container_width=True):
            selected_chip = q_text

st.markdown("---")

# Render các tin nhắn trong lịch sử
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="⚖️" if msg["role"] == "assistant" else "👤"):
        st.markdown(sanitize_display(msg["content"]))

        if msg.get("retrieval_source") == "none" and len(msg.get("sources", [])) == 0 and msg["role"] == "assistant":
            st.warning("📞 **Trực tiếp từ Cơ quan Thuế:** Bạn có thể gọi ngay đến Tổng đài miễn cước **1800 1525** để được cán bộ thuế hỗ trợ giải đáp trực tiếp.")

        # Hiển thị sources nếu có
        sources = msg.get("sources", [])
        if sources and show_sources_detail:
            method_used = msg.get("retrieval_source", "hybrid").upper()
            with st.expander(f"📑 Căn cứ nguồn trích dẫn ({len(sources)} tài liệu | Phương thức: {method_used})"):
                for idx, src in enumerate(sources, 1):
                    meta = src.get("metadata", {})
                    title = meta.get("title", "Tài liệu tham chiếu")
                    source_name = meta.get("source", "Tài liệu hệ thống")
                    doc_type = meta.get("doc_type", "legal")
                    score = src.get("score", 0.0)
                    chunk_text = src.get("content", "").strip()

                    badge_class = "badge-legal" if doc_type == "legal" else "badge-news"
                    type_label = "Văn bản luật" if doc_type == "legal" else "Bài viết hướng dẫn"

                    st.markdown(
                        f"""
                        <div class="source-card">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <strong>#{idx}. {html.escape(title)}</strong>
                                <div>
                                    <span class="badge-pill {badge_class}">{type_label}</span>
                                    <span class="badge-pill badge-hybrid">Score: {score:.4f}</span>
                                </div>
                            </div>
                            <small style="color: #64748b;">Nguồn: <code>{html.escape(source_name)}</code></small>
                            <div style="margin-top: 8px; font-size: 0.88rem; line-height: 1.5; color: #334155; background: rgba(0,0,0,0.02); padding: 8px; border-radius: 6px;">
                                {html.escape(chunk_text[:350])}{'...' if len(chunk_text) > 350 else ''}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

# Xử lý input từ chat hoặc từ nút chip
query = st.chat_input("Nhập câu hỏi pháp luật về hộ kinh doanh của bạn...")
active_query = selected_chip or query

if active_query:
    # 1. Thêm tin nhắn của user
    st.session_state.messages.append({"role": "user", "content": active_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(active_query)

    # 2. Xử lý phản hồi từ assistant
    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner("Đang tra cứu cơ sở dữ liệu pháp luật và phân tích..."):
            if "Dense" in retrieval_mode:
                chunks = semantic_search(active_query, top_k=top_k)
                retrieval_type = "dense"
            elif "BM25" in retrieval_mode:
                chunks = lexical_search(active_query, top_k=top_k)
                retrieval_type = "bm25"
            else:
                chunks = retrieve(active_query, top_k=top_k, use_reranking=True)
                retrieval_type = "hybrid"

            # Sinh câu trả lời với trích dẫn
            gen_result = generate_with_citation(active_query, top_k=top_k)
            answer_text = sanitize_display(gen_result["answer"])
            sources = chunks or gen_result["sources"]

            st.markdown(answer_text)

            # Hiển thị sources
            if sources and show_sources_detail:
                with st.expander(f"📑 Căn cứ nguồn trích dẫn ({len(sources)} tài liệu | Phương thức: {retrieval_type.upper()})"):
                    for idx, src in enumerate(sources, 1):
                        meta = src.get("metadata", {})
                        title = meta.get("title", "Tài liệu tham chiếu")
                        source_name = meta.get("source", "Tài liệu hệ thống")
                        doc_type = meta.get("doc_type", "legal")
                        score = src.get("score", 0.0)
                        chunk_text = src.get("content", "").strip()

                        badge_class = "badge-legal" if doc_type == "legal" else "badge-news"
                        type_label = "Văn bản luật" if doc_type == "legal" else "Bài viết hướng dẫn"

                        st.markdown(
                            f"""
                            <div class="source-card">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                    <strong>#{idx}. {html.escape(title)}</strong>
                                    <div>
                                        <span class="badge-pill {badge_class}">{type_label}</span>
                                        <span class="badge-pill badge-hybrid">Score: {score:.4f}</span>
                                    </div>
                                </div>
                                <small style="color: #64748b;">Nguồn: <code>{html.escape(source_name)}</code></small>
                                <div style="margin-top: 8px; font-size: 0.88rem; line-height: 1.5; color: #334155; background: rgba(0,0,0,0.02); padding: 8px; border-radius: 6px;">
                                    {html.escape(chunk_text[:350])}{'...' if len(chunk_text) > 350 else ''}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

    # 3. Lưu vào session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer_text,
        "sources": sources,
        "retrieval_source": retrieval_type,
    })

    if selected_chip:
        st.rerun()
