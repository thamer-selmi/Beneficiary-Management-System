import tkinter as tk
from tkinter import messagebox
from backend.farmers_services import Farmers
from config import Config


class AddFarmerDialog(tk.Toplevel):

    def __init__(self):
        super().__init__()
        self.title(f"{Config.APP_NAME} — إضافة فلاح")
        self.configure(bg=Config.BACKGROUND)
        self.resizable(False, False)
        
        # مركزية النافذة
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (420 // 2)
        y = (self.winfo_screenheight() // 2) - (1000 // 2)
        self.geometry(f"420x750+{x}+{y}")

        self.vars = {}
        
        # إطار رئيسي للتمرير
        main_frame = tk.Frame(self, bg=Config.BACKGROUND)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self._build_header(main_frame)
        self._build_form(main_frame)
        self._build_actions(main_frame)

    def _build_header(self, parent):
        header_frame = tk.Frame(parent, bg=Config.PRIMARY, height=70, 
                               highlightthickness=0)
        header_frame.pack(fill='x', pady=(0, 15))
        header_frame.pack_propagate(False)
        
        title = tk.Label(header_frame, text="إضافة فلاح جديد", 
                        bg=Config.PRIMARY, fg='white', 
                        font=("Arial", 16, "bold"))
        title.pack(side='right', padx=(0, 5), pady=20)
        
        separator = tk.Frame(parent, height=2, bg='#E0E0E0')
        separator.pack(fill='x', pady=(0, 15))

    def _build_form(self, parent):
        form_frame = tk.Frame(parent, bg=Config.BACKGROUND)
        form_frame.pack(fill='both', expand=True, pady=(0, 10))

        # نفس الحقول بنفس الترتيب تمامًا
        fields = [
            ("الاسم واللقب", "name"),
            ("رقم البطاقة (CIN)", "cin"),
            ("رقم العداد", "counter_number"),
            ("العداد القديم", "old_counter"),
            ("العداد الحالي", "current_counter"),
            ("سعر المتر", "price"),
            ("المدفوع", "payment"),
            ("الديون السابقة", "outstanding_debt"),
            ("المعاليم القارة", "fixed_fees"),
        ]

        for label_text, key in fields:
            field_container = tk.Frame(form_frame, bg=Config.BACKGROUND)
            field_container.pack(fill='x', pady=8)
            
            # التسمية مع محاذاة مناسبة
            lbl = tk.Label(field_container, text=label_text, 
                          bg=Config.BACKGROUND, fg='#333333',
                          font=("Arial", 11), anchor='e', width=20)
            lbl.pack(side='right', padx=(10, 0))
            
            # حقل الإدخال مع تصميم محسّن
            entry_bg = '#FFFFFF'
            show_char = '•' if 'password' in key else ''
            
            ent = tk.Entry(field_container, 
                          font=("Arial", 11),
                          bd=2,
                          relief='solid',
                          bg=entry_bg,
                          highlightthickness=0,
                          highlightbackground='#CCCCCC',
                          highlightcolor=Config.PRIMARY,
                          show=show_char,
                          insertbackground='#333333')
            ent.pack(side='right', fill='x', expand=True, ipady=8)
            
            # تأثيرات التركيز
            def make_focus_handlers(entry, bg_color):
                def on_focus_in(event):
                    entry.config(bg='#F0F8FF', highlightbackground=Config.PRIMARY)
                def on_focus_out(event):
                    entry.config(bg=bg_color, highlightbackground='#CCCCCC')
                return on_focus_in, on_focus_out
            
            focus_in, focus_out = make_focus_handlers(ent, entry_bg)
            ent.bind('<FocusIn>', focus_in)
            ent.bind('<FocusOut>', focus_out)
            
            self.vars[key] = ent

    def _build_actions(self, parent):
        action_frame = tk.Frame(parent, bg=Config.BACKGROUND)
        action_frame.pack(fill='x', pady=(20, 0))
        
        # خط فاصل فوق الأزرار
        separator = tk.Frame(parent, height=1, bg='#E0E0E0')
        separator.pack(fill='x', pady=(0, 15))
        
        # إطار للأزرار
        button_frame = tk.Frame(action_frame, bg=Config.BACKGROUND)
        button_frame.pack(fill='x', pady=5)
        
        # زر الإلغاء
        cancel_btn = tk.Button(button_frame, 
                              text="إلغاء",
                              bg='#6C757D',
                              fg='white',
                              font=("Arial", 11, "bold"),
                              command=self.close,
                              bd=0,
                              relief='flat',
                              cursor='hand2',
                              padx=30,
                              pady=12,
                              activebackground='#5A6268',
                              activeforeground='white')
        cancel_btn.pack(side='right', padx=(5, 0), fill='x', expand=True)
        
        # زر الحفظ
        save_btn = tk.Button(button_frame,
                            text="💾 حفظ",
                            bg=Config.PRIMARY,
                            fg='white',
                            font=("Arial", 11, "bold"),
                            command=self.submit,
                            bd=0,
                            relief='flat',
                            cursor='hand2',
                            padx=30,
                            pady=12,
                            activebackground='#0056b3',
                            activeforeground='white')
        save_btn.pack(side='left', padx=(0, 5), fill='x', expand=True)

    def submit(self):
        # جمع البيانات من الحقول
        data = {k: v.get() for k, v in self.vars.items()}
        
        # التحقق من الحقول الأساسية
        required_fields = ['name', 'cin', 'counter_number']
        missing = []
        
        for field in required_fields:
            if field in self.vars and not self.vars[field].get().strip():
                missing.append(field)
        
        if missing:
            field_names = {
                'name': 'الاسم واللقب',
                'cin': 'رقم البطاقة',
                'counter_number': 'رقم العداد'
            }
            missing_text = "\n".join([f"• {field_names[f]}" for f in missing])
            messagebox.showwarning("حقول مطلوبة", 
                                  f"يرجى ملء الحقول التالية:\n{missing_text}")
            return
        
        try:
            # تحويل القيم العددية
            name = data['name'].strip()
            cin = data['cin'].strip()
            counter_number = data['counter_number'].strip()
            old_counter = float(data['old_counter']) if data['old_counter'] else 0.0
            current_counter = float(data['current_counter']) if data['current_counter'] else 0.0
            price = float(data['price']) if data['price'] else 0.0
            payment = float(data['payment']) if data['payment'] else 0.0
            outstanding_debt = float(data['outstanding_debt']) if data['outstanding_debt'] else 0.0
            fixed_fees = float(data['fixed_fees']) if data['fixed_fees'] else 0.0
            
            # التحقق من صحة القيم العددية
            if current_counter < old_counter:
                messagebox.showwarning("خطأ في القيم", 
                                      "العداد الحالي يجب أن يكون أكبر من أو يساوي العداد القديم")
                return
            
            # استدعاء دالة الـ add من الـ backend
            Farmers.add(
                name=name,
                cin=cin,
                counter_number=counter_number,
                old_counter=old_counter,
                current_counter=current_counter,
                price=price,
                payment=payment,
                outstanding_debt=outstanding_debt,
                fixed_fees=fixed_fees,
            )
            
            # إظهار رسالة نجاح
            messagebox.showinfo("تم الحفظ", "✓ تمت إضافة الفلاح بنجاح!")
            
        except ValueError as e:
            messagebox.showerror("خطأ في القيم", 
                                f"يرجى إدخال قيم رقمية صحيحة:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("خطأ", 
                                f"حدث خطأ أثناء حفظ البيانات:\n{str(e)}")

    def close(self):
        self.destroy()


class EditFarmerDialog(tk.Toplevel):
    def __init__(self, name, cin, counter_number):
        super().__init__()

        self.name = name
        self.cin = cin
        self.counter_number = counter_number

        self.title(f"{Config.APP_NAME} — تعديل فلاح")
        self.configure(bg=Config.BACKGROUND)
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (520 // 2)
        y = (self.winfo_screenheight() // 2) - (620 // 2)
        self.geometry(f"520x620+{x}+{y}")
        self.resizable(False, False)
        self.vars = {}

        main_frame = tk.Frame(self, bg=Config.BACKGROUND)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self._build_header(main_frame)
        self._build_static_info(main_frame)
        self._build_form(main_frame)
        self._build_actions(main_frame)

    # ================= HEADER =================
    def _build_header(self, parent):
        header = tk.Frame(parent, bg=Config.PRIMARY, height=70)
        header.pack(fill='x', pady=(0, 15))
        header.pack_propagate(False)

        tk.Label(
            header,
            text="تعديل بيانات الفلاح",
            bg=Config.PRIMARY,
            fg="white",
            font=("Arial", 20, "bold")
        ).pack(side='right', padx=10, pady=20)

    # ================= STATIC INFO =================
    def _build_static_info(self, parent):
        info_frame = tk.Frame(parent, bg=Config.BACKGROUND)
        info_frame.pack(fill='x', pady=(0, 15))

        infos = [
            ("الاسم و اللقب", self.name),
            ("رقم البطاقة (CIN)", self.cin),
            ("رقم العداد", self.counter_number),
        ]

        for label, value in infos:
            row = tk.Frame(info_frame, bg=Config.BACKGROUND)
            row.pack(fill='x', pady=5)

            tk.Label(
                row,
                text=label,
                bg=Config.BACKGROUND,
                font=("Arial", 16),
                width=20,
                anchor='e'
            ).pack(side='right', padx=(10, 0))

            ent = tk.Entry(
                row,
                font=("Arial", 16),
                width=100,
                bd=2,
                relief='solid',
                bg='#EEEEEE'
            )
            ent.insert(0, value)
            ent.config(state='disabled')
            ent.pack(side='right', fill='x', expand=True, ipady=6)

    # ================= FORM =================
    def _build_form(self, parent):
        form = tk.Frame(parent, bg=Config.BACKGROUND)
        form.pack(fill='both', expand=True)

        fields = [
            ("العداد الجديد", "new_counter"),
            ("دفعة جديدة", "payment"),
            ("اضافة معاليم", "add_fees"),
            ("دفعة المعاليم", "fees_payment"),
        ]

        for label_text, key in fields:
            row = tk.Frame(form, bg=Config.BACKGROUND)
            row.pack(fill='x', pady=10)

            tk.Label(
                row,
                text=label_text,
                bg=Config.BACKGROUND,
                font=("Arial", 16),
                width=20,
                anchor='e'
            ).pack(side='right', padx=(10, 0))

            ent = tk.Entry(
                row,
                font=("Arial", 11),
                bd=2,
                relief='solid',
                bg='white'
            )
            ent.pack(side='right', fill='x', expand=True, ipady=8)
            self.vars[key] = ent

    # ================= ACTIONS =================
    def _build_actions(self, parent):
        frame = tk.Frame(parent, bg=Config.BACKGROUND)
        frame.pack(fill='x', pady=(20, 0))

        tk.Button(
            frame,
            text="إلغاء",
            bg="#6C757D",
            fg="white",
            font=("Arial", 16, "bold"),
            command=self.destroy,
            bd=0,
            padx=30,
            pady=12
        ).pack(side='right', padx=5, fill='x', expand=True)

        tk.Button(
            frame,
            text="💾 حفظ التعديلات",
            bg=Config.PRIMARY,
            fg="white",
            font=("Arial", 16, "bold"),
            command=self.submit,
            bd=0,
            padx=30,
            pady=12
        ).pack(side='left', padx=5, fill='x', expand=True)

    # ================= SUBMIT =================
    def submit(self):
        try:
            new_counter_var = float(self.vars["new_counter"].get() or 0)
            payment_var = float(self.vars["payment"].get() or 0)
            fees_payment_var = float(self.vars["fees_payment"].get() or 0)
            add_fees_var = float(self.vars["add_fees"].get() or 0)

            if payment_var != 0:
                Farmers.update_payments(
                    self.name,
                    self.cin,
                    self.counter_number,
                    payment_var,
                )
            if fees_payment_var != 0:
                Farmers.update_fees(
                    self.name,
                    self.cin,
                    self.counter_number,
                    fees_payment_var,
                )
            if add_fees_var != 0:
                Farmers.add_fees(
                    self.name,
                    self.cin,
                    self.counter_number,
                    add_fees_var,
                )
            if new_counter_var != 0:
                Farmers.add_new_counter(
                    self.name,
                    self.cin,
                    self.counter_number,
                    new_counter_var,
                )
            
            messagebox.showinfo("تم", "✓ تم تحديث البيانات بنجاح")
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال قيم رقمية صحيحة")
        except Exception as e:
            messagebox.showerror("خطأ", str(e)) 