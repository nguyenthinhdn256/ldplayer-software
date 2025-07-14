import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CauHinhRegGroupbox4:
    def __init__(self, parent):
        self.parent = parent
        self.app_selection_var = tk.StringVar(value="")  # Thêm biến này
        self.checkboxes = {}
        self.create_cauhinhreggroupbox4()
    
    def create_cauhinhreggroupbox4(self):
        self.cauhinhreggroupbox4 = tk.Frame(self.parent, width=1145, height=80, bg="#3b3b3b", relief="solid", bd=1, highlightbackground="white", highlightcolor="white", highlightthickness=1) 
        self.cauhinhreggroupbox4.place(x=10, y=370)
        self.cauhinhreggroupbox4.pack_propagate(False)
        
        def create_checkbox_icon(parent, x, y, checked=False):
            canvas = tk.Canvas(parent, width=18, height=18, bg="#3b3b3b", highlightthickness=0)
            canvas.place(x=x, y=y)
            canvas.create_rectangle(2, 2, 16, 16, outline="white", fill="", width=2)
            if checked:
                canvas.create_line(5, 9, 8, 12, fill="white", width=2)
                canvas.create_line(8, 12, 13, 6, fill="white", width=2)
            return canvas

        def on_checkbox_click(value):
            self.xuly_checkbox(value)

        # Checkbox "Không mồi", "khong_moi"
        icon_khong_moi = create_checkbox_icon(self.cauhinhreggroupbox4, 15, 10, False)
        icon_khong_moi.bind('<Button-1>', lambda e: on_checkbox_click("khong_moi"))
        label_khong_moi = tk.Label(self.cauhinhreggroupbox4, text="Không mồi", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_khong_moi.place(x=40, y=7)
        label_khong_moi.bind('<Button-1>', lambda e: on_checkbox_click("khong_moi"))

        # Checkbox "Mồi Mail Theo Tệp", "mail_theo_tep"
        icon_mail_theo_tep = create_checkbox_icon(self.cauhinhreggroupbox4, 250, 10, False)
        icon_mail_theo_tep.bind('<Button-1>', lambda e: on_checkbox_click("mail_theo_tep"))
        label_mail_theo_tep = tk.Label(self.cauhinhreggroupbox4, text="Mồi Mail Theo Tệp", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_mail_theo_tep.place(x=275, y=7)
        label_mail_theo_tep.bind('<Button-1>', lambda e: on_checkbox_click("mail_theo_tep"))
        mail_theo_tep_button = tk.Button(self.cauhinhreggroupbox4, text="Sửa Mail", command=self.on_sua_tep_mail_click, bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=8, height=1)
        mail_theo_tep_button.place(x=450, y=7)

        # Checkbox "Mồi SĐT Theo Tệp", "sdt_theo_tep" - SỬA LẠI VALUE
        icon_sdt_theo_tep = create_checkbox_icon(self.cauhinhreggroupbox4, 250, 45, False)
        icon_sdt_theo_tep.bind('<Button-1>', lambda e: on_checkbox_click("sdt_theo_tep"))  # Sửa từ "maildrop"
        label_sdt_theo_tep = tk.Label(self.cauhinhreggroupbox4, text="Mồi SĐT Theo Tệp", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_sdt_theo_tep.place(x=275, y=42)
        label_sdt_theo_tep.bind('<Button-1>', lambda e: on_checkbox_click("sdt_theo_tep"))  # Sửa từ "maildrop"
        sdt_theo_tep_button = tk.Button(self.cauhinhreggroupbox4, text="Sửa SĐT", command=self.on_sua_tep_sdt_click, bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=8, height=1)
        sdt_theo_tep_button.place(x=450, y=42)

        # Checkbox "Mồi Theo Đầu Mail", "sdt_dau_mail"
        icon_sdt_dau_mail = create_checkbox_icon(self.cauhinhreggroupbox4, 700, 10, False)
        icon_sdt_dau_mail.bind('<Button-1>', lambda e: on_checkbox_click("sdt_dau_mail"))
        label_sdt_dau_mail = tk.Label(self.cauhinhreggroupbox4, text="Mồi Theo Đầu Mail", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_sdt_dau_mail.place(x=725, y=7)
        label_sdt_dau_mail.bind('<Button-1>', lambda e: on_checkbox_click("sdt_dau_mail"))
        mail_sdt_dau_mail_button = tk.Button(self.cauhinhreggroupbox4, text="Sửa Mail", command=self.on_sua_dau_mail_click, bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=8, height=1)
        mail_sdt_dau_mail_button.place(x=900, y=7)

        # Checkbox "Mồi Theo Đầu Số", "sdt_dau_so"
        icon_sdt_dau_so = create_checkbox_icon(self.cauhinhreggroupbox4, 700, 45, False)
        icon_sdt_dau_so.bind('<Button-1>', lambda e: on_checkbox_click("sdt_dau_so"))
        label_sdt_dau_so = tk.Label(self.cauhinhreggroupbox4, text="Mồi Theo Đầu Số", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_sdt_dau_so.place(x=725, y=42)
        label_sdt_dau_so.bind('<Button-1>', lambda e: on_checkbox_click("sdt_dau_so"))
        sdt_sdt_dau_so_button = tk.Button(self.cauhinhreggroupbox4, text="Sửa SĐT", command=self.on_sua_dau_so_click, bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=8, height=1)
        sdt_sdt_dau_so_button.place(x=900, y=42)

        self.checkboxes.update({"khong_moi": icon_khong_moi, "mail_theo_tep": icon_mail_theo_tep, "sdt_theo_tep": icon_sdt_theo_tep, "sdt_dau_mail": icon_sdt_dau_mail, "sdt_dau_so": icon_sdt_dau_so})
        
    # DI CHUYỂN METHOD RA NGOÀI VÀ SỬA INDENTATION
    def xuly_checkbox(self, value):
        current_value = self.app_selection_var.get()
        if current_value == value:
            self.app_selection_var.set("")
        else:
            self.app_selection_var.set(value)
        selected_value = self.app_selection_var.get()
        for checkbox_name, checkbox_canvas in self.checkboxes.items():
            checkbox_canvas.delete("all")
            checkbox_canvas.create_rectangle(2, 2, 16, 16, outline="white", fill="", width=2)
            if checkbox_name == selected_value:
                checkbox_canvas.create_line(5, 9, 8, 12, fill="white", width=2)
                checkbox_canvas.create_line(8, 12, 13, 6, fill="white", width=2)

    def on_sua_tep_mail_click(self):
        """Xử lý khi click button Sửa Mail - mở file mailtheotep.txt"""
        try:
            import os, subprocess, platform
            logger.info("Sua Mail button clicked")
            folder_path = os.path.join("dulieu", "mailphone")
            if not os.path.exists(folder_path): os.makedirs(folder_path)
            file_path = os.path.join(folder_path, "mailtheotep.txt")
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f: 
                    f.write("# File chứa danh sách mail theo tệp\n# Mỗi dòng một mail\nexample1@gmail.com\nexample2@gmail.com\nexample3@gmail.com\n")
            if platform.system() == "Windows": os.startfile(file_path)
            elif platform.system() == "Darwin": subprocess.run(["open", file_path])
            else: subprocess.run(["xdg-open", file_path])
        except Exception as e:
            logger.error(f"Error in sua mail button click: {e}")
            tk.messagebox.showerror("Lỗi", f"Không thể mở file mailtheotep.txt:\n{str(e)}")

    def on_sua_tep_sdt_click(self):
        """Xử lý khi click button Sửa SĐT - mở file sdttheotep.txt"""
        try:
            import os, subprocess, platform
            logger.info("Sua SDT button clicked")
            folder_path = os.path.join("dulieu", "mailphone")
            if not os.path.exists(folder_path): os.makedirs(folder_path)
            file_path = os.path.join(folder_path, "sdttheotep.txt")
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f: 
                    f.write("# File chứa danh sách SĐT theo tệp\n# Mỗi dòng một SĐT\n0912345678\n0987654321\n0123456789\n")
            if platform.system() == "Windows": os.startfile(file_path)
            elif platform.system() == "Darwin": subprocess.run(["open", file_path])
            else: subprocess.run(["xdg-open", file_path])
        except Exception as e:
            logger.error(f"Error in sua sdt button click: {e}")
            tk.messagebox.showerror("Lỗi", f"Không thể mở file sdttheotep.txt:\n{str(e)}")

    def on_sua_dau_mail_click(self):
        """Xử lý khi click button Sửa Mail - mở file daumail.txt"""
        try:
            import os, subprocess, platform
            logger.info("Sua Dau Mail button clicked")
            folder_path = os.path.join("dulieu", "mailphone")
            if not os.path.exists(folder_path): os.makedirs(folder_path)
            file_path = os.path.join(folder_path, "daumail.txt")
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f: 
                    f.write("# File chứa danh sách đầu mail\n# Mỗi dòng một đầu mail\nexample1@gmail.com\nexample2@hotmail.com\nexample3@outlook.com\n")
            if platform.system() == "Windows": os.startfile(file_path)
            elif platform.system() == "Darwin": subprocess.run(["open", file_path])
            else: subprocess.run(["xdg-open", file_path])
        except Exception as e:
            logger.error(f"Error in sua dau mail button click: {e}")
            tk.messagebox.showerror("Lỗi", f"Không thể mở file daumail.txt:\n{str(e)}")

    def on_sua_dau_so_click(self):
        """Xử lý khi click button Sửa SĐT - mở file dauso.txt"""
        try:
            import os, subprocess, platform
            logger.info("Sua Dau So button clicked")
            folder_path = os.path.join("dulieu", "mailphone")
            if not os.path.exists(folder_path): os.makedirs(folder_path)
            file_path = os.path.join(folder_path, "dauso.txt")
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f: 
                    f.write("# File chứa danh sách đầu số\n# Mỗi dòng một đầu số\n091\n098\n032\n033\n034\n035\n036\n037\n038\n039\n")
            if platform.system() == "Windows": os.startfile(file_path)
            elif platform.system() == "Darwin": subprocess.run(["open", file_path])
            else: subprocess.run(["xdg-open", file_path])
        except Exception as e:
            logger.error(f"Error in sua dau so button click: {e}")
            tk.messagebox.showerror("Lỗi", f"Không thể mở file dauso.txt:\n{str(e)}")