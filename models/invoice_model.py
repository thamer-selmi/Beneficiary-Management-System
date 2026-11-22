import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.colors import black, red
from datetime import datetime
from backend.farmers_services import Farmers
from backend.documents_services import Documents

def setup_arabic_font():
    """إعداد الخط العربي"""
    pdfmetrics.registerFont(TTFont('Arial', r'fonts\arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial_bold', r'fonts\arial_bold.ttf'))
    return ['Arial', 'Arial_bold']


def arabic_text(text, font_size=12, font_name='Arial'):
    """دالة لمعالجة النص العربي"""
    if not text:
        return ""
    
    # إعادة تشكيل النص العربي
    reshaped_text = arabic_reshaper.reshape(text)
    # تحويل النص إلى اتجاه RTL
    bidi_text = get_display(reshaped_text)
    return bidi_text

def create_invoice_pdf(cin:str, isOne:bool):

    today = datetime.now().strftime("%Y_%m_%d")
    folder_path = fr"الفواتير\{today}"
    

    os.makedirs(folder_path, exist_ok=True)
    output_path=rf"{folder_path}\{cin}.pdf"

    # إعداد الخط العربي
    arabic_font = setup_arabic_font()[0]
    arabic_bold_font = setup_arabic_font()[1]
    # إنشاء ملف PDF
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # إعداد الخلفية (لون أبيض)
    c.setFillColor("#dee0d3")
    c.rect(0, 0, width, height, fill=1)
    c.setFillColor(black)
    
    header_y = height - 40  # بداية من أعلى الصفحة
    
    # العنوان الرئيسي في الأعلى
    c.setFont(arabic_font, 14)
    c.drawRightString(width - 20, header_y, arabic_text("الجمهورية التونسية"))
    c.drawRightString(width - 20, header_y - 20, arabic_text("وزارة الفلاحة والموارد المائية والصيد البحري"))
    c.drawRightString(width - 20, header_y - 40, arabic_text("المندوبية الجهوية للتنمية الفلاحية بالقيروان"))
    c.drawRightString(width - 20, header_y - 60, arabic_text("مجمع التنمية في القطاع الفلاحي 'الانقاذ'"))
    
    # العنوان الفرعي
    today = datetime.now().strftime("%Y/%m/%d")
    c.drawString(20, header_y, arabic_text(f"منزل مهيري في {today}"))
    c.drawString(20, header_y - 20, arabic_text("قرية السوالم طريق"))
    c.drawString(20, header_y - 40, arabic_text("نصر الله - حفوز"))
    c.drawString(20, header_y - 60, arabic_text("بجانب دار السبوعي"))

    # مسار الصورة
    logo_path = r"img\logo.jpeg"
    img_w = 120
    img_h = 100

    # مكان الصورة (على يمين العنوان)
    img_x = width  / 2 - 80
    img_y = header_y - 75

    # رسم الصورة
    c.drawImage(logo_path, img_x, img_y, width=img_w, height=img_h, mask='auto')
    
    # الخط الفاصل
    c.line(10, header_y - 80, width - 10, header_y - 80) 

    # ===== عنوان الفاتورة الرئيسي =======
    invoice_title_y = header_y - 130

    # عنوان الفاتورة
    c.setFont(arabic_bold_font, 22)
    c.setFillColor("#556b2f")
    invoice_number = str(Documents.get_invoice_id())
    c.drawCentredString(width / 2, invoice_title_y, arabic_text(f"فاتورة استهلاك عدد {invoice_number}"))
    c.setFillColor(black)

    # فترة الاستهلاك
    c.setFont(arabic_font, 18)
    start_date = Documents.get_date()[0]
    end_date = Documents.get_date()[1]
    c.drawCentredString(width / 2, invoice_title_y - 30, arabic_text(f"من {start_date} الى {end_date}"))
    
    # ===== معلومات الفلاح =====
    farmer_info_y = invoice_title_y - 90
    c.setFont(arabic_bold_font, 16)
    c.drawRightString(width - 30, farmer_info_y, arabic_text("الى السيد(ة) :"))
    c.drawRightString(width - 30, farmer_info_y - 25, arabic_text(f"رقم بطاقة التعريف الوطنية :"))
    
    name = Documents.get_name(cin)
    c.setFont(arabic_font, 14)
    c.drawRightString(width - 106, farmer_info_y, arabic_text(name))
    c.drawRightString(width - 176, farmer_info_y - 25, arabic_text(cin))
    
    # ===== إنشاء الجدول =====
    table_y = farmer_info_y - 80

    headers_line1 = [
        "رقم", "العدد", "العدد", "الكمية", "سعر", "المبلغ", "باقي", "ديون", "معاليم"
    ]

    headers_line2 = [
        "العداد", "القديم", "الجديد", "المستهلكة", "متر3", "الجملي", "الدفوعات", "مخلدة", "قارة"
    ]

    c.setFont(arabic_font, 14)
    c.setFillColor("#556b2f")

    col_width = 60
    start_x = 30

    # عكس العناوين حتى تظهر من اليسار إلى اليمين بشكل مرتب
    headers_line1_ltr = headers_line1[::-1]
    headers_line2_ltr = headers_line2[::-1]

    # رسم خلفية العناوين
    for i in range(len(headers_line1_ltr)):
        x_pos = start_x + (i * col_width)
        c.rect(x_pos, table_y - 15, col_width, 40, fill=1)

    c.setFillColor(black)

    # كتابة العناوين
    for i, header in enumerate(headers_line1_ltr):
        x_pos = start_x + (i * col_width)
        c.drawCentredString(x_pos + col_width / 2, table_y + 10, arabic_text(header, 10))

    for i, header in enumerate(headers_line2_ltr):
        x_pos = start_x + (i * col_width)
        c.drawCentredString(x_pos + col_width / 2, table_y - 8, arabic_text(header, 10))

    # عرض بيانات الجدول
    data = Documents.for_invoice(cin)

    c.setFont(arabic_font, 10)
    row_y = table_y - 35
    row_height = 20

    for row in data:
        row_ltr = row[::-1]   # عكس البيانات أيضا
        for col_index, value in enumerate(row_ltr):
            x_pos = start_x + (col_index * col_width)
            c.drawCentredString(
                x_pos + col_width / 2,
                row_y,
                arabic_text(str(value))
            )
        row_y -= row_height

    # رسم الحدود
    c.setLineWidth(1)
    c.line(start_x, table_y - 15, start_x + (len(headers_line1_ltr) * col_width), table_y - 15)
    c.line(start_x, table_y - 150, start_x + (len(headers_line1_ltr) * col_width), table_y - 150)
    c.rect(start_x, table_y - 180, col_width * len(headers_line1_ltr), 30, fill=0)

    for i in range(len(headers_line1_ltr) + 1):
        x_pos = start_x + (i * col_width)
        c.line(x_pos, table_y - 15, x_pos, table_y - 150)
    
    # ===== المبلغ المطلوب =====
    amount_y = table_y - 170
    
    c.setFont(arabic_bold_font, 14)
    required_amount = "{:.3f}".format(Farmers.calcul_total_requird_amount(cin))
    c.drawRightString(width - 200, amount_y, arabic_text("المبلغ المطلوب :"))
    c.setFont(arabic_font, 14)
    c.drawRightString(width - 280, amount_y, arabic_text(f"{required_amount} دينار"))
    c.setFillColor(black)
    
    # ===== معلومات الدفع =====
    payment_info_y = amount_y - 50
    c.setFont(arabic_bold_font, 14)
    c.drawString(150, payment_info_y, arabic_text("رقم الحساب الجاري : 1320101100247 البنك الوطني الفلاحي"))
    c.setFillColor(red)
    c.drawString(235, payment_info_y - 25, arabic_text("الرجاء الدفع قبل موفى الشهر الحالي"))
    
    # ===== التوقيعات =====
    signatures_y = 120 
    
    # توزيع التوقيعات
    c.setFont(arabic_font, 14)
    c.setFillColor(black)
    c.drawRightString(width - 40, signatures_y, arabic_text("امضاء المدير الفني"))
    c.drawRightString(width / 2 + 35, signatures_y, arabic_text("امضاء أمين المال"))
    c.drawString(40, signatures_y, arabic_text("امضاء رئيس المجمع"))
    
    
    # حفظ الملف
    c.save()
    if isOne:
        os.startfile(output_path)
    else:
        os.startfile(folder_path)
    return output_path