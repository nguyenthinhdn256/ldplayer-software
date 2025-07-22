import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import subprocess
import sys, json, os
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from service.veri_facebook import VerificationHandlerFactory
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CauHinhRegGroupbox2:
    def __init__(self, parent):
        self.parent = parent
        self.app_selection_var = tk.StringVar(value="")
        self.checkboxes = {}
        self.create_cauhinhreggroupbox2()
    
    def create_cauhinhreggroupbox2(self):
        self.cauhinhreggroupbox2 = tk.Frame(self.parent, width=600, height=300, bg="#3b3b3b", relief="solid", bd=1, highlightbackground="white", highlightcolor="white", highlightthickness=1) 
        self.cauhinhreggroupbox2.place(x=10, y=60)
        self.cauhinhreggroupbox2.pack_propagate(False)
        
        self.setup_custom_tabs()
    
    def setup_custom_tabs(self):
        # Bước 1: Tạo Tab Header Frame (chứa các nút tab)
        self.tab_header_frame = tk.Frame(self.cauhinhreggroupbox2, height=35, bg="#3b3b3b")
        self.tab_header_frame.pack(fill="x", padx=5, pady=(5,0))
        self.tab_header_frame.pack_propagate(False)
        
        # Bước 2: Tạo Tab Content Frame (chứa nội dung tabs)
        self.tab_content_frame = tk.Frame(self.cauhinhreggroupbox2, bg="#2b2b2b")
        self.tab_content_frame.pack(fill="both", expand=True, padx=5, pady=(0,5))
        
        # Bước 3: Khởi tạo variables quản lý tabs
        self.current_tab = "Ver Mail Api"
        self.tab_buttons = {}
        self.tab_contents = {}
        
        # Bước 4: Tạo từng tab
        self.create_tab_button("Ver Mail Api", 0)
        self.create_tab_content("Ver Mail Api")
        
        self.create_tab_button("Ver SMS", 1)
        self.create_tab_content("Ver SMS")
        
        self.create_tab_button("Ver Input Mail", 2)
        self.create_tab_content("Ver Input Mail")

        self.create_tab_button("Mail Change", 3)
        self.create_tab_content("Mail Change")
        
        # Bước 5: Hiển thị tab đầu tiên
        self.show_tab("Ver Mail Api")
    
    def create_tab_button(self, tab_name, index):
        button = tk.Button(self.tab_header_frame, text=tab_name, width=11, height=1, bg="#0dcaf0", fg="white", font=("Arial", 12, "bold"), bd=2, relief="raised", command=lambda: self.show_tab(tab_name))
        button.place(x=index*121, y=1)
        self.tab_buttons[tab_name] = button
    
    def create_tab_content(self, tab_name):
        content_frame = tk.Frame(self.tab_content_frame, bg="#3b3b3b")
        self.tab_contents[tab_name] = content_frame
        
        if tab_name == "Ver Mail Api":
            self.setup_vermailapi_tab_content(content_frame)
        elif tab_name == "Ver SMS":
            self.setup_versms_tab_content(content_frame)
        elif tab_name == "Ver Input Mail":
            self.setup_verinputmail_tab_content(content_frame)
        elif tab_name == "Mail Change":
            self.setup_mailchange_tab_content(content_frame)
    
    def setup_vermailapi_tab_content(self, content_frame):
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

        # Checkbox Gmail thuesim.app
        icon_mailthuesim = create_checkbox_icon(content_frame, 10, 20, False)
        icon_mailthuesim.bind('<Button-1>', lambda e: on_checkbox_click("mailthuesim"))
        label_mailthuesim = tk.Label(content_frame, text="Gmail thuesim.app", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_mailthuesim.place(x=35, y=17)
        label_mailthuesim.bind('<Button-1>', lambda e: on_checkbox_click("mailthuesim"))

        gmail_mailthuesim_input = ctk.CTkEntry(content_frame, width=100, height=25, border_color="#212529")
        gmail_mailthuesim_input.place(x=200, y=17)
        gmail_mailthuesim_api_input = ctk.CTkEntry(content_frame, width=250, height=25, placeholder_text="Write Api Key", border_color="#212529")
        gmail_mailthuesim_api_input.place(x=320, y=17)

        # Checkbox Gmail ironsim.com
        icon_ironsim = create_checkbox_icon(content_frame, 10, 50, False)
        icon_ironsim.bind('<Button-1>', lambda e: on_checkbox_click("mailironsim"))
        label_ironsim = tk.Label(content_frame, text="Gmail ironsim.com", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_ironsim.place(x=35, y=47)
        label_ironsim.bind('<Button-1>', lambda e: on_checkbox_click("mailironsim"))

        gmail_ironsim_input = ctk.CTkEntry(content_frame, width=250, height=25, placeholder_text="Write Api Key", border_color="#212529")
        gmail_ironsim_input.place(x=320, y=47)

        # Checkbox Hotmail regclone2fa.com
        icon_regclone2fa = create_checkbox_icon(content_frame, 10, 80, False)
        icon_regclone2fa.bind('<Button-1>', lambda e: on_checkbox_click("regclone2fa"))
        label_regclone2fa = tk.Label(content_frame, text="Hotmail regclone2fa.com", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_regclone2fa.place(x=35, y=77)
        label_regclone2fa.bind('<Button-1>', lambda e: on_checkbox_click("regclone2fa"))

        hotmail_regclone2fa_input = ctk.CTkEntry(content_frame, width=250, height=25, placeholder_text="Write Api Key", border_color="#212529")
        hotmail_regclone2fa_input.place(x=320, y=77)

        # Checkbox Hotmail dongvanfb.net
        icon_dongvanfb = create_checkbox_icon(content_frame, 10, 110, False)
        icon_dongvanfb.bind('<Button-1>', lambda e: on_checkbox_click("dongvanfb"))
        label_dongvanfb = tk.Label(content_frame, text="Hotmail dongvanfb.net", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_dongvanfb.place(x=35, y=107)
        label_dongvanfb.bind('<Button-1>', lambda e: on_checkbox_click("dongvanfb"))

        hotmail_dongvanfb_input = ctk.CTkEntry(content_frame, width=50, height=25, border_color="#212529")
        hotmail_dongvanfb_input.place(x=250, y=107)
        hotmail_dongvanfb_api_input = ctk.CTkEntry(content_frame, width=250, height=25, placeholder_text="Write Api Key", border_color="#212529")
        hotmail_dongvanfb_api_input.place(x=320, y=107)

        # Checkbox Input Mail
        icon_inputmail = create_checkbox_icon(content_frame, 10, 220, False)
        icon_inputmail.bind('<Button-1>', lambda e: self.handle_inputmail_checkbox())
        label_inputmail = tk.Label(content_frame, text="Input Mail", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_inputmail.place(x=35, y=217)
        label_inputmail.bind('<Button-1>', lambda e: self.handle_inputmail_checkbox())

        # Lưu trữ các checkbox để quản lý
        self.checkboxes.update({"mailthuesim": icon_mailthuesim, "mailironsim": icon_ironsim, "regclone2fa": icon_regclone2fa, "dongvanfb": icon_dongvanfb, "inputmail": icon_inputmail})
    
    def get_selected_mail_verification_handler(self):
        """Lấy handler cho verification mail được chọn"""
        selected = self.app_selection_var.get()
        if not selected:
            return None
        
        try:
            if selected == "mailthuesim":
                api_key = self.gmail_mailthuesim_api_input.get() if hasattr(self, 'gmail_mailthuesim_api_input') else None
                gmail_account = self.gmail_mailthuesim_input.get() if hasattr(self, 'gmail_mailthuesim_input') else None
                return VerificationHandlerFactory.create_handler('mailthuesim', api_key=api_key, gmail_account=gmail_account)
            elif selected == "mailironsim":
                api_key = self.gmail_ironsim_input.get() if hasattr(self, 'gmail_ironsim_input') else None
                return VerificationHandlerFactory.create_handler('mailironsim', api_key=api_key)
            elif selected == "regclone2fa":
                api_key = self.hotmail_regclone2fa_input.get() if hasattr(self, 'hotmail_regclone2fa_input') else None
                return VerificationHandlerFactory.create_handler('regclone2fa', api_key=api_key)
            elif selected == "dongvanfb":
                api_key = self.hotmail_dongvanfb_api_input.get() if hasattr(self, 'hotmail_dongvanfb_api_input') else None
                account = self.hotmail_dongvanfb_input.get() if hasattr(self, 'hotmail_dongvanfb_input') else None
                return VerificationHandlerFactory.create_handler('dongvanfb', api_key=api_key, account=account)
            elif selected == "inputmail":
                return VerificationHandlerFactory.create_handler('inputmail')
        except Exception as e:
            logging.error(f"Lỗi tạo mail verification handler: {str(e)}")
        return None

    def setup_versms_tab_content(self, content_frame):
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

        # Checkbox SIM viotp.com
        icon_simviotp = create_checkbox_icon(content_frame, 10, 10, False)
        icon_simviotp.bind('<Button-1>', lambda e: on_checkbox_click("simviotp"))
        label_simviotp = tk.Label(content_frame, text="SIM viotp.com", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_simviotp.place(x=35, y=7)
        label_simviotp.bind('<Button-1>', lambda e: on_checkbox_click("simviotp"))

        sim_viotp_input = ctk.CTkEntry(content_frame, width=250, height=25, placeholder_text="Write Api Key", border_color="#212529")
        sim_viotp_input.place(x=320, y=7)

        # Checkbox SIM ironsim.com
        icon_smsironsim = create_checkbox_icon(content_frame, 10, 40, False)
        icon_smsironsim.bind('<Button-1>', lambda e: on_checkbox_click("smsironsim"))
        label_smsironsim = tk.Label(content_frame, text="SIM ironsim.com", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_smsironsim.place(x=35, y=37)
        label_smsironsim.bind('<Button-1>', lambda e: on_checkbox_click("smsironsim"))

        sim_smsironsim_input = ctk.CTkEntry(content_frame, width=100, height=25, border_color="#212529")
        sim_smsironsim_input.place(x=200, y=37)
        sim_smsironsim_input2 = ctk.CTkEntry(content_frame, width=250, height=25, placeholder_text="Write Api Key", border_color="#212529")
        sim_smsironsim_input2.place(x=320, y=37)

        # Checkbox SIM funotp.com
        icon_funotp = create_checkbox_icon(content_frame, 10, 70, False)
        icon_funotp.bind('<Button-1>', lambda e: on_checkbox_click("funotp"))
        label_funotp = tk.Label(content_frame, text="SIM funotp.com", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_funotp.place(x=35, y=67)
        label_funotp.bind('<Button-1>', lambda e: on_checkbox_click("funotp"))

        sim_funotp_input = ctk.CTkEntry(content_frame, width=250, height=25, placeholder_text="Write Api Key", border_color="#212529")
        sim_funotp_input.place(x=320, y=67)

        # Checkbox SIM 5sim.com
        icon_5sim = create_checkbox_icon(content_frame, 10, 100, False)
        icon_5sim.bind('<Button-1>', lambda e: on_checkbox_click("5sim"))
        label_5sim = tk.Label(content_frame, text="SIM 5sim.com", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_5sim.place(x=35, y=97)
        label_5sim.bind('<Button-1>', lambda e: on_checkbox_click("5sim"))

        sim_5sim_input = ctk.CTkEntry(content_frame, width=250, height=25, placeholder_text="Write Api Key", border_color="#212529")
        sim_5sim_input.place(x=320, y=97)

        # Checkbox SIM 368sms.com
        icon_368sms = create_checkbox_icon(content_frame, 10, 130, False)
        icon_368sms.bind('<Button-1>', lambda e: on_checkbox_click("368sms"))
        label_368sms = tk.Label(content_frame, text="SIM 368sms.com", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_368sms.place(x=35, y=127)
        label_368sms.bind('<Button-1>', lambda e: on_checkbox_click("368sms"))

        sim_368sms_input = ctk.CTkEntry(content_frame, width=250, height=25, placeholder_text="Write Api Key", border_color="#212529")
        sim_368sms_input.place(x=320, y=127)

        # Checkbox SIM hcotp.com
        icon_hcotp = create_checkbox_icon(content_frame, 10, 160, False)
        icon_hcotp.bind('<Button-1>', lambda e: on_checkbox_click("hcotp"))
        label_hcotp = tk.Label(content_frame, text="SIM hcotp.com", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_hcotp.place(x=35, y=157)
        label_hcotp.bind('<Button-1>', lambda e: on_checkbox_click("hcotp"))

        sim_hcotp_input = ctk.CTkEntry(content_frame, width=250, height=25, placeholder_text="Write Api Key", border_color="#212529")
        sim_hcotp_input.place(x=320, y=157)

        # Checkbox SIM thuesim.app
        icon_smsthuesim = create_checkbox_icon(content_frame, 10, 190, False)
        icon_smsthuesim.bind('<Button-1>', lambda e: on_checkbox_click("smsthuesim"))
        label_smsthuesim = tk.Label(content_frame, text="SIM thuesim.app", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_smsthuesim.place(x=35, y=187)
        label_smsthuesim.bind('<Button-1>', lambda e: on_checkbox_click("smsthuesim"))

        gmail_smsthuesim_input = ctk.CTkEntry(content_frame, width=100, height=25, border_color="#212529")
        gmail_smsthuesim_input.place(x=200, y=187)
        sim_smsthuesim_input = ctk.CTkEntry(content_frame, width=250, height=25, placeholder_text="Write Api Key", border_color="#212529")
        sim_smsthuesim_input.place(x=320, y=187)

        # Checkbox SIM sim24.cc
        icon_sim24 = create_checkbox_icon(content_frame, 10, 220, False)
        icon_sim24.bind('<Button-1>', lambda e: on_checkbox_click("sim24"))
        label_sim24 = tk.Label(content_frame, text="SIM sim24.cc", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_sim24.place(x=35, y=217)
        label_sim24.bind('<Button-1>', lambda e: on_checkbox_click("sim24"))

        sim_sim24_input = ctk.CTkEntry(content_frame, width=250, height=25, placeholder_text="Write Api Key", border_color="#212529")
        sim_sim24_input.place(x=320, y=217)

        self.checkboxes.update({"simviotp": icon_simviotp, "smsironsim": icon_smsironsim, "funotp": icon_funotp, "5sim": icon_5sim, "368sms": icon_368sms, "hcotp": icon_hcotp, "smsthuesim": icon_smsthuesim, "sim24": icon_sim24})
    
    def get_selected_sms_verification_handler(self):
        """Lấy handler cho verification SMS được chọn"""
        selected = self.app_selection_var.get()
        if not selected:
            return None
        
        try:
            if selected == "simviotp":
                api_key = self.sim_viotp_input.get() if hasattr(self, 'sim_viotp_input') else None
                return VerificationHandlerFactory.create_handler('simviotp', api_key=api_key)
            elif selected == "smsironsim":
                api_key = self.sim_smsironsim_input2.get() if hasattr(self, 'sim_smsironsim_input2') else None
                account = self.sim_smsironsim_input.get() if hasattr(self, 'sim_smsironsim_input') else None
                return VerificationHandlerFactory.create_handler('smsironsim', api_key=api_key, account=account)
            elif selected == "funotp":
                api_key = self.sim_funotp_input.get() if hasattr(self, 'sim_funotp_input') else None
                return VerificationHandlerFactory.create_handler('funotp', api_key=api_key)
            elif selected == "5sim":
                api_key = self.sim_5sim_input.get() if hasattr(self, 'sim_5sim_input') else None
                return VerificationHandlerFactory.create_handler('5sim', api_key=api_key)
            elif selected == "368sms":
                api_key = self.sim_368sms_input.get() if hasattr(self, 'sim_368sms_input') else None
                return VerificationHandlerFactory.create_handler('368sms', api_key=api_key)
            elif selected == "hcotp":
                api_key = self.sim_hcotp_input.get() if hasattr(self, 'sim_hcotp_input') else None
                return VerificationHandlerFactory.create_handler('hcotp', api_key=api_key)
            elif selected == "smsthuesim":
                api_key = self.sim_smsthuesim_input.get() if hasattr(self, 'sim_smsthuesim_input') else None
                gmail_account = self.gmail_smsthuesim_input.get() if hasattr(self, 'gmail_smsthuesim_input') else None
                return VerificationHandlerFactory.create_handler('smsthuesim', api_key=api_key, gmail_account=gmail_account)
            elif selected == "sim24":
                api_key = self.sim_sim24_input.get() if hasattr(self, 'sim_sim24_input') else None
                return VerificationHandlerFactory.create_handler('sim24', api_key=api_key)
        except Exception as e:
            logging.error(f"Lỗi tạo SMS verification handler: {str(e)}")
        return None    



    #################################
    def setup_verinputmail_tab_content(self, content_frame):
        loai_mail_label = tk.Label(content_frame, text="Loại Mail:", font=('Arial', 12, 'bold'), bg='#3b3b3b', fg='white')
        loai_mail_label.place(x=5, y=10)
        mail_type_dropdown = ttk.Combobox(content_frame, values=["Gmail", "Hotmail", "Outlook Mail"], state="readonly", width=15)
        mail_type_dropdown.place(x=90, y=10)
        mail_type_dropdown.set("Gmail")
        chia_data_label = tk.Label(content_frame, text="Chia data:", font=('Arial', 12, 'bold'), bg='#3b3b3b', fg='white')
        chia_data_label.place(x=320, y=10)
        chia_button = tk.Button(content_frame, text="Chia", bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=8, height=1, command=self.open_chia_mail_window)
        chia_button.place(x=410, y=8)
        self.bangdulieu_verinputmail(content_frame)

    def bangdulieu_verinputmail(self, content_frame):
        table_frame = tk.Frame(content_frame, width=580, height=218, bg="#3b3b3b", relief="solid", bd=2, highlightbackground="#f8f9fa", highlightcolor="#f8f9fa", highlightthickness=2)
        table_frame.place(x=5, y=50)
        table_frame.pack_propagate(False)
        canvas = tk.Canvas(table_frame, bg="#3b3b3b", highlightthickness=0)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#3b3b3b")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        headers = [("", 30), ("STT", 50), ("DANH SÁCH MAIL", 200), ("LD PORT", 147), ("LẦN NHẬN CODE", 120)]
        for col, (header, width) in enumerate(headers):
            header_label = tk.Label(scrollable_frame, text=header, font=('Arial', 10, 'bold'), bg="#0dcaf0", fg="black", width=width//8, relief="solid", bd=0, highlightbackground="white", highlightthickness=1)
            header_label.grid(row=0, column=col, sticky="ew")
        self.table_canvas = canvas
        self.table_scrollable_frame = scrollable_frame
        self.table_headers = headers
        self.table_data = []
    
    def open_chia_mail_window(self):
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'script_phu'))
        chiamail_module = __import__('chiamail')
        chia_window = tk.Toplevel(self.parent)
        chia_manager = chiamail_module.LDPlayerManager(chia_window)
        chia_manager.set_update_table_callback(self.update_table_data)  

    def update_table_data(self, configs, folder_count):
        for widget in self.table_scrollable_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        row = 1
        port = 5554
        for i in range(1, folder_count + 1):
            for file_type in ['gmail', 'hotmail', 'outlookmail']:
                if file_type in configs and configs[file_type]['data']:
                    chunks = self.split_data_for_table(configs[file_type]['data'], configs[file_type]['split'])
                    if chunks:
                        chunk_index = (i - 1) % len(chunks)
                        data_for_folder = chunks[chunk_index]
                        for email_line in data_for_folder:
                            email = email_line.split(':')[0].split('|')[0] if ':' in email_line or '|' in email_line else email_line
                            cells = ["", str(row), email, f"emulator-{port}", ""]
                            for col, (cell_data, (_, width)) in enumerate(zip(cells, self.table_headers)):
                                cell_label = tk.Label(self.table_scrollable_frame, text=cell_data, font=('Arial', 9), bg="#3b3b3b", fg="white", width=width//8, relief="solid", bd=0, anchor="center", highlightbackground="white", highlightthickness=1)
                                cell_label.grid(row=row, column=col, sticky="ew")
                            row += 1
            port += 2
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

    def split_data_for_table(self, data, chunk_size):
        chunks = []
        for i in range(0, len(data), chunk_size):
            chunks.append(data[i:i + chunk_size])
        return chunks

    #################################

    def setup_mailchange_tab_content(self, content_frame):
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

        # Checkbox Mail 10minutemail.net
        icon_10minutemail = create_checkbox_icon(content_frame, 10, 10, False)
        icon_10minutemail.bind('<Button-1>', lambda e: on_checkbox_click("10minutemail"))
        label_10minutemail = tk.Label(content_frame, text="Mail 10minutemail.net", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_10minutemail.place(x=35, y=7)
        label_10minutemail.bind('<Button-1>', lambda e: on_checkbox_click("10minutemail"))

        # Checkbox Mail guerrillamail.com
        icon_guerrillamail = create_checkbox_icon(content_frame, 10, 40, False)
        icon_guerrillamail.bind('<Button-1>', lambda e: on_checkbox_click("guerrillamail"))
        label_guerrillamail = tk.Label(content_frame, text="Mail guerrillamail.com", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_guerrillamail.place(x=35, y=37)
        label_guerrillamail.bind('<Button-1>', lambda e: on_checkbox_click("guerrillamail"))

        # Checkbox Mail maildrop.cc
        icon_maildrop = create_checkbox_icon(content_frame, 10, 70, False)
        icon_maildrop.bind('<Button-1>', lambda e: on_checkbox_click("maildrop"))
        label_maildrop = tk.Label(content_frame, text="SIM funotp.com", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_maildrop.place(x=35, y=67)
        label_maildrop.bind('<Button-1>', lambda e: on_checkbox_click("maildrop"))

        # Checkbox Mail mohmal.com
        icon_mohmal = create_checkbox_icon(content_frame, 10, 100, False)
        icon_mohmal.bind('<Button-1>', lambda e: on_checkbox_click("mohmal"))
        label_mohmal = tk.Label(content_frame, text="Mail mohmal.com", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_mohmal.place(x=35, y=97)
        label_mohmal.bind('<Button-1>', lambda e: on_checkbox_click("mohmal"))

        # Checkbox Mail temp-mail.io
        icon_tempmailio = create_checkbox_icon(content_frame, 10, 130, False)
        icon_tempmailio.bind('<Button-1>', lambda e: on_checkbox_click("tempmailio"))
        label_tempmailio = tk.Label(content_frame, text="Mail temp-mail.io", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_tempmailio.place(x=35, y=127)
        label_tempmailio.bind('<Button-1>', lambda e: on_checkbox_click("tempmailio"))

        # Checkbox Mail temp-mail.org
        icon_tempmailorg = create_checkbox_icon(content_frame, 10, 160, False)
        icon_tempmailorg.bind('<Button-1>', lambda e: on_checkbox_click("tempmailorg"))
        label_tempmailorg = tk.Label(content_frame, text="Mail temp-mail.org", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_tempmailorg.place(x=35, y=157)
        label_tempmailorg.bind('<Button-1>', lambda e: on_checkbox_click("tempmailorg"))

        # Checkbox Mail tempmail100.com
        icon_tempmail100 = create_checkbox_icon(content_frame, 10, 190, False)
        icon_tempmail100.bind('<Button-1>', lambda e: on_checkbox_click("tempmail100"))
        label_tempmail100 = tk.Label(content_frame, text="Mail tempmail100.com", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_tempmail100.place(x=35, y=187)
        label_tempmail100.bind('<Button-1>', lambda e: on_checkbox_click("tempmail100"))

        # Checkbox Mail tempmail.io
        icon_tempmail_io = create_checkbox_icon(content_frame, 10, 220, False)
        icon_tempmail_io.bind('<Button-1>', lambda e: on_checkbox_click("tempmail_io"))
        label_tempmail_io = tk.Label(content_frame, text="Mail tempmail.io", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_tempmail_io.place(x=35, y=217)
        label_tempmail_io.bind('<Button-1>', lambda e: on_checkbox_click("tempmail_io"))


        # Checkbox Mail tempmail.so
        icon_tempmailso = create_checkbox_icon(content_frame, 300, 10, False)
        icon_tempmailso.bind('<Button-1>', lambda e: on_checkbox_click("tempmailso"))
        label_tempmailso = tk.Label(content_frame, text="Mail tempmail.so", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_tempmailso.place(x=325, y=7)
        label_tempmailso.bind('<Button-1>', lambda e: on_checkbox_click("tempmailso"))

        # Checkbox Mail yopmail.com
        icon_yopmail = create_checkbox_icon(content_frame, 300, 40, False)
        icon_yopmail.bind('<Button-1>', lambda e: on_checkbox_click("yopmail"))
        label_yopmail = tk.Label(content_frame, text="Mail Mail yopmail.com", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_yopmail.place(x=325, y=37)
        label_yopmail.bind('<Button-1>', lambda e: on_checkbox_click("yopmail"))


        self.checkboxes.update({"10minutemail": icon_10minutemail, "guerrillamail": icon_guerrillamail, "maildrop": icon_maildrop, "mohmal": icon_mohmal, "tempmailio": icon_tempmailio, "tempmailorg": icon_tempmailorg, "tempmail100": icon_tempmail100, "tempmail_io": icon_tempmail_io, "tempmailso": icon_tempmailso, "yopmail": icon_yopmail})
    
    def handle_inputmail_checkbox(self):
        # Xử lý chuyển sang tab Ver Input Mail khi checkbox Input Mail được tích
        self.xuly_checkbox("inputmail")
        self.show_tab("Ver Input Mail")


    def show_tab(self, tab_name):
        # Bước 1: Ẩn tất cả nội dung tab
        for content in self.tab_contents.values():
            content.pack_forget()
        
        # Bước 2: Reset màu tất cả button về màu mặc định
        for button in self.tab_buttons.values():
            button.configure(bg="#404040")
        
        # Bước 3: Hiển thị nội dung tab được chọn
        if tab_name in self.tab_contents:
            self.tab_contents[tab_name].pack(fill="both", expand=True)
        
        # Bước 4: Highlight button tab được chọn
        if tab_name in self.tab_buttons:
            self.tab_buttons[tab_name].configure(bg="#0dcaf0")
        
        # Bước 5: Cập nhật tab hiện tại
        self.current_tab = tab_name

    def xuly_checkbox(self, value): # Xử lý logic tích chọn checkbox cho Ver Mail Api và Ver SMS
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

    def get_verification_configuration(self):
        """Lấy cấu hình verification đầy đủ cho script chính"""
        try:
            selected = self.app_selection_var.get()
            if selected:
                # Xác định loại verification
                mail_verification_types = ['mailthuesim', 'mailironsim', 'regclone2fa', 'dongvanfb', 'inputmail']
                sms_verification_types = ['simviotp', 'smsironsim', 'funotp', '5sim', '368sms', 'hcotp', 'smsthuesim', 'sim24']
                
                if selected in mail_verification_types:
                    verification_method = "mail"
                elif selected in sms_verification_types:
                    verification_method = "sms"
                else:
                    verification_method = "unknown"
                
                return {"use_verification": True, "verification_type": selected, "verification_method": verification_method, "enabled": True}
            else:
                return {"use_verification": False, "verification_type": "", "verification_method": "", "enabled": False}
        except Exception as e:
            logger.error(f"Error getting verification configuration: {e}")
            return {"use_verification": False, "verification_type": "", "verification_method": "", "enabled": False}