import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import os, sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CauHinhRegGroupbox5:
    def __init__(self, parent):
        self.parent = parent
        self.app_selection_var = tk.StringVar(value="")
        self.app_selection_var2 = tk.StringVar(value="")
        self.checkboxes = {}
        self.checkboxes2 = {}

        # THÊM CÁC BIẾN NÀY
        self.proxy_selection_var = self.app_selection_var  # Alias
        self.proxy_type_selection_var = self.app_selection_var2  # Alias
        self.border_frame3 = None
        self.border_frame3_widgets = []

        self.create_cauhinhreggroupbox5()
    
    def create_cauhinhreggroupbox5(self):
        self.cauhinhreggroupbox5 = tk.Frame(self.parent, width=1145, height=330, bg="#3b3b3b", relief="solid", bd=1, highlightbackground="white", highlightcolor="white", highlightthickness=1) 
        self.cauhinhreggroupbox5.place(x=10, y=460)
        self.cauhinhreggroupbox5.pack_propagate(False)

        # Khung 1
        self.border_frame1 = tk.Frame(self.cauhinhreggroupbox5, width=250, height=90, bg="#3b3b3b", highlightbackground="white", highlightcolor="white", highlightthickness=1, relief="solid")
        self.border_frame1.place(x=5, y=5)

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

        # Checkbox "Dùng Proxy", "dung_proxy"
        icon_dung_proxy = create_checkbox_icon(self.border_frame1, 15, 10, False)
        icon_dung_proxy.bind('<Button-1>', lambda e: on_checkbox_click("dung_proxy"))
        label_dung_proxy = tk.Label(self.border_frame1, text="Dùng Proxy", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_dung_proxy.place(x=40, y=7)
        label_dung_proxy.bind('<Button-1>', lambda e: on_checkbox_click("dung_proxy"))

        # Checkbox "Không Dùng Proxy", "khong_dung_proxy"
        icon_khong_dung_proxy = create_checkbox_icon(self.border_frame1, 15, 40, False)
        icon_khong_dung_proxy.bind('<Button-1>', lambda e: on_checkbox_click("khong_dung_proxy"))
        label_khong_dung_proxy = tk.Label(self.border_frame1, text="Không Dùng Proxy", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_khong_dung_proxy.place(x=40, y=37)
        label_khong_dung_proxy.bind('<Button-1>', lambda e: on_checkbox_click("khong_dung_proxy"))

        self.checkboxes.update({"dung_proxy": icon_dung_proxy, "khong_dung_proxy": icon_khong_dung_proxy})

        # Khung 2
        border_frame2 = tk.Frame(self.cauhinhreggroupbox5, width=250, height=220, bg="#3b3b3b", highlightbackground="white", highlightcolor="white", highlightthickness=1, relief="solid")
        border_frame2.place(x=5, y=100)

        # Khung 3        
        self.border_frame3 = tk.Frame(self.cauhinhreggroupbox5, width=450, height=315, bg="#3b3b3b", highlightbackground="white", highlightcolor="white", highlightthickness=1, relief="solid")
        self.border_frame3.place(x=260, y=5)

        # THÊM CODE CHO BORDER_FRAME3
        def on_checkbox_click2(value):
            self.xuly_checkbox2(value)

        # Checkbox "Host:Port:User:Pass", "host_port_user_pass"
        icon_host_port_user_pass = create_checkbox_icon(self.border_frame3, 15, 10, False)
        icon_host_port_user_pass.bind('<Button-1>', lambda e: on_checkbox_click2("host_port_user_pass"))
        label_host_port_user_pass = tk.Label(self.border_frame3, text="Host:Port:User:Pass", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_host_port_user_pass.place(x=40, y=7)
        label_host_port_user_pass.bind('<Button-1>', lambda e: on_checkbox_click2("host_port_user_pass"))

        # Checkbox "Host:Port (Nên Dùng)", "host_port"
        icon_host_port = create_checkbox_icon(self.border_frame3, 15, 40, False)
        icon_host_port.bind('<Button-1>', lambda e: on_checkbox_click2("host_port"))
        label_host_port = tk.Label(self.border_frame3, text="Host:Port (Nên Dùng)", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_host_port.place(x=40, y=37)
        label_host_port.bind('<Button-1>', lambda e: on_checkbox_click2("host_port"))

        # Checkbox "Vn2ray", "vn2ray"
        icon_vn2ray = create_checkbox_icon(self.border_frame3, 15, 70, False)
        icon_vn2ray.bind('<Button-1>', lambda e: on_checkbox_click2("vn2ray"))
        label_vn2ray = tk.Label(self.border_frame3, text="Vn2ray", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_vn2ray.place(x=40, y=67)
        label_vn2ray.bind('<Button-1>', lambda e: on_checkbox_click2("vn2ray"))

        # Checkbox "WW Proxy", "ww_proxy"
        icon_ww_proxy = create_checkbox_icon(self.border_frame3, 15, 100, False)
        icon_ww_proxy.bind('<Button-1>', lambda e: on_checkbox_click2("ww_proxy"))
        label_ww_proxy = tk.Label(self.border_frame3, text="WW Proxy", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_ww_proxy.place(x=40, y=97)
        label_ww_proxy.bind('<Button-1>', lambda e: on_checkbox_click2("ww_proxy"))

        # Checkbox "Proxy No1", "proxy_no1"
        icon_proxy_no1 = create_checkbox_icon(self.border_frame3, 15, 130, False)
        icon_proxy_no1.bind('<Button-1>', lambda e: on_checkbox_click2("proxy_no1"))
        label_proxy_no1 = tk.Label(self.border_frame3, text="Proxy No1", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_proxy_no1.place(x=40, y=127)
        label_proxy_no1.bind('<Button-1>', lambda e: on_checkbox_click2("proxy_no1"))

        # Checkbox "Super Proxy", "super_proxy"
        icon_super_proxy = create_checkbox_icon(self.border_frame3, 15, 160, False)
        icon_super_proxy.bind('<Button-1>', lambda e: on_checkbox_click2("super_proxy"))
        label_super_proxy = tk.Label(self.border_frame3, text="Super Proxy", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_super_proxy.place(x=40, y=157)
        label_super_proxy.bind('<Button-1>', lambda e: on_checkbox_click2("super_proxy"))

        # Checkbox "Windscribe VPN", "windscribe_vpn"
        icon_windscribe_vpn = create_checkbox_icon(self.border_frame3, 15, 190, False)
        icon_windscribe_vpn.bind('<Button-1>', lambda e: on_checkbox_click2("windscribe_vpn"))
        label_windscribe_vpn = tk.Label(self.border_frame3, text="Windscribe VPN", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_windscribe_vpn.place(x=40, y=187)
        label_windscribe_vpn.bind('<Button-1>', lambda e: on_checkbox_click2("windscribe_vpn"))

        self.checkboxes2.update({"host_port_user_pass": icon_host_port_user_pass, "host_port": icon_host_port, "vn2ray": icon_vn2ray, "ww_proxy": icon_ww_proxy, "proxy_no1": icon_proxy_no1, "super_proxy": icon_super_proxy, "windscribe_vpn": icon_windscribe_vpn})

        # BUTTON "CHIA DỮ LIỆU"
        chia_du_lieu_label = tk.Label(self.border_frame3, text="Chia Dữ Liệu:", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        chia_du_lieu_label.place(x=15, y=280)
        # self.border_frame3_widgets.append(chia_du_lieu_label)
        
        chia_du_lieu_button = tk.Button(self.border_frame3, text="Chia", bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=8, height=1, command=self.open_chia_proxy_window) 
        chia_du_lieu_button.place(x=145, y=280)
        # self.border_frame3_widgets.append(chia_du_lieu_button)

        # LƯU TẤT CẢ WIDGETS VÀO DANH SÁCH
        for checkbox_name, checkbox_canvas in self.checkboxes2.items():
            self.border_frame3_widgets.append(checkbox_canvas)
        
        # Labels
        self.border_frame3_widgets.append(label_host_port_user_pass)
        self.border_frame3_widgets.append(label_host_port)
        self.border_frame3_widgets.append(label_vn2ray)
        self.border_frame3_widgets.append(label_ww_proxy)
        self.border_frame3_widgets.append(label_proxy_no1)
        self.border_frame3_widgets.append(label_super_proxy)
        self.border_frame3_widgets.append(label_windscribe_vpn)
        self.border_frame3_widgets.append(chia_du_lieu_label)
        self.border_frame3_widgets.append(chia_du_lieu_button)

        self.update_border_frame3_state()

    def open_chia_proxy_window(self):
        """Mở giao diện chia proxy"""
        try:
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'script_phu'))
            chiaproxy_module = __import__('chiaproxy')
            chia_window = tk.Toplevel(self.parent)
            chia_manager = chiaproxy_module.LDPlayerManager(chia_window)
        except Exception as e:
            print(f"ERROR: Không thể mở cửa sổ chia proxy: {str(e)}")

    def xuly_checkbox(self, value):  # Cho border_frame1
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

        # GỌI UPDATE STATE
        self.update_border_frame3_state()

    def xuly_checkbox2(self, value):  # Cho border_frame3
        current_value = self.app_selection_var2.get()
        if current_value == value:
            self.app_selection_var2.set("")
        else:
            self.app_selection_var2.set(value)
        selected_value = self.app_selection_var2.get()
        for checkbox_name, checkbox_canvas in self.checkboxes2.items():
            checkbox_canvas.delete("all")
            checkbox_canvas.create_rectangle(2, 2, 16, 16, outline="white", fill="", width=2)
            if checkbox_name == selected_value:
                checkbox_canvas.create_line(5, 9, 8, 12, fill="white", width=2)
                checkbox_canvas.create_line(8, 12, 13, 6, fill="white", width=2)

    ##############################################
    # Xử lý proxy
    def update_border_frame3_state(self):
        """Cập nhật trạng thái enable/disable của border_frame3 dựa trên proxy selection"""
        try:
            # SỬA: Sử dụng đúng biến
            selected_proxy = self.app_selection_var.get()  # Thay vì self.proxy_selection_var
            enable_frame3 = (selected_proxy == "dung_proxy")
            
            if enable_frame3:
                # ENABLE: Màu bình thường và cho phép tương tác
                if self.border_frame3:
                    self.border_frame3.config(highlightbackground="white")  # Thay vì "#3b3b3b"
                for widget in self.border_frame3_widgets:
                    if hasattr(widget, 'config'):
                        try:
                            if isinstance(widget, tk.Label):
                                widget.config(fg='white', state='normal')
                            elif isinstance(widget, tk.Button):
                                widget.config(state='normal', bg='#404040')
                            elif isinstance(widget, tk.Canvas):
                                widget.config(state='normal')
                        except:
                            pass
                logger.info("Enabled border_frame3 - User can select proxy type")

            else:
                # DISABLE: Màu xám và không cho phép tương tác
                if self.border_frame3:
                    self.border_frame3.config(highlightbackground="#666666")
                for widget in self.border_frame3_widgets:
                    if hasattr(widget, 'config'):
                        try:
                            if isinstance(widget, tk.Label):
                                widget.config(fg='#666666', state='disabled')
                            elif isinstance(widget, tk.Button):
                                widget.config(state='disabled', bg='#666666')
                            elif isinstance(widget, tk.Canvas):
                                widget.config(state='disabled')
                        except:
                            pass
                # RESET PROXY TYPE SELECTION KHI DISABLE
                self.app_selection_var2.set("")  # Thay vì self.proxy_type_selection_var
                self.update_proxy_type_checkboxes()  # Thêm method này
                logger.info("Disabled border_frame3 - No proxy will be used")

        except Exception as e:
            logger.error(f"Error updating border_frame3 state: {e}")
            
    def update_proxy_type_checkboxes(self):
        """Cập nhật hiển thị checkboxes trong border_frame3"""
        selected_value = self.app_selection_var2.get()
        for checkbox_name, checkbox_canvas in self.checkboxes2.items():
            checkbox_canvas.delete("all")
            checkbox_canvas.create_rectangle(2, 2, 16, 16, outline="white", fill="", width=2)
            if checkbox_name == selected_value:
                checkbox_canvas.create_line(5, 9, 8, 12, fill="white", width=2)
                checkbox_canvas.create_line(8, 12, 13, 6, fill="white", width=2)
                
    def is_border_frame3_enabled(self):
        """Kiểm tra border_frame3 có được enable không"""
        return self.app_selection_var.get() == "dung_proxy"

    def is_proxy_enabled(self):
        """Kiểm tra user có chọn dùng proxy không"""
        return self.app_selection_var.get() == "dung_proxy"

    def get_proxy_configuration(self):
        """Lấy cấu hình proxy đầy đủ cho script chính"""
        try:
            use_proxy = self.is_proxy_enabled()
            if use_proxy:
                proxy_type = self.app_selection_var2.get()  # Thay vì self.get_proxy_type_selected_value()
                return {"use_proxy": True, "proxy_type": proxy_type, "enabled": proxy_type != ""}
            else:
                return {"use_proxy": False, "proxy_type": "", "enabled": False}
        except Exception as e:
            logger.error(f"Error getting proxy configuration: {e}")
            return {"use_proxy": False, "proxy_type": "", "enabled": False}
        
    ##############################################