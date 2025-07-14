import tkinter as tk
from tkinter import ttk
from gui.cauhinhreggroupbox1 import CauHinhRegGroupbox1
from gui.cauhinhreggroupbox2 import CauHinhRegGroupbox2
from gui.cauhinhreggroupbox3 import CauHinhRegGroupbox3
from gui.cauhinhreggroupbox4 import CauHinhRegGroupbox4  
from gui.cauhinhreggroupbox5 import CauHinhRegGroupbox5
from gui.quanlyldphonegroupbox1 import QuanLyLDPhoneGroupbox1
from gui.quanlyldphonegroupbox2 import QuanLyLDPhoneGroupbox2
from gui.quanlyreggroupbox1 import QuanLyRegGroupbox1  

class Groupbox4Manager:
    def __init__(self, parent):
        self.parent = parent
        self.current_tab = "CẤU HÌNH REG"
        self.create_groupbox4()
    
    def create_groupbox4(self):
        self.groupbox4 = tk.Frame(self.parent, width=1180, height=855, bg="#3b3b3b", relief="solid", bd=2, highlightbackground="white", highlightcolor="white", highlightthickness=2)
        self.groupbox4.place(x=10, y=135)
        self.groupbox4.pack_propagate(False)
        
        self.setup_custom_tabs()
    
    def setup_custom_tabs(self):
        # Bước 1: Tạo Tab Header Frame (chứa các nút tab)
        self.tab_header_frame = tk.Frame(self.groupbox4, height=40, bg="#3b3b3b")
        self.tab_header_frame.pack(fill="x", padx=5, pady=(5,0))
        self.tab_header_frame.pack_propagate(False)
        
        # Bước 2: Tạo Tab Content Frame (chứa nội dung tabs)
        self.tab_content_frame = tk.Frame(self.groupbox4, bg="#2b2b2b")
        self.tab_content_frame.pack(fill="both", expand=True, padx=5, pady=(0,5))
        
        # Bước 3: Khởi tạo variables quản lý tabs
        self.current_tab = "CẤU HÌNH REG"
        self.tab_buttons = {}
        self.tab_contents = {}
        
        # Bước 4: Tạo từng tab
        self.create_tab_button("CẤU HÌNH REG", 0)
        self.create_tab_content("CẤU HÌNH REG")
        
        self.create_tab_button("QUẢN LÝ LD/PHONE", 1)
        self.create_tab_content("QUẢN LÝ LD/PHONE")
        
        self.create_tab_button("QUẢN LÝ REG", 2)
        self.create_tab_content("QUẢN LÝ REG")
        
        # Bước 5: Hiển thị tab đầu tiên
        self.show_tab("CẤU HÌNH REG")
    
    def create_tab_button(self, tab_name, index):
        button = tk.Button(self.tab_header_frame, text=tab_name, width=18, height=1, bg="#0dcaf0", fg="white", font=("Arial", 12, "bold"), bd=2, relief="raised", command=lambda: self.show_tab(tab_name))
        button.place(x=index*191, y=5)
        self.tab_buttons[tab_name] = button
    
    def create_tab_content(self, tab_name):
        content_frame = tk.Frame(self.tab_content_frame, bg="#2b2b2b")
        self.tab_contents[tab_name] = content_frame
        
        if tab_name == "CẤU HÌNH REG":
            self.setup_cauhinhreg_content(content_frame)
        elif tab_name == "QUẢN LÝ LD/PHONE":
            self.setup_quanlyldphone_content(content_frame)
        elif tab_name == "QUẢN LÝ REG":
            self.setup_quanlyreg_tab_content(content_frame)
    
    def setup_cauhinhreg_content(self, content_frame):
        # Tạo các chức năng cho tab CẤU HÌNH REG
        self.groupbox1_manager = CauHinhRegGroupbox1(content_frame)
        self.groupbox2_manager = CauHinhRegGroupbox2(content_frame)
        self.groupbox3_manager = CauHinhRegGroupbox3(content_frame)
        self.groupbox4_manager = CauHinhRegGroupbox4(content_frame)
        self.groupbox5_manager = CauHinhRegGroupbox5(content_frame)
    
    def setup_quanlyldphone_content(self, content_frame):
        self.ldgroupbox1_manager = QuanLyLDPhoneGroupbox1(content_frame)
        self.ldgroupbox2_manager = QuanLyLDPhoneGroupbox2(content_frame)
    
    def setup_quanlyreg_tab_content(self, content_frame):
        self.groupbox1_manager = QuanLyRegGroupbox1(content_frame)
    
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