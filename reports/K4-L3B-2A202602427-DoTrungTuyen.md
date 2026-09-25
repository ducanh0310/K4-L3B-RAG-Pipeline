# Individual contribution report

---

## Thông tin

- Họ và tên: Đỗ Trung Tuyến
- Mã học viên: 2A202602427
- Nhóm: K4-L3B
- Repository/branch: K4-L3B-RAG-Pipeline / main

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Streamlit Application | Thiết kế giao diện ứng dụng web Chatbot AI tư vấn pháp luật hiện đại với Custom CSS, bộ câu hỏi nhanh chip buttons và hiển thị trích dẫn nguồn chi tiết | [app.py](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/app.py) | Done |
| Evaluation Framework | Xây dựng bộ dữ liệu kiểm thử chuẩn Golden Dataset (15 test cases) và thực hiện đánh giá A/B Testing giữa Dense Only và Hybrid Search | [group_project/evaluation/golden_dataset.json](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/group_project/evaluation/golden_dataset.json), [group_project/evaluation/RESULT.md](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/group_project/evaluation/RESULT.md) | Done |
| Benchmarking & Reports | Tổng hợp và phân tích 4 chỉ số Ragas (Faithfulness, Answer Relevance, Context Precision, Context Recall), đưa ra khuyến nghị cải tiến hệ thống | [reports/RESULT.md](file:///d:/LabCode/Afternoon/K4-L3B-RAG-Pipeline/reports/RESULT.md) | Done |

## Quyết định kỹ thuật quan trọng

Mô tả tối đa hai quyết định mà bạn trực tiếp tham gia:

1. **Quyết định:** Thiết kế giao diện Streamlit với thanh Sidebar cho phép tùy chỉnh linh hoạt các cấu hình RAG (Model, Provider, Top-K, Chế độ xem nguồn trích dẫn).  
   **Lý do/evidence:** Giúp người dùng và giảng viên dễ dàng kiểm thử so sánh trực tiếp kết quả giữa các chiến lược tìm kiếm ngay trên UI sản phẩm.  
   **Trade-off:** Cần quản lý state (`st.session_state`) cẩn thận để giao diện không bị load lại mất lịch sử trò chuyện.

2. **Quyết định:** Đánh giá A/B Testing dựa trên tập Golden Dataset gồm 15 ca kiểm thử bao phủ toàn bộ các chủ đề pháp lý cốt lõi của hộ kinh doanh (Đăng ký, thuế khoán, hóa đơn máy tính tiền, bán hàng e-commerce).  
   **Lý do/evidence:** Cung cấp bằng chứng thực nghiệm rõ ràng chứng minh chiến lược Hybrid + RRF vượt trội hơn Dense Search thuần túy (+17.1% Context Precision).  
   **Trade-off:** Tốn nhiều thời gian gán nhãn thủ công và kiểm tra chéo các câu hỏi - câu trả lời chuẩn.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: Khởi chạy ứng dụng bằng `streamlit run app.py` và đo đạc chỉ số với tập `golden_dataset.json`.
- Kết quả trước/sau nếu có:
  - **Faithfulness:** **0.94** (Đạt mục tiêu ≥ 0.85)
  - **Answer Relevance:** **0.92** (Đạt mục tiêu ≥ 0.85)
  - **Context Precision:** **0.89** (Cải thiện từ 0.76 của Dense Search)
  - **Context Recall:** **0.93** (Cải thiện từ 0.81 của Dense Search)
- Lỗi đã phát hiện và cách xử lý: Lỗi hiển thị nhãn HTML thô trên giao diện Streamlit; xử lý bằng hàm `sanitize_display()` và tùy biến CSS badge thẻ bài viết/tài liệu.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Độ trễ trung bình của mô hình Hybrid + RRF là 28ms (cao hơn 12ms của Dense thuần túy) nhưng đổi lại độ chính xác cao hơn rõ rệt.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Bổ sung tính năng xuất báo cáo tư vấn pháp lý dạng file PDF trực tiếp cho người dùng từ giao diện Streamlit.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 25/09/2026
- Tên thành viên: Đỗ Trung Tuyến
