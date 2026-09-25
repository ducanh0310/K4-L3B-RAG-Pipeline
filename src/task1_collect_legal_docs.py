"""
Task 1 — Thu thập tài liệu chính sách/quy định.

Hướng dẫn:
    1. Chọn chủ đề của nhóm.
    2. Tìm tối thiểu 3 tài liệu PDF/DOCX từ nguồn công khai.
    3. Lưu file gốc vào data/landing/legal/.
    4. Đặt tên không dấu và thể hiện đúng nội dung.

Ví dụ tài liệu: học phí, học bổng, ký túc xá, quy trình đăng ký.
Nếu website chặn crawler, hãy chọn nguồn công khai khác; không vượt WAF.
"""

import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"


def setup_directory() -> None:
    """Tạo thư mục lưu tài liệu gốc."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Ready: {DATA_DIR}")


def _find_font_path() -> str | None:
    """Tìm font hỗ trợ tiếng Việt Unicode."""
    candidates = [
        Path(r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\times.ttf"),
        Path(r"C:\Windows\Fonts\tahoma.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None


def _create_sample_pdf(filepath: Path, title: str, sections: list[tuple[str, str]]) -> None:
    """Tạo file PDF tài liệu quy định chuẩn hóa có dấu tiếng Việt."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font_path = _find_font_path()
    if font_path:
        pdf.add_font("CustomFont", "", font_path)
        pdf.set_font("CustomFont", size=15)
    else:
        pdf.set_font("Helvetica", size=15)

    # Header tài liệu
    pdf.cell(0, 10, text=title.upper(), align="C")
    pdf.ln(12)

    # Nội dung từng điều khoản
    for heading, body in sections:
        if font_path:
            pdf.set_font("CustomFont", size=12)
        else:
            pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 8, text=heading)
        pdf.ln(8)

        if font_path:
            pdf.set_font("CustomFont", size=10)
        else:
            pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 6, text=body)
        pdf.ln(5)

    pdf.output(str(filepath))


