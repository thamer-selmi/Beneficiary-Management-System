from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display


def arabic_text(text):
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)


def setup_arabic_font():
    pdfmetrics.registerFont(TTFont("Arabic", "arial.ttf"))


def draw_header(c, width, height):
    header_y = height - 40
    arabic_font = "Arabic"

    # الجهة اليمنى
    c.setFont(arabic_font, 14)
    c.drawRightString(width - 25, header_y, arabic_text("الجمهورية التونسية"))

    c.setFont(arabic_font, 12)
    c.drawRightString(
        width - 25, header_y - 20,
        arabic_text("وزارة الفلاحة والموارد المائية والصيد البحري")
    )
    c.drawRightString(
        width - 25, header_y - 38,
        arabic_text("المندوبية الجهوية للتنمية الفلاحية بالقيروان")
    )

    c.setFont(arabic_font, 11)
    c.drawRightString(
        width - 25, header_y - 56,
        arabic_text("مجمع التنمية في القطاع الفلاحي «الإنقاذ»")
    )

    # الجهة اليسرى
    today = datetime.now().strftime("%Y/%m/%d")
    c.setFont(arabic_font, 11)
    c.drawString(25, header_y, arabic_text(f"القيروان في: {today}"))
    c.drawString(25, header_y - 20, arabic_text("معتمدية منزل مهيري – 3114"))
    c.drawString(25, header_y - 38, arabic_text("قرية السوالم – طريق حفوز"))
    c.drawString(25, header_y - 56, arabic_text("بجانب دار السبوعي"))

    # خط فاصل
    c.setLineWidth(1)
    c.line(25, header_y - 75, width - 25, header_y - 75)


# =========================
# Footer + ترقيم
# =========================
def draw_footer(c, width, page_num):
    c.setFont("Arabic", 9)
    c.drawCentredString(
        width / 2, 25,
        arabic_text(f"الصفحة {page_num}")
    )


# =========================
# جدول الاستهلاك
# =========================
def draw_table(c, width, start_y, data):
    arabic_font = "Arabic"
    row_height = 22
    col_widths = [40, 150, 90, 90, 90]
    x_positions = [
        width - 25,
        width - 25 - col_widths[0],
        width - 25 - sum(col_widths[:2]),
        width - 25 - sum(col_widths[:3]),
        width - 25 - sum(col_widths[:4]),
    ]

    headers = ["رقم", "اسم المنتفع", "رقم العداد", "الاستهلاك (م³)", "المبلغ (د.ت)"]

    c.setFont(arabic_font, 11)
    c.setFillColor(colors.lightgrey)
    c.rect(25, start_y - row_height, width - 50, row_height, fill=1)

    c.setFillColor(colors.black)
    for i, h in enumerate(headers):
        c.drawRightString(x_positions[i] - 5, start_y - 16, arabic_text(h))

    y = start_y - row_height

    for idx, row in enumerate(data, start=1):
        y -= row_height
        if y < 80:
            c.showPage()
            draw_header(c, width, A4[1])
            y = A4[1] - 160

        values = [
            idx,
            row["name"],
            row["meter"],
            row["consumption"],
            row["amount"]
        ]

        c.rect(25, y, width - 50, row_height, fill=0)

        for i, val in enumerate(values):
            c.drawRightString(
                x_positions[i] - 5,
                y + 6,
                arabic_text(val)
            )


# =========================
# إنشاء التقرير
# =========================
def generate_consumption_report(data, filename="consumption_report.pdf"):
    setup_arabic_font()

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    page_num = 1

    draw_header(c, width, height)

    # عنوان التقرير
    c.setFont("Arabic", 16)
    c.drawCentredString(
        width / 2, height - 140,
        arabic_text("تقرير الاستهلاك")
    )

    draw_table(c, width, height - 180, data)
    draw_footer(c, width, page_num)

    c.save()
    print("تم إنشاء التقرير بنجاح:", filename)


# =========================
# مثال بيانات
# =========================
if __name__ == "__main__":
    sample_data = [
        {"name": "محمد علي", "meter": "12345", "consumption": 45, "amount": 67.5},
        {"name": "أحمد صالح", "meter": "67890", "consumption": 30, "amount": 45.0},
        {"name": "سالم بن عمر", "meter": "11223", "consumption": 60, "amount": 90.0},
    ]

    generate_consumption_report(sample_data)
