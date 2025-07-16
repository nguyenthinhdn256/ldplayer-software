import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class QuanLyRegGroupbox1:
    def __init__(self, parent):
        self.parent = parent
        self.app_selection_var = tk.StringVar(value="kantana")
        self.app_radio_buttons = []
        self.table_rows = []
        self.bangdulieu_quanlyreg()

    def create_quanlyldphonegroupbox1(self):
        self.quanlyldphonegroupbox1 = tk.Frame(self.parent, width=567, height=780, bg="#3b3b3b", relief="solid", bd=1, highlightbackground="white", highlightcolor="white", highlightthickness=1) 
        self.quanlyldphonegroupbox1.place(x=10, y=10)
        self.quanlyldphonegroupbox1.pack_propagate(False)
        
        tips_label = ctk.CTkLabel(self.quanlyldphonegroupbox1, text="HƯỚNG DẪN: CHUỘT PHẢI VÀO Ở TRỐNG ĐỂ TÌM KIẾM LẠI THIẾT BỊ PHONE HOẶC LDPLAYER", font=("Arial", 14, "bold"), text_color="white", wraplength=400)
        tips_label.pack(pady=8)

        self.bangdulieu_quanlyreg()

    def bangdulieu_quanlyreg(self):
        table_frame = tk.Frame(self.parent, width=1155, height=785, bg="#3b3b3b", relief="solid", bd=2, highlightbackground="#f8f9fa", highlightcolor="#f8f9fa", highlightthickness=2)
        table_frame.place(x=5, y=5)
        table_frame.pack_propagate(False)
        h_scrollbar = tk.Scrollbar(table_frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        canvas = tk.Canvas(table_frame, bg="#3b3b3b", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=h_scrollbar.set)
        scrollbar.configure(command=canvas.yview)
        h_scrollbar.configure(command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg="#3b3b3b")
        def configure_scroll_region(event): canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        headers = [("", 30), ("STT", 50), ("TRẠNG THÁI", 300), ("TÊN MÁY", 150), ("KẾT QUẢ", 120), ("HỌ", 100), ("TÊN", 100), ("MẬT KHẨU", 150), ("EMAIL/SDT", 250), ("UID", 150), ("COOKIE", 200), ("TOKEN", 200), ("PROXY", 200)]
        for col, (header, width) in enumerate(headers):
            header_label = tk.Label(scrollable_frame, text=header, font=('Arial', 10, 'bold'), bg="#0dcaf0", fg="black", width=width//8, relief="solid", bd=0, highlightbackground="white", highlightthickness=1)
            header_label.grid(row=0, column=col, sticky="ew")
        self.table_canvas = canvas
        self.table_scrollable_frame = scrollable_frame
        self.table_headers = headers
        self.table_data = []
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def create_rows_from_so_ld(self, so_ld_count):
        """Tạo rows và lưu trữ widget references"""
        # Xóa các rows cũ
        for widget in self.table_scrollable_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0: 
                widget.destroy()
        
        # Reset table_rows
        self.table_rows = []
        
        # Tạo rows mới
        for row in range(1, so_ld_count + 1):
            cells = ["", str(row), "", "", "", "", "", "", "", "", "", "", ""]
            row_widgets = []
            
            for col, (cell_data, (_, width)) in enumerate(zip(cells, self.table_headers)):
                cell_label = tk.Label(self.table_scrollable_frame, text=cell_data, font=('Arial', 9), bg="#3b3b3b", fg="white", width=width//8, relief="solid", bd=0, anchor="center", highlightbackground="white", highlightthickness=1)
                cell_label.grid(row=row, column=col, sticky="ew")
                row_widgets.append(cell_label)
            
            self.table_rows.append(row_widgets)
        
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

    # Cập nhập status từ table_status_manager.py lên giao diện gui
    def update_table_row_safe(self, row_index: int, status_data: dict):
        """Thread-safe method để cập nhật table từ background thread"""
        def update_ui():
            self.update_table_row(row_index, status_data)
        
        # Tìm root window để gọi after
        root = self.parent
        while root.master:
            root = root.master
        
        # Schedule UI update trên main thread
        root.after(0, update_ui)

    def update_table_row(self, row_index: int, status_data: dict):
        """Cập nhật một row trong bảng với dữ liệu mới - CHỈ ĐƯỢC GỌI TỪ MAIN THREAD"""
        try:
            if row_index < 0 or row_index >= len(self.table_rows):
                return
            
            row_widgets = self.table_rows[row_index]
            field_names = ["", "stt", "trang_thai", "ten_may", "ket_qua", "ho", "ten", "mat_khau", "email_sdt", "uid", "cookie", "token", "proxy"]
            
            for col, field_name in enumerate(field_names):
                if col < len(row_widgets) and field_name in status_data:
                    old_text = row_widgets[col].cget("text")
                    new_text = status_data[field_name]
                    row_widgets[col].config(text=new_text)
                    print(f"DEBUG: Updated row {row_index}, col {col} ({field_name}): '{old_text}' -> '{new_text}'")
            
            
            # Cập nhật scroll region
            self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
            
        except Exception as e:
            print(f"Error updating table row {row_index}: {e}")

    
