import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import filedialog
import logging
import os
import subprocess
import platform

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CauHinhRegGroupbox3:
    def __init__(self, parent):
        self.parent = parent
        self.create_cauhinhreggroupbox3()
    
    def create_cauhinhreggroupbox3(self):
        self.cauhinhreggroupbox3 = tk.Frame(self.parent, width=535, height=300, bg="#3b3b3b", relief="solid", bd=1, highlightbackground="white", highlightcolor="white", highlightthickness=1) 
        self.cauhinhreggroupbox3.place(x=620, y=60)
        self.cauhinhreggroupbox3.pack_propagate(False)
        
        self.setup_custom_tabs()
    
    def setup_custom_tabs(self):
        # Bước 1: Tạo Tab Header Frame (chứa các nút tab)
        self.tab_header_frame = tk.Frame(self.cauhinhreggroupbox3, height=35, bg="#3b3b3b")
        self.tab_header_frame.pack(fill="x", padx=5, pady=(5,0))
        self.tab_header_frame.pack_propagate(False)
        
        # Bước 2: Tạo Tab Content Frame (chứa nội dung tabs)
        self.tab_content_frame = tk.Frame(self.cauhinhreggroupbox3, bg="#2b2b2b")
        self.tab_content_frame.pack(fill="both", expand=True, padx=5, pady=(0,5))
        
        # Bước 3: Khởi tạo variables quản lý tabs
        self.current_tab = "Cài Đặt"
        self.tab_buttons = {}
        self.tab_contents = {}
        
        # Bước 4: Tạo từng tab
        self.create_tab_button("Cài Đặt", 0)
        self.create_tab_content("Cài Đặt")
        
        self.create_tab_button("Settings Info", 1)
        self.create_tab_content("Settings Info")
        
        self.create_tab_button("Change Info", 2)
        self.create_tab_content("Change Info")

        # Bước 5: Hiển thị tab đầu tiên
        self.show_tab("Cài Đặt")
    
    def create_tab_button(self, tab_name, index):
        button = tk.Button(self.tab_header_frame, text=tab_name, width=11, height=1, bg="#0dcaf0", fg="white", font=("Arial", 12, "bold"), bd=2, relief="raised", command=lambda: self.show_tab(tab_name))
        button.place(x=index*121, y=1)
        self.tab_buttons[tab_name] = button
    
    def create_tab_content(self, tab_name):
        content_frame = tk.Frame(self.tab_content_frame, bg="#3b3b3b")
        self.tab_contents[tab_name] = content_frame
        
        if tab_name == "Cài Đặt":
            self.setup_caidat_tab_content(content_frame)
        elif tab_name == "Settings Info":
            self.setup_settingsinfo_tab_content(content_frame)
        elif tab_name == "Change Info":
            self.setup_changeinfo_tab_content(content_frame)

    ###########################
    def setup_caidat_tab_content(self, content_frame):       
        so_ld_label = tk.Label(content_frame, text="Số LD/Phone:", font=('Arial', 12, 'bold'), bg='#3b3b3b', fg='white')
        so_ld_label.place(x=15, y=20)
        self.so_ld_var = self.create_custom_number_input(content_frame, x=150, y=25, width=150, min_val=1, max_val=999, default_val=1)
        
        so_acc_label = tk.Label(content_frame, text="Số Acc/Email:", font=('Arial', 12, 'bold'), bg='#3b3b3b', fg='white')
        so_acc_label.place(x=15, y=60)
        self.so_acc_var = self.create_custom_number_input(content_frame, x=150, y=65, width=150, min_val=1, max_val=999, default_val=1)
        
        duong_dan_label = tk.Label(content_frame, text="Đường dẫn:", font=('Arial', 12, 'bold'), bg='#3b3b3b', fg='white')
        duong_dan_label.place(x=15, y=100)
        self.duong_dan_var = tk.StringVar()
        duong_dan_input = ctk.CTkEntry(content_frame, width=150, height=25, placeholder_text="Chọn đường dẫn file", textvariable=self.duong_dan_var, border_color="#3b3b3b")
        duong_dan_input.place(x=150, y=105)
        browse_button = tk.Button(content_frame, text="Browse", bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=8, height=1, command=lambda: self.duong_dan_var.set(filedialog.askopenfilename(title="Chọn file", filetypes=[("All files", "*.*")]) or self.duong_dan_var.get()))
        browse_button.place(x=320, y=102)

        cai_apk_proxy_label = tk.Label(content_frame, text="Cài Apk Proxy:", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        cai_apk_proxy_label.place(x=15, y=140)
        
        self.apk_proxy_var = tk.StringVar(value="Vn2ray")
        apk_proxy_dropdown = ttk.Combobox(content_frame, values=["Vn2ray", "WW Proxy", "Proxy No1"], state="readonly", width=21, textvariable=self.apk_proxy_var)
        apk_proxy_dropdown.place(x=150, y=145)

        cai_dat_button = tk.Button(content_frame, text="Cài đặt", bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=8, height=1) #  command=self.on_cai_dat_button_click,
        cai_dat_button.place(x=320, y=140)

    
    def create_custom_number_input(self, parent, x, y, width=150, min_val=1, max_val=999, default_val=1):
        try:
            variable = tk.StringVar(value=str(default_val))
            number_entry = ctk.CTkEntry(parent, width=width, height=25, textvariable=variable, justify="center", font=("Arial", 12), border_color="#3b3b3b")
            number_entry.place(x=x, y=y)

            def increase_value():
                try:
                    current = int(variable.get())
                    if current < max_val:
                        variable.set(str(current + 1))
                except ValueError:
                    variable.set(str(default_val))

            def decrease_value():
                try:
                    current = int(variable.get())
                    if current > min_val:
                        variable.set(str(current - 1))
                except ValueError:
                    variable.set(str(min_val))

            def validate_input(event):
                try:
                    value = int(variable.get())
                    if value < min_val: variable.set(str(min_val))
                    elif value > max_val: variable.set(str(max_val))
                except ValueError:
                    variable.set(str(min_val))

            decrease_btn = tk.Button(parent, text="−", command=decrease_value, bg='#404040', fg='white', font=('Arial', 12, 'bold'), width=2, height=1, bd=1, relief="solid")
            decrease_btn.place(x=320, y=y)

            increase_btn = tk.Button(parent, text="+", command=increase_value, bg='#404040', fg='white', font=('Arial', 12, 'bold'), width=2, height=1, bd=1, relief="solid")
            increase_btn.place(x=360, y=y)

            number_entry.bind("<KeyRelease>", validate_input)
            number_entry.bind("<FocusOut>", validate_input)

            logger.info(f"Created number input at ({x}, {y}) with range {min_val}-{max_val}")
            return variable
        except Exception as e:
            logger.error(f"Error creating number input: {e}")
            return tk.StringVar(value=str(default_val))

    #########################
        
    def setup_settingsinfo_tab_content(self, content_frame):
        ho_button = tk.Button(content_frame, text="Họ", command=lambda: self.on_ho_button_click(), bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=8, height=1)
        ho_button.place(x=5, y=10)
        ten_button = tk.Button(content_frame, text="Tên", command=lambda: self.on_ten_button_click(), bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=8, height=1)
        ten_button.place(x=95, y=10)

        
    def setup_changeinfo_tab_content(self, content_frame):
        ho_button = tk.Button(content_frame, text="Họ", command=lambda: self.on_ho_button_click(), bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=8, height=1)
        ho_button.place(x=5, y=10)
        ten_button = tk.Button(content_frame, text="Tên Mới", command=lambda: self.on_ten_button_click(), bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=8, height=1)
        ten_button.place(x=95, y=10)
        

    #################################


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

    def on_ho_button_click(self):
        """Xử lý click button Họ - mở file Ho.txt để edit"""
        try:
            logger.info("Ho button clicked")
            
            # Tạo folder dulieu/hoten nếu chưa tồn tại
            folder_path = os.path.join("dulieu", "hoten")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                logger.info(f"Created folder: {folder_path}")
            
            # Đường dẫn file Ho.txt
            file_path = os.path.join(folder_path, "Ho.txt")
            
            # Tạo file với nội dung mặc định nếu chưa tồn tại
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("# File chứa danh sách Họ\n# Mỗi dòng một họ\nNguyen\nTran\nLe\nPham\nVo\n")
                logger.info(f"Created default Ho.txt file: {file_path}")
            
            # Mở file bằng editor mặc định của hệ thống
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            else:  # Linux
                subprocess.run(["xdg-open", file_path])
                       
        except Exception as e:
            logger.error(f"Error in ho button click: {e}")
            tk.messagebox.showerror("Lỗi", f"Không thể mở file Họ:\n{str(e)}")

    def on_ten_button_click(self):
        """Xử lý click button Tên - mở file Ten.txt để edit"""
        try:           
            logger.info("Ten button clicked")
            
            # Tạo folder dulieu/hoten nếu chưa tồn tại
            folder_path = os.path.join("dulieu", "hoten")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                logger.info(f"Created folder: {folder_path}")
            
            # Đường dẫn file Ten.txt
            file_path = os.path.join(folder_path, "Ten.txt")
            
            # Tạo file với nội dung mặc định nếu chưa tồn tại
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("# File chứa danh sách Tên\n# Mỗi dòng một tên\nVan A\nVan B\nVan C\n")
                logger.info(f"Created default Ten.txt file: {file_path}")
            
            # Mở file bằng editor mặc định của hệ thống
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            else:  # Linux
                subprocess.run(["xdg-open", file_path])
                        
        except Exception as e:
            logger.error(f"Error in ten button click: {e}")
            tk.messagebox.showerror("Lỗi", f"Không thể mở file Tên:\n{str(e)}")