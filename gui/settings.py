import tkinter as tk
from tkinter import messagebox
from config import Config
from tkinter import filedialog
from backend.documents_services import Documents, set_db_path
from backend.farmers_services import Farmers


class SettingTab:
    """تبويب الإعدادات"""

    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg=Config.BACKGROUND)
        self.create_ui()
        self.load_current_period()

    def create_ui(self):

        # ===== العنوان =====
        title = tk.Label(
            self.frame,
            text="⚙️ الإعدادات العامة",
            font=('Arial', 24, 'bold'),
            bg=Config.BACKGROUND,
            fg=Config.PRIMARY
        )
        title.pack(anchor='e', padx=40, pady=(30, 10))

        subtitle = tk.Label(
            self.frame,
            text="إدارة إعدادات التطبيق",
            font=('Arial', 12),
            bg=Config.BACKGROUND,
            fg="#555"
        )
        subtitle.pack(anchor='e', padx=40, pady=(0, 30))

        # =========================
        # تغيير الفترة
        # =========================
        period_frame = tk.Frame(self.frame, bg="white", bd=2, relief=tk.RIDGE)
        period_frame.pack(fill="x", padx=40, pady=10)

        tk.Label(
            period_frame,
            text="تغيير الفترة",
            font=('Arial', 16, 'bold'),
            bg="white",
            fg=Config.PRIMARY
        ).pack(anchor='e', padx=20, pady=15)

        input_frame = tk.Frame(period_frame, bg="white")
        input_frame.pack(padx=20, pady=10)

        # من
        tk.Label(
            input_frame,
            text="من:",
            font=('Arial', 12),
            bg="white"
        ).grid(row=0, column=2, padx=10, pady=5)

        self.from_entry = tk.Entry(input_frame, width=20, justify="right")
        self.from_entry.grid(row=0, column=1, padx=10, pady=5)

        # إلى
        tk.Label(
            input_frame,
            text="إلى:",
            font=('Arial', 12),
            bg="white"
        ).grid(row=1, column=2, padx=10, pady=5)

        self.to_entry = tk.Entry(input_frame, width=20, justify="right")
        self.to_entry.grid(row=1, column=1, padx=10, pady=5)

        # زر الحفظ
        save_btn = tk.Button(
            period_frame,
            text="💾 حفظ الفترة",
            bg=Config.PRIMARY,
            fg="white",
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.save_period
        )
        save_btn.pack(anchor='e', padx=20, pady=15)

        # =========================
        # مسح البيانات
        # =========================
        danger_frame = tk.Frame(self.frame, bg="white", bd=2, relief=tk.RIDGE)
        danger_frame.pack(fill="x", padx=40, pady=20)

        tk.Label(
            danger_frame,
            text="⚠",
            font=('Arial', 16, 'bold'),
            bg="white",
            fg="red"
        ).pack(anchor='e', padx=20, pady=15)

        delete_btn = tk.Button(
            danger_frame,
            text="🗑 مسح جميع البيانات",
            bg="red",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.confirm_delete
        )
        delete_btn.pack(anchor='e', padx=20, pady=15)


    # =========================
    # تحميل الفترة الحالية
    # =========================
    def load_current_period(self):

        from_, to_ = Documents.get_date()

        if from_:
            self.from_entry.insert(0, from_)
        if to_:
            self.to_entry.insert(0, to_)

    # =========================
    # حفظ الفترة
    # =========================
    def save_period(self):

        new_from = self.from_entry.get().strip()
        new_to = self.to_entry.get().strip()

        if not new_from or not new_to:
            messagebox.showerror("خطأ", "يرجى إدخال القيمتين")
            return
        isUpdate = Documents.update_date(new_from, new_to)
        if isUpdate:
            messagebox.showinfo("نجاح", "تم تحديث الفترة بنجاح")
        else:
            messagebox.showerror("خطأ",isUpdate)

    # =========================
    # تأكيد الحذف
    # =========================
    def confirm_delete(self):

        answer = messagebox.askyesno(
            "تحذير",
            "هل أنت متأكد أنك تريد مسح جميع البيانات؟ لا يمكن التراجع!"
        )

        if answer:
            self.delete_all_data()

    # =========================
    # مسح البيانات
    # =========================
    def delete_all_data(self):
        try:
            if Farmers.deleteAll():
                messagebox.showinfo("تم", "تم مسح جميع البيانات")
        except Exception as e:
            messagebox.showerror("خطأ", str(e))

    def choose_database(self):

        file_path = filedialog.askopenfilename(
            title="اختر قاعدة البيانات",
            filetypes=[("SQLite DB", "*.db")]
        )

        if file_path:
            try:
                set_db_path(file_path)
                messagebox.showinfo("نجاح", "تم تغيير قاعدة البيانات بنجاح")
            except Exception as e:
                messagebox.showerror("خطأ", str(e))