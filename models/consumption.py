import os
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black, white

import arabic_reshaper
from bidi.algorithm import get_display

from backend.documents_services import Documents
from backend.farmers_services import Farmers


def setup_arabic_font():
    """إعداد الخط العربي"""
    font_path = Path("fonts")
    regular_font = font_path / "arial.ttf"
    bold_font = font_path / "arial_bold.ttf"

    if not regular_font.exists():
        raise FileNotFoundError(f"الخط غير موجود: {regular_font}")
    if not bold_font.exists():
        raise FileNotFoundError(f"الخط غير موجود: {bold_font}")

    pdfmetrics.registerFont(TTFont("Arial", str(regular_font)))
    pdfmetrics.registerFont(TTFont("Arial_bold", str(bold_font)))
    return "Arial", "Arial_bold"


def arabic_text(text):
    """معالجة النص العربي للعرض داخل PDF"""
    if text is None:
        return ""
    text = str(text)
    if text == "":
        return ""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)


def create_consumption_pdf():
    folder_path = Path("دفتر_الاستهلاك")
    folder_path.mkdir(parents=True, exist_ok=True)

    file_date = datetime.now().strftime("%Y_%m_%d")
    output_path = folder_path / f"{file_date}.pdf"

    arabic_font, arabic_bold = setup_arabic_font()

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    PAGE_NUMBER = 1
    BOTTOM_MARGIN = 70

    headers = [
        "المبلغ الجملي",
        "سعر م3",
        "الاستهلاك",
        "العداد الجديد",
        "العداد القديم",
        "رقم العداد",
        "ر ب ت و",
        "الاسم و اللقب",
    ]

    start_x = 30
    col_widths = [60, 60, 60, 60, 60, 60, 60, 100]
    row_height = 25

    def draw_page_number():
        c.setFont(arabic_font, 10)
        c.drawCentredString(width / 2, 30, arabic_text(str(PAGE_NUMBER)))

    def draw_table_header(y):
        c.setFont(arabic_bold, 13)

        x = start_x
        c.setLineWidth(1)

        # الإطار العلوي
        c.line(start_x, y + row_height, start_x + sum(col_widths), y + row_height)

        for i, header in enumerate(headers):
            c.drawCentredString(
                x + col_widths[i] / 2,
                y + 7,
                arabic_text(header)
            )
            c.line(x, y, x, y + row_height)
            x += col_widths[i]

        c.line(x, y, x, y + row_height)

        c.setLineWidth(1.5)
        c.line(start_x, y, x, y)
        c.setLineWidth(1)

        return y - row_height

    def start_new_page():
        nonlocal PAGE_NUMBER
        draw_page_number()
        c.showPage()
        PAGE_NUMBER += 1
        c.setFillColor(white)
        c.rect(0, 0, width, height, fill=1)
        c.setFillColor(black)

    # ===== الصفحة الأولى =====
    c.setFillColor(white)
    c.rect(0, 0, width, height, fill=1)
    c.setFillColor(black)

    header_y = height - 40

    c.setFont(arabic_font, 14)
    c.drawRightString(width - 20, header_y, arabic_text("الجمهورية التونسية"))
    c.drawRightString(width - 20, header_y - 20, arabic_text("وزارة الفلاحة والموارد المائية والصيد البحري"))
    c.drawRightString(width - 20, header_y - 40, arabic_text("المندوبية الجهوية للتنمية الفلاحية بالقيروان"))
    c.drawRightString(width - 20, header_y - 60, arabic_text("مجمع التنمية في القطاع الفلاحي 'الانقاذ'"))

    today_str = datetime.now().strftime("%Y/%m/%d")
    c.drawString(20, header_y, arabic_text(f"منزل مهيري في {today_str}"))
    c.drawString(20, header_y - 20, arabic_text("قرية السوالم طريق"))
    c.drawString(20, header_y - 40, arabic_text("نصر الله - حفوز"))
    c.drawString(20, header_y - 60, arabic_text("بجانب دار السبوعي"))

    # مسار الصورة
    logo_path = r"img\logo2.png"
    img_w = 120
    img_h = 100

    # مكان الصورة (على يمين العنوان)
    img_x = width  / 2 - 80
    img_y = header_y - 75

    # رسم الصورة
    c.drawImage(logo_path, img_x, img_y, width=img_w, height=img_h, mask='auto')

    c.line(10, header_y - 80, width - 10, header_y - 80)

    title_y = header_y - 130
    c.setFont(arabic_bold, 22)
    c.drawCentredString(
        width / 2,
        title_y,
        arabic_text("دفتر متابعة الاستهلاك و الفوترة لكل المنتفعين")
    )

    c.setFont(arabic_font, 18)
    date_info = Documents.get_date()
    if isinstance(date_info, (list, tuple)) and len(date_info) > 0:
        start_date = date_info[0]
        end_date = date_info[1]
    else:
        start_date = ""
        end_date = ""

    c.drawCentredString(
        width / 2,
        title_y - 30,
        arabic_text(f"من {start_date} الى {end_date}")
    )

    # ===== جدول البيانات =====
    table_y = title_y - 70
    y = draw_table_header(table_y)

    data = Documents.for_dafter()
    c.setFont(arabic_font, 10)

    for row in data:
        if y < BOTTOM_MARGIN:
            start_new_page()
            y = height - 60
            y = draw_table_header(y)
            c.setFont(arabic_font, 10)

        x = start_x

        for i, val in enumerate(row):
            c.drawCentredString(
                x + col_widths[i] / 2,
                y + 7,
                arabic_text(val)
            )
            c.line(x, y, x, y + row_height)
            x += col_widths[i]

        c.line(x, y, x, y + row_height)
        c.line(start_x, y, x, y)
        y -= row_height

    # ===== جدول الملخص =====
    if y < 150:
        start_new_page()
        y = height - 50
        
    y = y - 40
    summary_x = start_x + 45
    summary_widths = [150, 300]
    summary_height = 35

    values = Farmers.for_daftr()

    total_users = len(Documents.get_unique_cins())

    total_consumption = values[0] if isinstance(values, (list, tuple)) and len(values) > 0 else 0
    total_amount = values[1] if isinstance(values, (list, tuple)) and len(values) > 1 else 0

    summary_data = [
        ("اجمالي المنتفعين", total_users),
        ("اجمالي الكميات المستهلكة", f"{total_consumption} م3"),
        ("اجمالي المبالغ الجملية", f"{total_amount} د"),
    ]

    for label, value in summary_data:
        x = summary_x

        c.rect(x, y, sum(summary_widths), summary_height)
        c.line(x + summary_widths[0], y, x + summary_widths[0], y + summary_height)

        c.setFont(arabic_bold, 14)
        c.drawCentredString(
            x + summary_widths[0] + summary_widths[1] / 2,
            y + 10,
            arabic_text(label)
        )

        c.setFont(arabic_font, 14)
        c.drawCentredString(
            x + summary_widths[0] / 2,
            y + 10,
            arabic_text(value)
        )

        y -= summary_height

    # ===== التوقيعات =====
    if y < 150:
        start_new_page()
        y = height - 50

    sig_y = y - 30
    c.setFont(arabic_font, 14)
    c.drawRightString(width - 40, sig_y, arabic_text("امضاء المدير الفني"))
    c.drawCentredString(width / 2, sig_y, arabic_text("امضاء أمين المال"))
    c.drawString(40, sig_y, arabic_text("امضاء رئيس المجمع"))

    draw_page_number()
    c.save()

    try:
        os.startfile(str(output_path))
    except Exception:
        pass

    return str(output_path)