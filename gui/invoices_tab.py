import tkinter as tk
from config import Config
from models import invoice_model, consumption
from backend.documents_services import Documents

class InvoicesTab:
    """أبسط نسخة لتبويب الفواتير"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=Config.BACKGROUND)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.setup_ui()
    
    def setup_ui(self):
        total_btn = tk.Button(
            self.frame,
            text="جميع الفواتير",
            font=("Arial", 14),
            bg=Config.PRIMARY,
            fg='white',
            width=25,
            height=3,
            command=self.show_total_invoices
        )
        total_btn.place(relx=0.5, rely=0.4, anchor='center')
        
        consumption_btn = tk.Button(
            self.frame,
            text="دفتر الاستهلاك",
            font=("Arial", 14),
            bg=Config.SUCCESS,
            fg='white',
            width=25,
            height=3,
            command=self.show_consumption_ledgers
        )
        consumption_btn.place(relx=0.5, rely=0.6, anchor='center')
    
    def show_total_invoices(self):
        cins = Documents.get_unique_cins()
        for cin in cins:
            invoice_model.create_invoice_pdf(cin, False)
    
    def show_consumption_ledgers(self):
        consumption.create_consumption_pdf()