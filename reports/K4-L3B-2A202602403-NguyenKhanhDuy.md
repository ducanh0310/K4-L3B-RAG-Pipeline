# Individual contribution report

---

## Thông tin

- Họ và tên: Nguyễn Khánh Duy
- Mã học viên: 2A202602403
- Nhóm: K4-L3B
- Repository/branch: K4-L3B-RAG-Pipeline / main

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Task 4 — Chunking & Indexing | Xây dựng chiến lược `RecursiveCharacterTextSplitter` (chunk_size=500, overlap=50), nhúng vector chuẩn hóa L2 và upsert vào ChromaDB với cosine distance | [src/task4_chunking_indexing.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/src/task4_chunking_indexing.py) | Done |
| Task 5 — Semantic Search | Triển khai mô hình tìm kiếm ngữ nghĩa Dense Search trên ChromaDB, quy đổi distance sang similarity score (`1.0 - distance`), sắp xếp kết quả chuẩn | [src/task5_semantic_search.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/src/task5_semantic_search.py) | Done |
| Unit Testing | Viết toàn bộ hệ thống test hợp đồng dữ liệu và kiểm thử chấp nhận cho pipeline | [tests/test_contracts.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/tests/test_contracts.py), [tests/test_acceptance.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/tests/test_acceptance.py) | Done |

## Quyết định kỹ thuật quan trọng

Mô tả tối đa hai quyết định mà bạn trực tiếp tham gia:

1. **Quyết định:** Chọn kích thước `chunk_size = 500` ký tự và `chunk_overlap = 50` ký tự với separators ưu tiên ngắt theo đoạn văn (`\n\n`, `\n`).  
   **Lý do/evidence:** Đảm bảo mỗi chunk giữ nguyên vẹn nội dung của từng Điều/Khoản trong văn bản pháp luật, tránh trường hợp ngắt giữa chừng một điều khoản thuế quan trọng.  
   **Trade-off:** Kích thước chunk vừa phải giúp ngữ cảnh tập trung nhưng cần overlap hợp lý để không mất liên kết giữa các ý.

2. **Quyết định:** Sử dụng không gian lưu trữ Cosine Distance (`hnsw:space: cosine`) trong ChromaDB và chuẩn hóa L2 vector embedding.  
   **Lý do/evidence:** Giúp điểm số tương đồng (similarity score = `1.0 - distance`) nằm trong khoảng `[0.0, 1.0]`, dễ dàng thiết lập ngưỡng lọc (threshold) cho pipeline.  
   **Trade-off:** Cần xử lý cẩn thận các giá trị biên để score không bị âm khi distance > 1.0.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: `pytest tests/test_contracts.py tests/test_acceptance.py` và thử nghiệm truy vấn "thủ tục đăng ký hộ kinh doanh".
- Kết quả trước/sau nếu có: 100% test pass. Hệ thống truy xuất chính xác các chunk điều khoản từ Nghị định 01/2021 với điểm số tương đồng > 0.85.
- Lỗi đã phát hiện và cách xử lý: Khắc phục lỗi ChromaDB trả về đường dẫn URL `None` bằng cách chuyển thành chuỗi rỗng `""` trước khi lưu vào metadata của ChromaDB.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Tìm kiếm Dense bằng vector đơn thuần đôi khi bỏ sót các câu hỏi chứa chính xác tên con số thuế (như "1.5%", "5%").
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Thử nghiệm bổ sung mô hình embedding chuyên sâu cho tiếng Việt (`bkai-foundation-models/vietnamese-bi-encoder`).

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 25/09/2026
- Tên thành viên: Nguyễn Khánh Duy
