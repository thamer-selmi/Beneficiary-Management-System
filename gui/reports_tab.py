"""
تبويب التقارير
"""

import tkinter as tk
from tkinter import ttk, messagebox
from backend.reports_services import Reports
from config import Config


class ReportsTab:
    """تبويب التقارير"""
    notAbilableMsg = "غير متوفر حاليا"

    def __init__(self, parent):
        self.parent = parent
        self.all_reports = []

        self.frame = tk.Frame(parent, bg=Config.BACKGROUND)
        self.setup_ui()

    def setup_ui(self):
        self.create_toolbar()
        self.create_report_area()

    # ===========================
    # شريط الأدوات
    # ===========================
    def create_toolbar(self):
        toolbar = tk.Frame(self.frame, bg=Config.CARD, height=60)
        toolbar.pack(fill=tk.X, padx=10, pady=10)

        reports = [
            ("📊 تقرير الاستهلاك", self.consumption_report),
            ("💰 تقرير الديون", self.debt_report),
            ("📈 تقرير الإيرادات", self.revenue_report),
            ("👥 تقرير الفلاحين", self.farmers_report),
            ("🔄 تحديث", self.load_sample_report),
        ]

        for text, command in reports:
            btn = tk.Button(
                toolbar,
                text=text,
                font=Config.NORMAL_FONT,
                bg=Config.PRIMARY,
                fg='white',
                relief=tk.RAISED,
                bd=2,
                padx=15,
                pady=6,
                cursor='hand2',
                command=command
            )
            btn.pack(side=tk.RIGHT, padx=5, pady=10)

    # ===========================
    # منطقة التقرير
    # ===========================
    def create_report_area(self):

        report_frame = tk.Frame(self.frame, bg='white', relief=tk.SUNKEN, bd=2)
        report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # ===== التحكم =====
        control_frame = tk.Frame(report_frame, bg='white')
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            control_frame,
            text="معاينة التقرير",
            font=Config.SUBHEADING_FONT,
            bg='white',
            fg=Config.PRIMARY
        ).pack(side=tk.RIGHT, padx=10)

        # حقل البحث
        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            control_frame,
            textvariable=self.search_var,
            font=Config.NORMAL_FONT,
            width=30,
            justify='right'
        )
        search_entry.pack(side=tk.LEFT, padx=5)

        # زر البحث
        search_btn = tk.Button(
            control_frame,
            text="🔍 بحث",
            font=Config.NORMAL_FONT,
            bg=Config.PRIMARY,
            fg="white",
            cursor="hand2",
            command=self.search_reports
        )
        search_btn.pack(side=tk.LEFT, padx=5)

        # زر مسح
        clear_btn = tk.Button(
            control_frame,
            text="❌ مسح",
            font=Config.NORMAL_FONT,
            bg="gray",
            fg="white",
            cursor="hand2",
            command=self.clear_search
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

        # عداد النتائج
        self.result_label = tk.Label(
            control_frame,
            text="",
            font=Config.NORMAL_FONT,
            bg="white",
            fg="gray"
        )
        self.result_label.pack(side=tk.LEFT, padx=15)

        # ===== منطقة النص =====
        text_frame = tk.Frame(report_frame, bg='white')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.report_text = tk.Text(
            text_frame,
            font=("Arial", 15),
            bg='white',
            fg=Config.TEXT,
            wrap=tk.WORD
        )

        scrollbar = ttk.Scrollbar(
            text_frame,
            orient=tk.VERTICAL,
            command=self.report_text.yview
        )

        self.report_text.configure(yscrollcommand=scrollbar.set)

        self.report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_sample_report()

    # ===========================
    # تحميل التقارير
    # ===========================
    def load_sample_report(self):

        self.all_reports = Reports.get_last_reports()

        self.report_text.config(state='normal')
        self.report_text.delete(1.0, 'end')

        for report in self.all_reports:
            self.report_text.insert('end', report + "\n")

        self.report_text.config(state='disabled')
        self.result_label.config(text=f"عدد النتائج: {len(self.all_reports)}")

    # ===========================
    # البحث
    # ===========================
    def search_reports(self):

        query = self.search_var.get().strip().lower()

        self.report_text.config(state='normal')
        self.report_text.delete(1.0, 'end')

        count = 0

        for report in self.all_reports:
            if query in report.lower():
                self.report_text.insert('end', report + "\n")
                count += 1

        self.report_text.config(state='disabled')
        self.result_label.config(text=f"عدد النتائج: {count}")

    # ===========================
    # مسح البحث
    # ===========================
    def clear_search(self):

        self.search_var.set("")
        self.load_sample_report()

    # ===========================
    # أنواع التقارير
    # ===========================



    def consumption_report(self):
        self.load_sample_report()
        messagebox.showinfo("تقرير",  str(self.notAbilableMsg))

    def debt_report(self):
        messagebox.showinfo("تقرير", str(self.notAbilableMsg))

    def revenue_report(self):
        messagebox.showinfo("تقرير", str(self.notAbilableMsg))

    def farmers_report(self):
        messagebox.showinfo("تقرير", str(self.notAbilableMsg))
