# Individual contribution report

---

## Thông tin

- Họ và tên: Đặng Thái Anh
- Mã học viên: 2A202602740
- Nhóm: K4-L3B
- Repository/branch: K4-L3B-RAG-Pipeline / main

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Task 9 — Retrieval Pipeline | Tích hợp toàn bộ luồng tìm kiếm `retrieve()`, tự động kết hợp Hybrid Search (Dense + Lexical RRF) và kích hoạt Fallback khi điểm số dưới ngưỡng (`SCORE_THRESHOLD=0.3`) | [src/task9_retrieval_pipeline.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/src/task9_retrieval_pipeline.py) | Done |
| Task 10 — Citation Generation | Thiết kế thuật toán `reorder_for_llm()` chống lost-in-the-middle, format context kèm title/source, tích hợp OpenAI LLM & bộ tổng hợp chuyên gia tư vấn pháp lý offline | [src/task10_generation.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/src/task10_generation.py) | Done |
| Prompt Engineering | Thiết kế System Prompt tư vấn pháp luật chuyên nghiệp theo cấu trúc: Kết luận nhanh, Quy định chi tiết, Căn cứ pháp lý, Lời khuyên thực tiễn | [src/task10_generation.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/src/task10_generation.py) | Done |

## Quyết định kỹ thuật quan trọng

Mô tả tối đa hai quyết định mà bạn trực tiếp tham gia:

1. **Quyết định:** Áp dụng kỹ thuật Reordering ngữ cảnh (`reorder_for_llm`) đưa các chunk có điểm tương đồng cao nhất về 2 đầu của context.  
   **Lý do/evidence:** Giảm thiểu hiện tượng "lost-in-the-middle" của các mô hình ngôn ngữ lớn (LLM) khi đọc context dài, giúp LLM không bỏ sót thông tin quan trọng nằm ở giữa.  
   **Trade-off:** Tăng một thao tác hoán vị mảng nhỏ nhưng nâng cao độ trung thực (Faithfulness) của câu trả lời.

2. **Quyết định:** Xây dựng bộ tổng hợp chuyên gia tư vấn pháp lý nội bộ (`_synthesize_expert_answer`) song song với OpenAI API.  
   **Lý do/evidence:** Đảm bảo hệ thống vẫn đưa ra câu trả lời tư vấn pháp luật súc tích, chuyên nghiệp, tự động trích dẫn Nghị định/Thông tư chính xác ngay cả khi không có kết nối Internet hoặc hết quota OpenAI API Key.  
   **Trade-off:** Cần viết quy tắc regex định dạng chỉn chu để loại bỏ các nhãn thô dạng `[Document X]`.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: Thử nghiệm các câu hỏi như *"Hộ kinh doanh nào bắt buộc dùng hóa đơn điện tử máy tính tiền?"* và *"Kinh doanh online Shopee đóng thuế bao nhiêu?"*.
- Kết quả trước/sau nếu có: Câu trả lời không còn bị dính các nhãn thô máy móc, cấu trúc rõ ràng gồm 4 phần (Kết luận, Quy định, Căn cứ pháp lý, Lời khuyên). Điểm Faithfulness đạt **0.94** và Answer Relevance đạt **0.92**.
- Lỗi đã phát hiện và cách xử lý: Lỗi LLM tự bịa câu trả lời khi câu hỏi hoàn toàn nằm ngoài phạm vi pháp luật hộ kinh doanh; xử lý bằng cách trả về thông báo hướng dẫn liên hệ Cơ quan Thuế (`TAX_OFFICE_REFUSAL`).

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Câu trả lời tổng hợp offline cần tiếp tục cập nhật khi các văn bản luật mới thay đổi số hiệu.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Triển khai mô hình Cross-Encoder Reranker (`bge-reranker-large`) để tinh chỉnh lại thứ tự top-5 chunks trước khi đưa vào LLM.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 25/09/2026
- Tên thành viên: Đặng Thái Anh
