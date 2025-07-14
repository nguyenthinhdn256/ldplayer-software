import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class QuanLyLDPhoneGroupbox1:
    def __init__(self, parent):
        self.parent = parent
        self.app_selection_var = tk.StringVar(value="kantana")
        self.app_radio_buttons = []
        self.create_quanlyldphonegroupbox1()
    
    def create_quanlyldphonegroupbox1(self):
        self.quanlyldphonegroupbox1 = tk.Frame(self.parent, width=567, height=780, bg="#3b3b3b", relief="solid", bd=1, highlightbackground="white", highlightcolor="white", highlightthickness=1) 
        self.quanlyldphonegroupbox1.place(x=10, y=10)
        self.quanlyldphonegroupbox1.pack_propagate(False)
        
        tips_label = ctk.CTkLabel(self.quanlyldphonegroupbox1, text="HƯỚNG DẪN: CHUỘT PHẢI VÀO Ở TRỐNG ĐỂ TÌM KIẾM LẠI THIẾT BỊ PHONE HOẶC LDPLAYER", font=("Arial", 14, "bold"), text_color="white", wraplength=400)
        tips_label.pack(pady=8)

        self.bangdulieu_quanlyldphone()
        
    def bangdulieu_quanlyldphone(self):
        # ✅ SỬA PARENT WIDGET: dùng self.quanlyldphonegroupbox1 thay vì self.parent
        table_frame = tk.Frame(self.quanlyldphonegroupbox1, width=547, height=720, bg="#3b3b3b", relief="solid", bd=2, highlightbackground="#f8f9fa", highlightcolor="#f8f9fa", highlightthickness=2)        
        table_frame.place(x=10, y=50)  # Thay đổi từ y=50 thành y=70
        table_frame.pack_propagate(False)

        canvas = tk.Canvas(table_frame, bg="#3b3b3b", highlightthickness=0)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#3b3b3b")
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Tạo context menu và bind vào tất cả widgets
        self.create_context_menu(table_frame, canvas, scrollable_frame)

        # ✅ SỬA HEADERS CHO PHÙ HỢP VỚI QUẢN LÝ LD/PHONE
        headers = [("", 30), ("STT", 50), ("TRẠNG THÁI", 145), ("TÊN MÁY", 150), ("CHỌN", 150)]
        
        for col, (header, width) in enumerate(headers):
            header_label = tk.Label(scrollable_frame, text=header, font=('Arial', 10, 'bold'), bg="#0dcaf0", fg="black", width=width//8, relief="solid", bd=0, highlightbackground="white", highlightthickness=1)
            header_label.grid(row=0, column=col, sticky="ew")
           
        self.table_canvas = canvas
        self.table_scrollable_frame = scrollable_frame
        self.table_headers = headers
        self.table_data = []

    def create_context_menu(self, table_frame, canvas, scrollable_frame):
        context_menu = tk.Menu(table_frame, tearoff=0, font=("Arial", 10))
        context_menu.add_command(label="Tìm Lại LD/Phone", command=lambda: print("Tìm lại LD/Phone được thực hiện"))
        context_menu.add_command(label="Chọn Tất Cả", command=lambda: print("Chọn tất cả được thực hiện"))
        context_menu.add_command(label="Bỏ Chọn Tất Cả", command=lambda: print("Bỏ chọn tất cả được thực hiện"))
        
        def show_context_menu(event):
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
        
        table_frame.bind("<Button-3>", show_context_menu)
        canvas.bind("<Button-3>", show_context_menu)
        scrollable_frame.bind("<Button-3>", show_context_menu)