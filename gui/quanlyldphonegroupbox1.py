import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import threading
import subprocess


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
        context_menu.add_command(label="Tìm Lại LD/Phone", command=self.on_find_devices_click)
        context_menu.add_command(label="Chọn Tất Cả", command=self.select_all_devices)
        context_menu.add_command(label="Bỏ Chọn Tất Cả", command=self.deselect_all_devices)
        
        def show_context_menu(event):
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
        
        table_frame.bind("<Button-3>", show_context_menu)
        canvas.bind("<Button-3>", show_context_menu)
        scrollable_frame.bind("<Button-3>", show_context_menu)

    def on_find_devices_click(self): # Tìm kiếm thiết bị đang chạy
        threading.Thread(target=self.scan_running_devices, daemon=True).start()

    def scan_running_devices(self): # Quét thiết bị đang chạy
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]
                devices = []
                for line in lines:
                    if line.strip() and '\t' in line:
                        device_id, status = line.strip().split('\t')
                        if status == 'device':
                            if device_id.startswith('emulator-'):
                                port = device_id.split('-')[1]
                                emulator_name = f"emulator-{port}"
                            else:
                                emulator_name = device_id
                            devices.append({'id': device_id, 'status': 'Live', 'name': emulator_name})
                
                # Sắp xếp thiết bị theo port từ thấp đến cao
                devices.sort(key=lambda x: int(x['name'].split('-')[1]) if x['name'].startswith('emulator-') else 99999)
                self.parent.after(0, lambda: self.update_device_table(devices))
            else:
                self.parent.after(0, lambda: self.update_device_table([]))
        except subprocess.TimeoutExpired:
            self.parent.after(0, lambda: self.update_device_table([]))
        except FileNotFoundError:
            self.parent.after(0, lambda: self.update_device_table([]))
        except Exception as e:
            self.parent.after(0, lambda: self.update_device_table([]))

    def update_device_table(self, devices): # Update các thiết bị đang chạy lên bảng
        for widget in self.table_scrollable_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        self.device_data = []
        self.device_checkboxes = {}
        row = 1
        for device in devices:
            checkbox_var = tk.BooleanVar()
            self.device_checkboxes[device['id']] = checkbox_var
            cells = ["", str(row), device['status'], device['name'], ""]
            for col, (cell_data, (_, width)) in enumerate(zip(cells, self.table_headers)):
                if col == 4:
                    checkbox_label = tk.Label(self.table_scrollable_frame, text="", font=('Arial', 9), bg="#3b3b3b", fg="white", width=width//8, relief="solid", bd=1, anchor="center", highlightbackground="white", highlightcolor="white", highlightthickness=1)
                    checkbox_label.grid(row=row, column=col, sticky="nsew", padx=0, pady=0)
                    checkbox = tk.Checkbutton(checkbox_label, variable=checkbox_var, bg="#3b3b3b", fg="white", selectcolor="#3b3b3b", activebackground="#3b3b3b")
                    checkbox.pack(expand=True)
                else:
                    cell_label = tk.Label(self.table_scrollable_frame, text=cell_data, font=('Arial', 9), bg="#3b3b3b", fg="white", width=width//8, relief="solid", bd=1, anchor="center", highlightbackground="white", highlightcolor="white", highlightthickness=1)
                    cell_label.grid(row=row, column=col, sticky="nsew", padx=0, pady=0)
            
            self.device_data.append({'id': device['id'], 'status': device['status'], 'name': device['name'], 'checkbox_var': checkbox_var})
            row += 1
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

    def select_all_devices(self):
        for checkbox_var in self.device_checkboxes.values():
            checkbox_var.set(True)

    def deselect_all_devices(self):
        for checkbox_var in self.device_checkboxes.values():
            checkbox_var.set(False)