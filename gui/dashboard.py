
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from backend.documents_services import Documents
from config import Config
from backend.farmers_services import Farmers
from backend.reports_services import Reports

class DashboardTab:
    
    def __init__(self, parent):
        self.parent = parent
        
        self.frame = tk.Frame(parent, bg=Config.BACKGROUND)
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        self.create_header()
        
        self.create_stats_row()
        
        self.create_recent_activities()
    
    def create_header(self):
        header_frame = tk.Frame(self.frame, bg=Config.PRIMARY, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_frame = tk.Frame(header_frame, bg=Config.PRIMARY)
        title_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        tk.Label(
            title_frame,
            text="📊 ",
            font=('Arial', 24, 'bold'),
            bg=Config.PRIMARY,
            fg='white'
        ).pack(side=tk.RIGHT)
        
        date_frame = tk.Frame(header_frame, bg=Config.PRIMARY)
        date_frame.pack(side=tk.LEFT, padx=20, pady=20)
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        tk.Label(
            date_frame,
            text=f"📅 {current_date}",
            font=('Arial', 12),
            bg=Config.PRIMARY,
            fg='white'
        ).pack()
    
    def create_stats_row(self):
        self.stats_frame = tk.Frame(self.frame, bg=Config.BACKGROUND)
        self.stats_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        self.update_stats()

    def update_stats(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        getData = Farmers.get_total_data()
        total = len(Documents.get_unique_cins())

        stats_data = [
            {"title": "إجمالي المنتفعين", "value": total, "color": Config.INFO, "icon": "👥"},
            {"title": "إجمالي الكميات المستهلكة", "value": getData[0], "color": Config.SECONDARY, "icon": "💧"},
            {"title": "اجمالي المبالغ الجملية", "value": getData[1], "color": Config.SECONDARY, "icon": "📋"},
            {"title": "اجمالي الديون", "value": getData[2], "color": Config.ERROR, "icon": "💵"},
            {"title": "اجمالي المعاليم القارة", "value": getData[3], "color": Config.ERROR, "icon": "💵"},
            {"title": "اجمالي المبالغ المطلوبة", "value": getData[4], "color": Config.PRIMARY, "icon": "💰"},
        ]

        for data in stats_data:
            card = self.create_stat_card(self.stats_frame, data)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5) 
    
    def create_stat_card(self, parent, data):
        card = tk.Frame(parent, bg=Config.CARD, relief=tk.RAISED, borderwidth=2)
        
        content = tk.Frame(card, bg=Config.CARD, padx=15, pady=15)
        content.pack(fill=tk.BOTH, expand=True)
        
        top_row = tk.Frame(content, bg=Config.CARD)
        top_row.pack(fill=tk.X)
        
        tk.Label(
            top_row,
            text=data["icon"],
            font=('Arial', 20),
            bg=Config.CARD
        ).pack(side=tk.RIGHT)
        
        tk.Label(
            top_row,
            text=data["title"],
            font=('Arial', 11),
            bg=Config.CARD,
            fg=Config.TEXT
        ).pack(side=tk.RIGHT, padx=(8, 0))
        
        tk.Label(
            content,
            text=data["value"],
            font=('Arial', 24, 'bold'),
            bg=Config.CARD,
            fg=data["color"]
        ).pack(pady=(10, 5))
        
        tk.Label(
            content,
            text="آخر تحديث: الآن",
            font=('Arial', 9),
            bg=Config.CARD,
            fg='#666666'
        ).pack()
        
        separator = tk.Frame(card, height=3, bg=data["color"])
        separator.pack(fill=tk.X, side=tk.BOTTOM)
        
        return card
    
    def create_recent_activities(self):
        activities_frame = tk.Frame(self.frame, bg=Config.CARD, relief=tk.RAISED, borderwidth=2)
        activities_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        title_frame = tk.Frame(activities_frame, bg=Config.CARD)
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            title_frame,
            text="🕐 النشاطات الأخيرة",
            font=Config.HEADING_FONT,
            bg=Config.CARD,
            fg=Config.TEXT
        ).pack(side=tk.RIGHT)
        
        tk.Button(
            title_frame,
            text="تحديث",
            font=('Arial', 12),
            bg=Config.CARD,
            fg=Config.PRIMARY,
            relief=tk.FLAT,
            cursor='hand2',
            command=self.refresh_data
        ).pack(side=tk.LEFT)
        
        list_frame = tk.Frame(activities_frame, bg=Config.CARD)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        self.activities_list = tk.Listbox(
            list_frame,
            height=8,
            font=('Arial', 18),
            bg='white',
            fg=Config.TEXT,
            relief=tk.SUNKEN,
            borderwidth=1,
            selectbackground=Config.ACCENT
        )
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.activities_list.yview)
        self.activities_list.configure(yscrollcommand=scrollbar.set)
        
        self.activities_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.load_recent_activities()
        
    def load_recent_activities(self):
        self.activities_list.delete(0, tk.END)

        reports = Reports.get_last_reports()
        reports = reports[:10]
        for report in reports:
            self.activities_list.insert(tk.END, report)
    
    def refresh_data(self):
        self.update_stats()
        self.load_recent_activities()

