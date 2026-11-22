"""
النافذة الرئيسية للتطبيق
"""

import tkinter as tk
from tkinter import ttk
from config import Config
from gui.dashboard import DashboardTab
from gui.farmers_tab import FarmersTab
from gui.reports_tab import ReportsTab
from gui.invoices_tab import InvoicesTab
from gui.settings import SettingTab

class MainWindow:
    """النافذة الرئيسية للنظام"""
    
    def __init__(self, root):
        self.root = root
        
        # إعداد النافذة
        self.setup_window()
        
        # إنشاء الواجهة
        self.create_ui()
    
    def setup_window(self):
        """إعداد إعدادات النافذة"""
        self.root.title(Config.APP_NAME)
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        self.root.configure(bg=Config.BACKGROUND)
        
        # مركزية النافذة
        self.center_window()
    
    def center_window(self):
        """مركزية النافذة على الشاشة"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_ui(self):
        """إنشاء واجهة المستخدم"""
        # شريط العنوان
        self.create_header()
        
        # منطقة المحتوى الرئيسية
        self.create_content_area()
    
    def create_header(self):
        """إنشاء شريط العنوان"""
        header = tk.Frame(
            self.root,
            bg=Config.PRIMARY,
            height=80
        )
        header.pack(fill=tk.X)
        
        # لوغو وتسمية النظام (يمين)
        logo_frame = tk.Frame(header, bg=Config.PRIMARY)
        logo_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        tk.Label(
            logo_frame,
            text="🌾",
            font=('Arial', 28),
            bg=Config.PRIMARY,
            fg='white'
        ).pack(side=tk.RIGHT)
        
        tk.Label(
            logo_frame,
            text=Config.APP_NAME,
            font=('Arial', 20, 'bold'),
            bg=Config.PRIMARY,
            fg='white'
        ).pack(side=tk.RIGHT, padx=10)
        
        # معلومات النظام (يسار)
        info_frame = tk.Frame(header, bg=Config.PRIMARY)
        info_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            info_frame,
            text=f"الإصدار: {Config.APP_VERSION}",
            font=('Arial', 10),
            bg=Config.PRIMARY,
            fg='white'
        ).pack(anchor='w')
    
    def create_content_area(self):
        """إنشاء منطقة المحتوى"""
        # الإطار الرئيسي
        main_frame = tk.Frame(self.root, bg=Config.BACKGROUND)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إنشاء نظام التبويبات
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء التبويبات
        self.create_tabs()
    
    def create_tabs(self):
        """إنشاء تبويبات النظام"""
        # تبويب لوحة التحكم
        self.dashboard_tab = DashboardTab(self.notebook)
        self.notebook.add(self.dashboard_tab.frame, text="🏠 الرئيسية")
        
        # تبويب الفلاحين
        self.farmers_tab = FarmersTab(self.notebook,)
        self.notebook.add(self.farmers_tab.frame, text="👨‍🌾 الفلاحين")
        
        # تبويب المستندات
        self.invoices_tab = InvoicesTab(self.notebook)
        self.notebook.add(self.invoices_tab.frame, text="💰 المستندات")
        
        # تبويب التقارير
        self.reports_tab = ReportsTab(self.notebook)
        self.notebook.add(self.reports_tab.frame, text="📊 التقارير")

         # تبويب الاعدادات
        self.settings_tab = SettingTab(self.notebook)
        self.notebook.add(self.settings_tab.frame, text=" الاعدادات")