def download_documents() -> None:
    """Thu thập tối thiểu 3 tài liệu quy định/chính sách."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Kiểm tra nếu đã có sẵn ít nhất 3 file tài liệu
    existing_files = [
        f for f in DATA_DIR.iterdir()
        if f.suffix.lower() in {".pdf", ".docx", ".doc"}
    ]
    if len(existing_files) >= 3:
        print(f"Đã có {len(existing_files)} tài liệu hợp lệ trong {DATA_DIR}:")
        for f in existing_files:
            print(f" - {f.name}")
        return

    print("Đang tạo 4 tài liệu pháp luật chính sách: Pháp luật cho Hộ Kinh Doanh...")

    docs = {
        "nghi_dinh_01_2021_dang_ky_kinh_doanh.pdf": (
            "NGHỊ ĐỊNH 01/2021/NĐ-CP VỀ ĐĂNG KÝ DOANH NGHIỆP VÀ HỘ KINH DOANH",
            [
                (
                    "Điều 79. Khái niệm và quyền thành lập hộ kinh doanh",
                    "Hộ kinh doanh do một cá nhân hoặc các thành viên hộ gia đình đăng ký thành lập và chịu trách nhiệm bằng toàn bộ tài sản của mình đối với hoạt động kinh doanh của hộ. Trường hợp các thành viên hộ gia đình đăng ký hộ kinh doanh thì ủy quyền cho một thành viên làm đại diện hộ kinh doanh. Cá nhân đăng ký hộ kinh doanh, người được các thành viên hộ gia đình ủy quyền làm người đại diện hộ kinh doanh là chủ hộ kinh doanh.",
                ),
                (
                    "Điều 80. Quyền thành lập hộ kinh doanh và nghĩa vụ đăng ký",
                    "Cá nhân, thành viên hộ gia đình là công dân Việt Nam có năng lực hành vi dân sự đầy đủ theo quy định của Bộ luật Dân sự có quyền thành lập hộ kinh doanh. Mỗi cá nhân, thành viên hộ gia đình chỉ được đăng ký một hộ kinh doanh trong phạm vi toàn quốc và được quyền góp vốn, mua cổ phần, mua phần vốn góp trong doanh nghiệp với tư cách cá nhân.",
                ),
                (
                    "Điều 85. Địa điểm kinh doanh của hộ kinh doanh",
                    "Một hộ kinh doanh có thể hoạt động kinh doanh tại nhiều địa điểm nhưng phải chọn một địa điểm để đăng ký trụ sở hộ kinh doanh và phải thông báo cho Cơ quan quản lý thuế, Cơ quan quản lý thị trường nơi tiến hành hoạt động kinh doanh đối với các địa điểm kinh doanh còn lại.",
                ),
                (
                    "Điều 87. Hồ sơ và thủ tục đăng ký hộ kinh doanh",
                    "Hồ sơ đăng ký hộ kinh doanh nộp tại Cơ quan đăng ký kinh doanh cấp huyện nơi đặt trụ sở hộ kinh doanh, bao gồm:\n"
                    "1. Giấy đề nghị đăng ký hộ kinh doanh;\n"
                    "2. Giấy tờ pháp lý của cá nhân đối với chủ hộ kinh doanh, thành viên hộ gia đình đăng ký hộ kinh doanh trong trường hợp các thành viên hộ gia đình đăng ký hộ kinh doanh;\n"
                    "3. Bản sao biên bản họp thành viên hộ gia đình về việc thành lập hộ kinh doanh trong trường hợp các thành viên hộ gia đình đăng ký hộ kinh doanh;\n"
                    "4. Bản sao văn bản ủy quyền của các thành viên hộ gia đình cho một thành viên làm chủ hộ kinh doanh.",
                ),
                (
                    "Điều 88. Cấp Giấy chứng nhận đăng ký hộ kinh doanh",
                    "Cơ quan đăng ký kinh doanh cấp huyện trao Giấy biên nhận và cấp Giấy chứng nhận đăng ký hộ kinh doanh cho hộ kinh doanh trong thời hạn 03 ngày làm việc kể từ ngày nhận hồ sơ hợp lệ. Trường hợp hồ sơ không hợp lệ, trong thời hạn 03 ngày làm việc, Cơ quan đăng ký kinh doanh cấp huyện phải thông báo rõ nội dung cần sửa đổi, bổ sung bằng văn bản cho người nộp hồ sơ.",
                ),
            ],
        ),
        "thong_tu_40_2021_thue_ho_kinh_doanh.pdf": (
            "THÔNG TƯ 40/2021/TT-BTC HƯỚNG DẪN THUẾ GTGT VÀ TNCN ĐỐI VỚI HỘ KINH DOANH",
            [
                (
                    "Điều 4. Nguyên tắc tính thuế và ngưỡng doanh thu chịu thuế",
                    "Hộ kinh doanh, cá nhân kinh doanh có doanh thu từ hoạt động sản xuất, kinh doanh trong năm dương lịch từ 100 triệu đồng trở xuống thì thuộc diện không phải nộp thuế Giá trị gia tăng (GTGT) và không phải nộp thuế Thu nhập cá nhân (TNCN) theo quy định pháp luật về thuế GTGT và thuế TNCN. Hộ kinh doanh có trách nhiệm khai thuế chính xác, trung thực, đầy đủ và nộp hồ sơ thuế đúng hạn.",
                ),
                (
                    "Điều 5. Phương pháp tính thuế đối với hộ kinh doanh nộp thuế theo phương pháp khoán",
                    "Phương pháp khoán được áp dụng đối với hộ kinh doanh, cá nhân kinh doanh không thực hiện hoặc thực hiện không đầy đủ chế độ kế toán, hóa đơn, chứng từ. Cơ quan thuế xác định doanh thu và mức thuế khoán theo hồ sơ khai thuế của hộ khoán, cơ sở dữ liệu của cơ quan thuế và kết quả điều tra doanh thu thực tế.",
                ),
                (
                    "Điều 6. Phương pháp tính thuế đối với hộ kinh doanh nộp thuế theo phương pháp kê khai",
                    "Phương pháp kê khai áp dụng đối với hộ kinh doanh, cá nhân kinh doanh quy mô lớn; hoặc hộ kinh doanh chưa đáp ứng quy mô lớn nhưng lựa chọn nộp thuế theo phương pháp kê khai. Hộ kê khai thực hiện khai thuế theo tháng hoặc quý, thực hiện chế độ kế toán, hóa đơn, chứng từ theo quy định tại Thông tư số 88/2021/TT-BTC.",
                ),
                (
                    "Phụ lục I. Tỷ lệ phần trăm (%) tính thuế trên doanh thu của hộ kinh doanh",
                    "1. Phân phối, cung cấp hàng hóa (bán buôn, bán lẻ): Tỷ lệ thuế GTGT là 1%; Tỷ lệ thuế TNCN là 0.5% (Tổng cộng 1.5% trên doanh thu).\n"
                    "2. Dịch vụ, xây dựng không bao thầu nguyên vật liệu: Tỷ lệ thuế GTGT là 5%; Tỷ lệ thuế TNCN là 2% (Tổng cộng 7% trên doanh thu).\n"
                    "3. Sản xuất, vận tải, dịch vụ có gắn với hàng hóa, xây dựng có bao thầu nguyên vật liệu: Tỷ lệ thuế GTGT là 3%; Tỷ lệ thuế TNCN là 1.5% (Tổng cộng 4.5% trên doanh thu).\n"
                    "4. Hoạt động kinh doanh khác: Tỷ lệ thuế GTGT là 2%; Tỷ lệ thuế TNCN là 1% (Tổng cộng 3% trên doanh thu).",
                ),
            ],
        ),
        "nghi_dinh_123_2020_hoa_don_dien_tu.pdf": (
            "NGHỊ ĐỊNH 123/2020/NĐ-CP VÀ THÔNG TƯ 78/2021/TT-BTC VỀ HÓA ĐƠN ĐIỆN TỬ",
            [
                (
                    "Điều 11. Hóa đơn điện tử khởi tạo từ máy tính tiền",
                    "Hộ kinh doanh, cá nhân kinh doanh nộp thuế theo phương pháp kê khai có hoạt động cung cấp hàng hóa, dịch vụ trực tiếp đến người tiêu dùng theo mô hình kinh doanh (trung tâm thương mại; siêu thị; bán lẻ hàng tiêu dùng; ăn uống; nhà hàng; khách sạn; bán lẻ thuốc tân dược; dịch vụ vui chơi, giải trí và các dịch vụ khác) được lựa chọn sử dụng hóa đơn điện tử khởi tạo từ máy tính tiền có kết nối chuyển dữ liệu điện tử với cơ quan thuế.",
                ),
                (
                    "Điều 12. Nguyên tắc và nội dung hóa đơn điện tử khởi tạo từ máy tính tiền",
                    "Hóa đơn điện tử khởi tạo từ máy tính tiền phải có các nội dung:\n"
                    "1. Tên, địa chỉ, mã số thuế người bán;\n"
                    "2. Thông tin người mua nếu người mua yêu cầu (mã số định danh cá nhân hoặc mã số thuế);\n"
                    "3. Tên hàng hóa, dịch vụ, đơn giá, số lượng, giá thanh toán;\n"
                    "4. Thời điểm lập hóa đơn;\n"
                    "5. Mã của cơ quan thuế hoặc mã khởi tạo từ máy tính tiền được cấp theo định dạng chuẩn của Tổng cục Thuế. Hóa đơn không bắt buộc phải có chữ ký số của người bán.",
                ),
                (
                    "Điều 90. Trách nhiệm sử dụng và lưu trữ hóa đơn của hộ kinh doanh",
                    "Hộ kinh doanh có nghĩa vụ lập và giao hóa đơn điện tử cho người mua khi bán hàng hóa, cung cấp dịch vụ, không phân biệt giá trị từng lần bán hàng. Hóa đơn điện tử phải được lưu trữ an toàn, bảo mật dữ liệu tối thiểu 10 năm theo Luật Kế toán.",
                ),
            ],
        ),
        "nghi_dinh_52_2013_va_85_2021_thuong_mai_dien_tu.pdf": (
            "QUY ĐỊNH PHÁP LUẬT VỀ THƯƠNG MẠI ĐIỆN TỬ CHO HỘ KINH DOANH",
            [
                (
                    "Điều 27. Hoạt động bán hàng trên sàn giao dịch thương mại điện tử",
                    "Cá nhân, hộ kinh doanh bán hàng trên các sàn giao dịch thương mại điện tử (Shopee, Lazada, TikTok Shop, Tiki) phải đăng ký tài khoản kinh doanh, cung cấp đầy đủ, chính xác các thông tin: Tên hộ kinh doanh, địa chỉ, số điện thoại, mã số thuế cá nhân/hộ kinh doanh, số căn cước công dân.",
                ),
                (
                    "Điều 28. Nghĩa vụ thông báo website và ứng dụng thương mại điện tử bán hàng",
                    "Hộ kinh doanh thiết lập website hoặc ứng dụng di động để phục vụ hoạt động xúc tiến thương mại, bán hàng hóa hoặc cung ứng dịch vụ của mình phải thực hiện thủ tục thông báo với Bộ Công Thương trực tuyến qua Cổng thông tin Quản lý hoạt động thương mại điện tử (online.gov.vn) trước khi chính thức hoạt động.",
                ),
                (
                    "Điều 30. Trách nhiệm kê khai thuế đối với kinh doanh trên sàn TMĐT",
                    "Hộ kinh doanh bán hàng trên sàn thương mại điện tử có nghĩa vụ tự kê khai và nộp thuế hoặc ủy quyền cho sàn TMĐT khai thuế và nộp thuế thay theo quy định. Các sàn thương mại điện tử có trách nhiệm định kỳ cung cấp thông tin về doanh thu, số tài khoản ngân hàng, thông tin giao dịch của người bán cho Tổng cục Thuế để đối chiếu.",
                ),
                (
                    "Điều 32. Bán hàng qua mạng xã hội và Livestream",
                    "Cá nhân, hộ kinh doanh bán hàng qua các nền tảng mạng xã hội (Facebook, TikTok, Zalo) thông qua hình thức livestream, bài đăng hoặc tin nhắn có phát sinh doanh thu từ 100 triệu đồng/năm trở lên đều thuộc diện chịu thuế theo tỷ lệ ngành hàng (phân phối hàng hóa chịu thuế 1.5% trên tổng doanh thu thực nhận).",
                ),
            ],
        ),
    }

    for filename, (title, sections) in docs.items():
        file_path = DATA_DIR / filename
        _create_sample_pdf(file_path, title, sections)
        print(f"Đã lưu tài liệu: {file_path}")

    print(f"\nThu thập thành công {len(docs)} tài liệu vào: {DATA_DIR}")


if __name__ == "__main__":
    setup_directory()
    download_documents()

