import tkinter as tk
from tkinter import ttk, messagebox
from backend.farmers_services import Farmers
from config import Config
from gui.dialogs import AddFarmerDialog, EditFarmerDialog
from models.invoice_model import create_invoice_pdf

class FarmersTab:

    def __init__(self, parent):
        self.parent = parent
        self.selected_cin = None
        self.selected_counter = None

        self.frame = tk.Frame(parent, bg=Config.BACKGROUND)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.create_toolbar()
        self.create_table()
        self.load_farmers()

    # ================= Toolbar =================
    def create_toolbar(self):
        """إنشاء شريط الأدوات"""
        toolbar = tk.Frame(self.frame, bg=Config.CARD, height=60)
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        # أزرار الإجراءات
        actions = [
            ("➕ إضافة", Config.PRIMARY, lambda: AddFarmerDialog()),
            ("✏️ تعديل", Config.PRIMARY, self.edit_farmer ),
            ("🗑️ حذف", Config.PRIMARY, self.delete_farmer),
            ("🔄 تحديث", Config.PRIMARY, self.load_farmers),
            ("🧾 فاتورة", Config.PRIMARY, self.create_invoice)
        ]
        
        for text, color, command in actions:
            btn = tk.Button(
                toolbar,
                text=text,
                font=Config.NORMAL_FONT,
                bg=color,
                fg='white',
                relief=tk.RAISED,
                bd=2,
                padx=10,
                pady=5,
                cursor='hand2',
                command=command
            )
            btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # حقل البحث
        search_frame = tk.Frame(toolbar, bg=Config.CARD)
        search_frame.pack(side=tk.RIGHT, padx=20)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=Config.NORMAL_FONT,
            bg='white',
            fg=Config.TEXT,
            relief=tk.SUNKEN,
            bd=2,
            width=30
        )
        search_entry.pack(side=tk.RIGHT, padx=5)
        
        # زر البحث
        search_btn = tk.Button(
            search_frame,
            text="بحث",
            font=Config.NORMAL_FONT,
            bg=Config.PRIMARY,
            fg='white',
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5,
            command=self.search_farmer
        )
        search_btn.pack(side=tk.RIGHT)

    # ================= Table =================
    def create_table(self):
        cols = (
            "name", "cin", "counter_number", "old_counter", "current_counter",
            "consumed", "price", "total_amount", "remaining_payment",
            "outstanding_debt", "fixed_fees", "required_amount",
            "entry_date", "last_update", "password"
        )

        self.tree = ttk.Treeview(self.frame, columns=cols[::-1], show="headings")  # عكس الأعمدة

        headers = [
            "الاسم", "ر ب ت و", "العداد", "قديم", "حالي",
            "الكمية المستهلكة", "السعر", "المبلغ الجملي", "باقي الدفوعات",
            "الديون المخلدة", "معاليم قارة", "المبلغ المطلوب",
            "الدخول", "آخر تحديث", "كلمة المرور"
        ]

        headers_ltr = headers[::-1]  # عكس العناوين لتوافق ترتيب الأعمدة

        for c, h in zip(cols[::-1], headers_ltr):
            self.tree.heading(c, text=h, anchor="center")  # ضبط النص في الوسط
            self.tree.column(c, width=120, anchor="center")  # ضبط عرض الأعمدة

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    # ================= Logic =================
    def load_farmers(self):
        self.tree.delete(*self.tree.get_children())
        for f in Farmers.getAll():
            self.tree.insert("", tk.END, values=tuple(f.get(c, "") for c in self.tree["columns"]))

    def on_select(self, event):
        sel = self.tree.selection()
        if sel:
            vals = self.tree.item(sel[0], "values")
            self.selected_name = str(vals[14])
            self.selected_cin = str(vals[13])
            self.selected_counter = str(vals[12])

    def delete_farmer(self):
        if self.selected_cin is None or self.selected_counter is None:
            messagebox.showwarning("تنبيه", "اختر منتفع")
            return
        if Farmers.deleteOne(self.selected_name, self.selected_cin, self.selected_counter):
            self.load_farmers()
            messagebox.showinfo("تم", "تم الحذف")
        else:
            messagebox.showerror("خطأ", "غير موجود")

    def search_farmer(self):
        term = self.search_var.get()
        if not term:
            self.load_farmers()
            return

        self.tree.delete(*self.tree.get_children())
        for f in Farmers.search(term):
            self.tree.insert("", tk.END, values=tuple(f.get(c, "") for c in self.tree["columns"]))


    def edit_farmer(self):
        if not self.selected_cin:
            messagebox.showwarning("تنبيه", "اختر منتفع")
            return
        else:
            EditFarmerDialog(self.selected_name, self.selected_cin, self.selected_counter)

    def create_invoice(self):
        if not self.selected_cin or not self.selected_name:
            messagebox.showwarning("تنبيه", "اختر منتفع")
            return
        else :
            create_invoice_pdf(self.selected_cin, True)