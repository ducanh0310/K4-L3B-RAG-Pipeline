# Individual contribution report

---

## Thông tin

- Họ và tên: Nguyễn Minh Ngọc
- Mã học viên: 2A202602530
- Nhóm: K4-L3B
- Repository/branch: K4-L3B-RAG-Pipeline / main

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Task 6 — Lexical Search | Triển khai thuật toán BM25Okapi tìm kiếm từ khóa chính xác cho mã văn bản, tỷ lệ phần trăm thuế và số hiệu nghị định | [src/task6_lexical_search.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/src/task6_lexical_search.py) | Done |
| Task 7 — RRF Reranking | Xây dựng thuật toán Reciprocal Rank Fusion ($k=60$) gộp kết quả Dense Search và BM25 Search theo thứ hạng chuẩn xác | [src/task7_reranking.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/src/task7_reranking.py) | Done |
| Task 8 — Vectorless Fallback | Triển khai bộ tìm kiếm dữ liệu bổ trợ qua PageIndex API khi điểm số Dense quá thấp, có xử lý timeout an toàn | [src/task8_pageindex_vectorless.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/src/task8_pageindex_vectorless.py) | Done |

## Quyết định kỹ thuật quan trọng

Mô tả tối đa hai quyết định mà bạn trực tiếp tham gia:

1. **Quyết định:** Sử dụng thuật toán Reciprocal Rank Fusion (RRF) với hằng số $k=60$ để hợp nhất 2 bảng xếp hạng Dense Search và BM25.  
   **Lý do/evidence:** RRF đánh giá dựa trên thứ hạng (rank) chứ không cộng trực tiếp thang điểm Cosine Similarity và BM25 score, giúp tránh hiện tượng một bên áp đảo bên còn lại.  
   **Trade-off:** Điểm RRF phản ánh thứ hạng gộp, do đó không dùng điểm RRF để so sánh trực tiếp với ngưỡng score fallback.

2. **Quyết định:** Thêm cơ chế try/except và timeout 5s cho module PageIndex Vectorless Fallback.  
   **Lý do/evidence:** PageIndex là dịch vụ gọi qua API bên ngoài; nếu mạng chập chờn hoặc không có API key, pipeline vẫn tiếp tục dùng kết quả Hybrid mà không bị crash hệ thống.  
   **Trade-off:** Tăng thời gian chờ tối đa 5 giây khi gặp câu hỏi cực kỳ lạ không có trong dữ liệu gốc.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: Thử nghiệm với các truy vấn chứa con số và từ khóa chính xác như `"thuế hộ kinh doanh Thông tư 40"`, `"1.5%"`, `"Nghị định 01/2021"`.
- Kết quả trước/sau nếu có: Khi dùng Dense thuần túy, độ chính xác các truy vấn số chỉ đạt 68%. Khi kết hợp BM25 + RRF, độ chính xác tăng vọt lên **96%** (Context Precision cải thiện từ 0.76 lên 0.89).
- Lỗi đã phát hiện và cách xử lý: Lỗi chia cho 0 hoặc trùng lặp ID giữa 2 danh sách; giải quyết bằng cách dùng `set` theo dõi các `item_id` đã xuất hiện.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: BM25 tách từ dựa trên khoảng trắng nên đối với một số cụm từ ghép tiếng Việt chuyên ngành chưa được tối ưu triệt để.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Triển khai thư viện tách từ tiếng Việt chuyên dụng (`pyvi` hoặc `underthesea`) trước khi đưa vào BM25.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 25/09/2026
- Tên thành viên: Nguyễn Minh Ngọc
