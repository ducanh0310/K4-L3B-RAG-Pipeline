# Individual contribution report

---

## Thông tin

- Họ và tên: Nguyễn Đức Anh
- Mã học viên: 2A202602888
- Nhóm: K4-L3B
- Repository/branch: K4-L3B-RAG-Pipeline / main

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Data Contracts | Thiết kế định nghĩa TypedDict và hàm validate chuẩn cho Document, Chunk, SearchResult, GenerationResult | [src/contracts.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/src/contracts.py) | Done |
| Task 1 — Collect Legal Docs | Xây dựng module thu thập tài liệu pháp luật (PDF/DOCX), sinh file PDF chuẩn hóa tiếng Việt hỗ trợ Unicode | [src/task1_collect_legal_docs.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/src/task1_collect_legal_docs.py) | Done |
| Task 2 — Crawl News | Thu thập và cấu trúc hóa các bài viết hướng dẫn thực tế từ Dịch vụ công quốc gia, Thư viện pháp luật, Tổng cục Thuế | [src/task2_crawl_news.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/src/task2_crawl_news.py) | Done |
| Task 3 — Convert Markdown | Chuẩn hóa toàn bộ dữ liệu thô (PDF, DOCX, JSON) sang định dạng Markdown đồng nhất có lưu giữ header metadata | [src/task3_convert_markdown.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/src/task3_convert_markdown.py) | Done |

## Quyết định kỹ thuật quan trọng

Mô tả tối đa hai quyết định mà bạn trực tiếp tham gia:

1. **Quyết định:** Thống nhất dữ liệu đầu vào thông qua Data Contracts nghiêm ngặt (`TypedDict` + Validation Functions).  
   **Lý do/evidence:** Đảm bảo toàn bộ các module từ Chunking, Search đến Generation hoạt động nhất quán, loại bỏ lỗi thiếu trường metadata hoặc sai kiểu dữ liệu khi truyền giữa các bước của pipeline.  
   **Trade-off:** Tăng khối lượng code kiểm định ban đầu nhưng giúp pipeline chạy ổn định 100%, không bị crash giữa chừng.

2. **Quyết định:** Tự động sinh tài liệu PDF chuẩn hóa có dấu bằng thư viện `FPDF` kết hợp font Unicode hệ thống (`Arial`/`Times New Roman`).  
   **Lý do/evidence:** Khắc phục lỗi font tiếng Việt phổ biến khi parse PDF thô, đảm bảo văn bản pháp luật chứa đầy đủ dấu tiếng Việt chuẩn xác cho mô hình đọc hiểu.  
   **Trade-off:** Cần kiểm tra đường dẫn font tương thích đa nền tảng (Windows/Linux/macOS).

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: `pytest tests/test_contracts.py` và chạy thử nghiệm `python -m src.task3_convert_markdown`.
- Kết quả trước/sau nếu có: Chuyển đổi thành công 100% tài liệu pháp lý (Nghị định 01/2021, Thông tư 40/2021, Nghị định 123/2020) và bài viết tin tức sang thư mục `data/standardized/` dạng Markdown chuẩn.
- Lỗi đã phát hiện và cách xử lý: Lỗi ngắt câu và mã hóa UTF-8 trên Windows PowerShell; xử lý bằng cách cấu hình `sys.stdout.reconfigure(encoding="utf-8")`.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Tốc độ parse PDF thô phụ thuộc vào độ phức tạp của định dạng bảng biểu trong văn bản pháp luật.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Bổ sung bộ OCR tự động cho các tài liệu pháp lý dạng bản quét (scanned PDF).

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 25/09/2026
- Tên thành viên: Nguyễn Đức Anh
