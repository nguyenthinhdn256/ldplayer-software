import tkinter as tk
from tkinter import ttk, messagebox
from gui.groupbox_4 import Groupbox4Manager
from gui.cauhinhreggroupbox3 import CauHinhRegGroupbox3
from utils.apk_manager import ApkManager
import threading
import subprocess, time
from typing import Optional, Dict, Any


class Groupbox2Manager:
    def __init__(self, parent):
        self.parent = parent
        self.create_groupbox2()
    
    def create_groupbox2(self):
        self.groupbox2 = tk.Frame(self.parent, width=430, height=120, bg="#3b3b3b", relief="solid", bd=2, highlightbackground="white", highlightcolor="white", highlightthickness=2)
        self.groupbox2.place(x=320, y=5)
        self.groupbox2.pack_propagate(False)

        # App Settings button
        self.settings_button = tk.Button(self.groupbox2, text="App Settings", bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=15, height=1, command=self.process_app_settings)
        self.settings_button.place(x=10, y=4)

        # Save ADB button
        self.save_button = tk.Button(self.groupbox2, text="Connect ADB", bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=15, height=1, command=self.connect_adb_devices)
        self.save_button.place(x=10, y=42)
        
        # Start Appium button 
        self.appium_button = tk.Button(self.groupbox2, text="Start Appium", bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=15, height=1)
        self.appium_button.place(x=10, y=82)

        # START REG button
        self.start_reg_button = tk.Button(self.groupbox2, text="Start", bg='#dc3545', fg='white', font=('Arial', 10, 'bold'), width=15, height=1, command=self.on_start_reg_click)
        self.start_reg_button.place(x=290, y=4)

    def connect_adb_devices(self):
        def worker():
            try:
                app_window = self.parent
                while app_window and not hasattr(app_window, 'groupbox4_manager'):
                    app_window = app_window.master
                if not app_window or not hasattr(app_window, 'groupbox4_manager'):
                    self.parent.after(0, lambda: messagebox.showerror("Lỗi", "Không tìm thấy groupbox4_manager."))
                    return
                groupbox4_manager = app_window.groupbox4_manager
                if groupbox4_manager.current_tab != "QUẢN LÝ LD/PHONE":
                    self.parent.after(0, lambda: messagebox.showwarning("Cảnh báo", f"Tab hiện tại: {groupbox4_manager.current_tab}. Vui lòng chuyển sang tab 'QUẢN LÝ LD/PHONE' và quét thiết bị trước."))
                    return
                device_manager = None
                if hasattr(groupbox4_manager, 'ldgroupbox1_manager'):
                    device_manager = groupbox4_manager.ldgroupbox1_manager
                if not device_manager:
                    for attr_name in dir(groupbox4_manager):
                        if not attr_name.startswith('_'):
                            try:
                                attr_value = getattr(groupbox4_manager, attr_name)
                                if hasattr(attr_value, '__class__') and attr_value.__class__.__name__ == 'QuanLyLDPhoneGroupbox1':
                                    device_manager = attr_value
                                    break
                            except:
                                pass
                if not device_manager:
                    self.parent.after(0, lambda: messagebox.showerror("Lỗi", "Không tìm thấy QuanLyLDPhoneGroupbox1 manager. Vui lòng đảm bảo đã ở tab 'QUẢN LÝ LD/PHONE' và quét thiết bị."))
                    return
                if not hasattr(device_manager, 'device_checkboxes') or not device_manager.device_checkboxes:
                    self.parent.after(0, lambda: messagebox.showwarning("Cảnh báo", "Chưa có thiết bị nào được quét. Vui lòng chuột phải vào bảng và chọn 'Tìm Lại LD/Phone'."))
                    return
                selected_devices = [device_id for device_id, checkbox_var in device_manager.device_checkboxes.items() if checkbox_var.get()]
                if not selected_devices:
                    self.parent.after(0, lambda: messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một thiết bị để kết nối."))
                    return
                adb_devices_result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=10)
                if adb_devices_result.returncode != 0:
                    self.parent.after(0, lambda: messagebox.showerror("Lỗi", "Không thể thực thi lệnh ADB. Vui lòng kiểm tra ADB đã được cài đặt."))
                    return
                existing_devices = {}
                for line in adb_devices_result.stdout.strip().split('\n')[1:]:
                    if line.strip() and '\t' in line:
                        device_id, status = line.strip().split('\t')
                        existing_devices[device_id] = status
                connection_results = []
                successful_connections = 0
                for selected_device in selected_devices:
                    try:
                        if selected_device.startswith('emulator-'):
                            port = selected_device.split('-')[1]
                            adb_device_id = f"127.0.0.1:{port}"
                            if selected_device in existing_devices and existing_devices[selected_device] == 'device':
                                connection_results.append(f"✅ {selected_device}: Đã kết nối")
                                successful_connections += 1
                            elif adb_device_id in existing_devices and existing_devices[adb_device_id] == 'device':
                                connection_results.append(f"✅ {selected_device} → {adb_device_id}: Đã kết nối")
                                successful_connections += 1
                            else:
                                connect_result = subprocess.run(['adb', 'connect', adb_device_id], capture_output=True, text=True, timeout=10)
                                if 'already connected' in connect_result.stdout.lower() or 'connected to' in connect_result.stdout.lower():
                                    connection_results.append(f"✅ {selected_device} → {adb_device_id}: Kết nối thành công")
                                    successful_connections += 1
                                else:
                                    connection_results.append(f"❌ {selected_device} → {adb_device_id}: Kết nối thất bại")
                        else:
                            if selected_device in existing_devices and existing_devices[selected_device] == 'device':
                                connection_results.append(f"✅ {selected_device}: Đã kết nối")
                                successful_connections += 1
                            else:
                                connection_results.append(f"❌ {selected_device}: Thiết bị không khả dụng")
                    except Exception as e:
                        connection_results.append(f"❌ {selected_device}: Lỗi kết nối")
                total_selected = len(selected_devices)
                if successful_connections == total_selected:
                    status_icon = "🎉"
                    status_text = "Hoàn hảo!"
                elif successful_connections > 0:
                    status_icon = "⚠️"
                    status_text = "Một phần thành công"
                else:
                    status_icon = "❌"
                    status_text = "Thất bại"
                result_message = f"{status_icon} Kết quả Connect ADB - {status_text}\n\n{chr(10).join(connection_results)}\n\nTổng kết: {successful_connections}/{total_selected} thiết bị kết nối thành công."
                self.parent.after(0, lambda: messagebox.showinfo("Kết quả Connect ADB", result_message))
            except subprocess.TimeoutExpired:
                self.parent.after(0, lambda: messagebox.showerror("Lỗi", "Timeout khi thực thi lệnh ADB."))
            except FileNotFoundError:
                self.parent.after(0, lambda: messagebox.showerror("Lỗi", "Không tìm thấy ADB. Vui lòng cài đặt Android SDK Platform Tools."))
            except Exception as e:
                self.parent.after(0, lambda: messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}"))
        threading.Thread(target=worker, daemon=True).start()

    # def on_start_reg_click(self):
    #     try:
    #         app_window = self.parent
    #         while app_window and not hasattr(app_window, 'groupbox4_manager'):
    #             app_window = app_window.master
    #         if app_window and hasattr(app_window, 'groupbox4_manager'):
    #             groupbox4_manager = app_window.groupbox4_manager
    #             if hasattr(groupbox4_manager, 'groupbox3_manager') and hasattr(groupbox4_manager.groupbox3_manager, 'so_ld_var'):
    #                 so_ld_value = int(groupbox4_manager.groupbox3_manager.so_ld_var.get())
    #                 groupbox4_manager.show_tab("QUẢN LÝ REG")
    #                 if hasattr(groupbox4_manager, 'groupbox1_manager'):
    #                     groupbox4_manager.groupbox1_manager.create_rows_from_so_ld(so_ld_value)
    #     except Exception as e:
    #         print(f"Error in start reg click: {e}")

    def on_start_reg_click(self):
        """Thực hiện các bước UI trước, sau đó gọi worker"""
        try:
            # === BƯỚC 1: Thực hiện logic UI cũ ===
            app_window = self.parent
            while app_window and not hasattr(app_window, 'groupbox4_manager'):
                app_window = app_window.master
                
            if app_window and hasattr(app_window, 'groupbox4_manager'):
                groupbox4_manager = app_window.groupbox4_manager
                
                if hasattr(groupbox4_manager, 'groupbox3_manager') and hasattr(groupbox4_manager.groupbox3_manager, 'so_ld_var'):
                    so_ld_value = int(groupbox4_manager.groupbox3_manager.so_ld_var.get())
                    
                    # Chuyển sang tab "QUẢN LÝ REG"
                    groupbox4_manager.show_tab("QUẢN LÝ REG")
                    
                    # Tạo bảng dữ liệu
                    if hasattr(groupbox4_manager, 'groupbox1_manager'):
                        groupbox4_manager.groupbox1_manager.create_rows_from_so_ld(so_ld_value)
                        
                    # messagebox.showinfo("Thông báo", f"Đã tạo bảng với {so_ld_value} rows.\nBắt đầu khởi động worker...")
            
            # === BƯỚC 2: Import từ thư mục service ===
            from service import facebook_main
            
            starter = facebook_main.FacebookRegistrationStarter(self.parent)
            success = starter.call_worker_only()
            
            if success:
                time.sleep(1)
                # messagebox.showinfo("Thành công", "Worker đa tiến trình đã được khởi tạo!")
            else:
                messagebox.showerror("Lỗi", "Không thể khởi tạo worker")
                
        except Exception as e:
            print(f"Error in start reg click: {e}")
            messagebox.showerror("Lỗi", f"Lỗi khởi động: {str(e)}")

    #############################################
    # Xử lý Appium server
    # def toggle_appium_server(self):
    #     """Toggle Appium server start/stop với dynamic device management"""
    #     def worker():
    #         try:
    #             if self.appium_manager.is_running:
    #                 # STOP ALL SERVERS
    #                 self.parent.after(0, lambda: self.update_appium_button("Stopping...", "#ffc107"))
    #                 result = self.appium_manager.stop_all_servers()
                    
    #                 if result["success"]:
    #                     self.parent.after(0, lambda: self.update_appium_button("Start Appium", "#404040"))
    #                     self.parent.after(0, lambda: messagebox.showinfo("Success", result["message"]))
    #                 else:
    #                     self.parent.after(0, lambda: self.update_appium_button("Start Appium", "#404040"))
    #                     self.parent.after(0, lambda: messagebox.showerror("Error", result["message"]))
    #             else:
    #                 # START SERVERS FOR SELECTED DEVICES
    #                 self.parent.after(0, lambda: self.update_appium_button("Starting...", "#ffc107"))
                    
    #                 # Lấy danh sách devices đã chọn
    #                 selected_devices = self.get_selected_devices()
                    
    #                 if not selected_devices:
    #                     self.parent.after(0, lambda: self.update_appium_button("Start Appium", "#404040"))
    #                     self.parent.after(0, lambda: messagebox.showwarning("Warning", 
    #                         "No devices selected!\nPlease go to 'QUẢN LÝ LD/PHONE' tab and select devices first."))
    #                     return
                    
    #                 # Khởi động servers cho devices đã chọn
    #                 result = self.appium_manager.start_servers_for_devices(selected_devices, max_workers=10)
                    
    #                 if result["success"]:
    #                     self.parent.after(0, lambda: self.update_appium_button("Stop Appium", "#dc3545"))
    #                     message = f"{result['message']}\n\nPort mapping:\n"
    #                     for device_id in selected_devices:
    #                         port = self.appium_manager.get_appium_port_for_device(device_id)
    #                         message += f"• {device_id} → Port {port}\n"
    #                     self.parent.after(0, lambda: messagebox.showinfo("Success", message))
    #                 else:
    #                     self.parent.after(0, lambda: self.update_appium_button("Start Appium", "#404040"))
    #                     self.parent.after(0, lambda: messagebox.showerror("Error", result["message"]))
                        
    #         except Exception as e:
    #             self.parent.after(0, lambda: self.update_appium_button("Start Appium", "#404040"))
    #             self.parent.after(0, lambda: messagebox.showerror("Error", f"Unexpected error: {str(e)}"))
        
    #     # Run in separate thread to avoid GUI freezing
    #     threading.Thread(target=worker, daemon=True).start()

    def get_selected_devices(self) -> list:
        """Lấy danh sách devices đã được chọn từ tab QUẢN LÝ LD/PHONE"""
        try:
            # Tìm groupbox4_manager
            app_window = self.parent
            while app_window and not hasattr(app_window, 'groupbox4_manager'):
                app_window = app_window.master
                
            if not app_window or not hasattr(app_window, 'groupbox4_manager'):
                return []
                
            groupbox4_manager = app_window.groupbox4_manager
            
            # Tìm device manager
            if hasattr(groupbox4_manager, 'ldgroupbox1_manager'):
                device_manager = groupbox4_manager.ldgroupbox1_manager
                if hasattr(device_manager, 'device_checkboxes'):
                    return [device_id for device_id, checkbox_var in device_manager.device_checkboxes.items() 
                           if checkbox_var.get()]
            
            return []
            
        except Exception as e:
            print(f"Error getting selected devices: {e}")
            return []

    # def start_appium_for_device(self, device_id: str) -> Dict[str, Any]:
    #     """Khởi động Appium server cho device cụ thể (gọi từ registration worker)"""
    #     try:
    #         result = self.appium_manager.start_server_for_device(device_id)
    #         return result
    #     except Exception as e:
    #         return {"success": False, "message": f"Error starting Appium for {device_id}: {str(e)}"}

    # def get_appium_url_for_device(self, device_id: str) -> Optional[str]:
    #     """Lấy Appium server URL cho device cụ thể"""
    #     return self.appium_manager.get_device_server_url(device_id)
    
    # def update_appium_button(self, text: str, color: str):
    #     """Update button text and color"""
    #     self.appium_button.config(text=text, bg=color)
    #############################################


    #############################################
    # Xử lý cài app trong App Settings
    def process_app_settings(self):
        """Xử lý App Settings theo logic yêu cầu"""
        def worker():
            try:
                manager = ApkManager()
                
                # Kiểm tra có device nào kết nối không
                devices = manager.get_connected_devices()
                if not devices:
                    self.parent.after(0, lambda: messagebox.showwarning("Warning", 
                        "No devices connected!\nPlease click 'Connect ADB' button first."))
                    return
                
                # Hiển thị thông báo đang xử lý
                self.parent.after(0, lambda: messagebox.showinfo("Processing", 
                    f"Processing {len(devices)} device(s)...\nVui lòng đợi cài đặt hoàn thành."))
                
                # Xử lý tất cả devices
                results = manager.process_all_devices()
                
            except Exception as e:
                self.parent.after(0, lambda: messagebox.showerror("Error", f"Error: {str(e)}"))
        
        threading.Thread(target=worker, daemon=True).start()

    #############################################