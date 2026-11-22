"""
إعدادات النظام
"""

class Config:
    # معلومات التطبيق
    APP_NAME = "نظام إدارة المنتفعين"
    APP_VERSION = "2.0.0"
    
    # إعدادات النافذة
    WINDOW_SIZE = "1400x800"
    MIN_WINDOW_SIZE = "1000x600"
    
    # ألوان النظام
    PRIMARY = '#2E7D32'       # أخضر داكن
    SECONDARY = '#4CAF50'     # أخضر
    ACCENT = '#81C784'        # أخضر فاتح
    BACKGROUND = '#F5F5F5'    # رمادي فاتح
    CARD = '#FFFFFF'          # أبيض
    TEXT = '#212529'          # أسود
    BORDER = '#E0E0E0'        # رمادي
    SUCCESS = '#388E3C'       # أخضر نجاح
    WARNING = '#F57C00'       # برتقالي تحذير
    ERROR = '#D32F2F'         # أحمر خطأ
    INFO = '#1976D2'          # أزرق معلومات
    
    # الخطوط
    TITLE_FONT = ('Arial', 20, 'bold')
    HEADING_FONT = ('Arial', 16, 'bold')
    SUBHEADING_FONT = ('Arial', 14, 'bold')
    NORMAL_FONT = ('Arial', 12)
    SMALL_FONT = ('Arial', 10)
    
    @classmethod
    def get_color(cls, color_name):
        """الحصول على لون"""
        return getattr(cls, color_name, cls.PRIMARY)