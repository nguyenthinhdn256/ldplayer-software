import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import shutil
from datetime import datetime
import json

class LDPlayerManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Chia Dữ Liệu")
        self.root.geometry("800x900")
        self.root.configure(bg='#f0f0f0')
        
        # Cấu hình lưu trữ
        self.configs = {
            'host:port': {'data': [], 'split': 1},
            'vn2ray': {'data': [], 'split': 1},
            'wwproxy': {'data': [], 'split': 1},
            'proxyno1': {'data': [], 'split': 1}
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title frame - fixed position
        title_frame = tk.Frame(self.root, bg='#3b3b3b', height=80)
        title_frame.place(x=0, y=0, width=800, height=80)
        
        title_label = tk.Label(title_frame, text="QUẢN LÝ DỮ LIỆU", 
                              font=('Arial', 24, 'bold'), fg='white', bg='#3b3b3b')
        title_label.place(x=400, y=25, anchor='center')
        
        subtitle_label = tk.Label(title_frame, text="Tool quản lý dữ liệu folders LDPlayer", 
                                 font=('Arial', 12), fg='#ecf0f1', bg='#3b3b3b')
        subtitle_label.place(x=400, y=55, anchor='center')
        
        # Main content area - sử dụng Frame thông thường thay vì Canvas
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.place(x=0, y=80, width=800, height=820)
        
        # Folder count section
        folder_frame = tk.LabelFrame(main_frame, text="CẤU HÌNH FOLDER", 
                                    font=('Arial', 12, 'bold'), fg='#2c3e50', bg='#f8f9fa')
        folder_frame.place(x=20, y=20, width=760, height=100)
        
        folder_label = tk.Label(folder_frame, text="Số folder LDPlayer", 
                               font=('Arial', 12, 'bold'), bg='#f8f9fa')
        folder_label.place(x=15, y=5)
        
        self.folder_count = tk.StringVar(value="1")
        folder_spinbox = tk.Spinbox(folder_frame, from_=1, to=40, width=10, 
                                   textvariable=self.folder_count, font=('Arial', 11))
        folder_spinbox.place(x=15, y=45)
        
        self.folder_info = tk.Label(folder_frame, text="(Từ LDPlayer-1 đến LDPlayer-xx)", 
                                   font=('Arial', 10), fg='#666', bg='#f8f9fa')
        self.folder_info.place(x=150, y=47)
        
        self.folder_count.trace('w', self.update_folder_info)
        
        # Delete section
        delete_frame = tk.LabelFrame(main_frame, text="XÓA DỮ LIỆU", 
                                    font=('Arial', 12, 'bold'), fg='#2c3e50', bg='#f8f9fa')
        delete_frame.place(x=20, y=130, width=760, height=210)
        
        self.enable_delete = tk.BooleanVar()
        delete_check = tk.Checkbutton(delete_frame, text="Xóa proxy/key proxy", 
                                     variable=self.enable_delete, font=('Arial', 12, 'bold'),
                                     bg='#f8f9fa', command=self.toggle_delete_options)
        delete_check.place(x=15, y=5)
        
        self.delete_options_frame = tk.Frame(delete_frame, bg='white', relief='ridge', bd=1)
        
        self.delete_gmail = tk.BooleanVar()
        self.delete_proxy = tk.BooleanVar()
        self.delete_ipport = tk.BooleanVar()
        self.delete_wwproxy = tk.BooleanVar()
        
        gmail_del_check = tk.Checkbutton(self.delete_options_frame, text="Host:Port", 
                                        variable=self.delete_gmail, font=('Arial', 10), bg='white')
        gmail_del_check.place(x=20, y=10)
        
        proxy_del_check = tk.Checkbutton(self.delete_options_frame, text="Vn2ray", 
                                        variable=self.delete_proxy, font=('Arial', 10), bg='white')
        proxy_del_check.place(x=20, y=35)
        
        ipport_del_check = tk.Checkbutton(self.delete_options_frame, text="WW Proxy", 
                                         variable=self.delete_ipport, font=('Arial', 10), bg='white')
        ipport_del_check.place(x=20, y=60)
        
        wwproxy_del_check = tk.Checkbutton(self.delete_options_frame, text="Proxy No1", 
                                          variable=self.delete_wwproxy, font=('Arial', 10), bg='white')
        wwproxy_del_check.place(x=20, y=85)
        
        # Add data section
        add_frame = tk.LabelFrame(main_frame, text="➕ Thêm dữ liệu file", 
                                 font=('Arial', 12, 'bold'), fg='#2c3e50', bg='#f8f9fa')
        add_frame.place(x=20, y=350, width=760, height=410)
        
        self.enable_add = tk.BooleanVar()
        add_check = tk.Checkbutton(add_frame, text="Thêm proxy/key proxy", 
                                  variable=self.enable_add, font=('Arial', 11, 'bold'),
                                  bg='#f8f9fa', command=self.toggle_add_options)
        add_check.place(x=15, y=5)
        
        # Container cho các file type checkboxes
        self.add_options_frame = tk.Frame(add_frame, bg='white', relief='ridge', bd=1)
        
        self.add_hostport = tk.BooleanVar()
        self.add_vn2ray = tk.BooleanVar()
        self.add_wwproxy = tk.BooleanVar()
        self.add_proxyno1 = tk.BooleanVar()
        
        # File type checkboxes
        hostport_check = tk.Checkbutton(self.add_options_frame, text="Host:Port", 
                                       variable=self.add_hostport, font=('Arial', 10), bg='white',
                                       command=lambda: self.toggle_file_config('host:port'))
        hostport_check.place(x=10, y=10)
        
        vn2ray_check = tk.Checkbutton(self.add_options_frame, text="Vn2ray", 
                                     variable=self.add_vn2ray, font=('Arial', 10), bg='white',
                                     command=lambda: self.toggle_file_config('vn2ray'))
        vn2ray_check.place(x=150, y=10)
        
        wwproxy_add_check = tk.Checkbutton(self.add_options_frame, text="WW Proxy", 
                                          variable=self.add_wwproxy, font=('Arial', 10), bg='white',
                                          command=lambda: self.toggle_file_config('wwproxy'))
        wwproxy_add_check.place(x=280, y=10)
        
        proxyno1_check = tk.Checkbutton(self.add_options_frame, text="Proxy No1", 
                                       variable=self.add_proxyno1, font=('Arial', 10), bg='white',
                                       command=lambda: self.toggle_file_config('proxyno1'))
        proxyno1_check.place(x=420, y=10)
        
        # File configurations container
        self.file_configs_container = tk.Frame(self.add_options_frame, bg='white')
        
        # File configurations
        self.file_configs = {}
        self.create_file_configs()
        
        # Run button
        run_button = tk.Button(main_frame, text="XỬ LÝ", 
                              font=('Arial', 14, 'bold'), bg='#e74c3c', fg='white',
                              width=10, height=1, command=self.run_process)
        run_button.place(x=400, y=790, anchor='center')
        
    def create_file_configs(self):
        for i, file_type in enumerate(['host:port', 'vn2ray', 'wwproxy', 'proxyno1']):
            config_frame = tk.Frame(self.file_configs_container, bg='#f8f9fa', relief='groove', bd=1)
            
            # Title
            title_map = {
                'host:port': 'Chia Host:Port', 
                'vn2ray': 'Chia Host:Port', 
                'wwproxy': 'Chia Key',
                'proxyno1': 'Chia Key'
            }
            
            title_label = tk.Label(config_frame, text=title_map[file_type], 
                                  font=('Arial', 11, 'bold'), bg='#f8f9fa')
            title_label.place(x=10, y=10)
            
            # Data input label
            data_label = tk.Label(config_frame, text=f"Dữ liệu {file_type.upper()}:", 
                                 font=('Arial', 10), bg='#f8f9fa')
            data_label.place(x=10, y=40)
            
            # Text widget
            text_widget = scrolledtext.ScrolledText(config_frame, height=4, width=80, 
                                                   font=('Courier', 9))
            text_widget.place(x=10, y=65, width=680, height=80)
            
            # Placeholder text
            placeholders = {
                'host:port': '123.456.78.90:8080\n203.113.160.50:3128\n192.241.212.123:1080',
                'vn2ray': '5.189.184.6:3128\n159.89.132.108:8989\n138.201.5.60:3128',
                'wwproxy': 'UK-992415dc-6953-477f-bdd6-4283fcb1aab4\nUK-7f4d2a1b-3d2e-4c0f-91b8-d8c4e62f9a2c\nUK-fd8a9c3e-0e2a-4f6a-9e5b-2b3d1c6a1234',
                'proxyno1': 'proxy1.example.com:8080\nproxy2.example.com:3128\nproxy3.example.com:1080'
            }
            text_widget.insert('1.0', placeholders[file_type])
            text_widget.config(fg='gray')
            
            def on_focus_in(event, widget=text_widget, placeholder=placeholders[file_type]):
                if widget.get('1.0', 'end-1c') == placeholder:
                    widget.delete('1.0', 'end')
                    widget.config(fg='black')
                    
            def on_focus_out(event, widget=text_widget, placeholder=placeholders[file_type]):
                if not widget.get('1.0', 'end-1c').strip():
                    widget.insert('1.0', placeholder)
                    widget.config(fg='gray')
            
            text_widget.bind('<FocusIn>', on_focus_in)
            text_widget.bind('<FocusOut>', on_focus_out)
            
            # Split config
            split_label = tk.Label(config_frame, text=f"Số lượng {file_type} mỗi file:", 
                                  font=('Arial', 12), bg='#f8f9fa')
            split_label.place(x=10, y=165)
            
            split_var = tk.StringVar(value="1")
            split_spinbox = tk.Spinbox(config_frame, from_=1, to=100, width=5, 
                                      textvariable=split_var, font=('Arial', 12))
            split_spinbox.place(x=230, y=168)
            
            # Save button
            save_btn = tk.Button(config_frame, text="Save", 
                               font=('Arial', 12),bg='#0dcaf0', fg='white', width=10,
                               command=lambda ft=file_type: self.save_config(ft))
            save_btn.place(x=300, y=162)
            
            self.file_configs[file_type] = {
                'frame': config_frame,
                'text': text_widget,
                'split': split_var
            }
    
    def update_folder_info(self, *args):
        count = self.folder_count.get()
        self.folder_info.config(text=f"(Từ LDPlayer-1 đến LDPlayer-{count})")
    
    def toggle_delete_options(self):
        if self.enable_delete.get():
            self.delete_options_frame.place(x=15, y=50, width=720, height=120)
        else:
            self.delete_options_frame.place_forget()
    
    def toggle_add_options(self):
        if self.enable_add.get():
            self.add_options_frame.place(x=15, y=30, width=720, height=335)
            self.file_configs_container.place(x=10, y=40, width=700, height=290)
        else:
            self.add_options_frame.place_forget()
    
    def toggle_file_config(self, file_type):
        var_map = {
            'host:port': self.add_hostport, 
            'vn2ray': self.add_vn2ray, 
            'wwproxy': self.add_wwproxy,
            'proxyno1': self.add_proxyno1
        }
        
        # Tính vị trí y cho từng config
        file_types = ['host:port', 'vn2ray', 'wwproxy', 'proxyno1']
        active_configs = [ft for ft in file_types if var_map[ft].get()]
        
        if var_map[file_type].get():
            # Hiển thị config
            y_pos = active_configs.index(file_type) * 220
            self.file_configs[file_type]['frame'].place(x=0, y=y_pos, width=700, height=210)
        else:
            # Ẩn config
            self.file_configs[file_type]['frame'].place_forget()
            
        # Sắp xếp lại các config còn lại
        for i, ft in enumerate(active_configs):
            if var_map[ft].get():
                self.file_configs[ft]['frame'].place(x=0, y=i * 220, width=700, height=210)
    
    def save_config(self, file_type):
        text_widget = self.file_configs[file_type]['text']
        data_text = text_widget.get('1.0', 'end-1c').strip()
        
        # Check if it's placeholder text
        placeholders = {
            'host:port': '123.456.78.90:8080\n203.113.160.50:3128\n192.241.212.123:1080',
            'vn2ray': '5.189.184.6:3128\n159.89.132.108:8989\n138.201.5.60:3128',
            'wwproxy': 'UK-992415dc-6953-477f-bdd6-4283fcb1aab4\nUK-7f4d2a1b-3d2e-4c0f-91b8-d8c4e62f9a2c\nUK-fd8a9c3e-0e2a-4f6a-9e5b-2b3d1c6a1234',
            'proxyno1': 'proxy1.example.com:8080\nproxy2.example.com:3128\nproxy3.example.com:1080'
        }
        
        if not data_text or data_text == placeholders[file_type]:
            messagebox.showerror("Lỗi", f"Vui lòng nhập dữ liệu {file_type.upper()}")
            return
        
        split_count = int(self.file_configs[file_type]['split'].get())
        data_lines = [line.strip() for line in data_text.split('\n') if line.strip()]
        
        self.configs[file_type] = {
            'data': data_lines,
            'split': split_count
        }
        

    
    def split_data(self, data, chunk_size):
        """Chia dữ liệu thành các phần"""
        chunks = []
        for i in range(0, len(data), chunk_size):
            chunks.append(data[i:i + chunk_size])
        return chunks
    
    def backup_file(self, file_path):
        """Backup file trước khi xóa vào folder Backup"""
        try:
            if os.path.exists(file_path):
                # Tạo folder Backup nếu chưa có
                backup_dir = os.path.join("Profile", "Backup")
                print(f"DEBUG: Đang tạo backup dir: {backup_dir}")
                
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                    print(f"DEBUG: Đã tạo folder backup: {backup_dir}")
                else:
                    print(f"DEBUG: Folder backup đã tồn tại: {backup_dir}")
                
                # Tạo tên file backup với thông tin folder và timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                folder_name = os.path.basename(os.path.dirname(file_path))  # LDPlayer-X
                filename = os.path.basename(file_path)  # gmail.txt
                backup_filename = f"{folder_name}_{filename}.backup_{timestamp}"
                backup_path = os.path.join(backup_dir, backup_filename)
                
                print(f"DEBUG: Đang backup {file_path} -> {backup_path}")
                shutil.copy2(file_path, backup_path)
                print(f"DEBUG: Backup thành công: {backup_path}")
                return backup_path
            else:
                print(f"DEBUG: File không tồn tại để backup: {file_path}")
                return None
        except Exception as e:
            print(f"DEBUG: Lỗi khi backup {file_path}: {str(e)}")
            return None
    
    def run_process(self):
        try:
            folder_count = int(self.folder_count.get())
            enable_delete = self.enable_delete.get()
            enable_add = self.enable_add.get()
            
            if not enable_delete and not enable_add:
                messagebox.showerror("Lỗi", "Vui lòng chọn ít nhất một chức năng (Xóa hoặc Thêm)")
                return
            
            # Kiểm tra folder Instance
            instance_path = "Profile"
            if not os.path.exists(instance_path):
                messagebox.showerror("Lỗi", "Không tìm thấy folder 'Instance'")
                return
            
            process_log = []
            backup_files = []
            
            # Xử lý từng folder
            for i in range(1, folder_count + 1):
                folder_name = f"Profile-{i}"
                folder_path = os.path.join(instance_path, folder_name)
                
                if not os.path.exists(folder_path):
                    process_log.append(f"⚠️ Folder không tồn tại: {folder_name}")
                    continue
                
                process_log.append(f"\n📁 Xử lý folder: {folder_name}")
                
                # Xử lý xóa file
                if enable_delete:
                    files_to_delete = []
                    if self.delete_gmail.get():
                        files_to_delete.append('hostport.txt')
                    if self.delete_proxy.get():
                        files_to_delete.append('vn2ray.txt')
                    if self.delete_ipport.get():
                        files_to_delete.append('wwproxy.txt')
                    if self.delete_wwproxy.get():
                        files_to_delete.append('proxyno1.txt')
                    
                    for filename in files_to_delete:
                        file_path = os.path.join(folder_path, filename)
                        print(f"DEBUG: Checking file: {file_path}")
                        
                        if os.path.exists(file_path):
                            print(f"DEBUG: File tồn tại, sẽ backup: {file_path}")
                            # Backup trước khi xóa
                            backup_path = self.backup_file(file_path)
                            if backup_path:
                                backup_name = os.path.basename(backup_path)
                                process_log.append(f"  💾 Backup: {backup_name}")
                                backup_files.append(backup_path)
                            
                            # Xóa file
                            os.remove(file_path)
                            process_log.append(f"  🗑️ Đã xóa: {filename}")
                        else:
                            print(f"DEBUG: File không tồn tại: {file_path}")
                            process_log.append(f"  ⚠️ File không tồn tại: {filename}")
                
                # Xử lý thêm dữ liệu
                # Xử lý thêm dữ liệu (dòng 439-465)
                if enable_add:
                    files_to_add = []
                    if self.add_hostport.get():
                        files_to_add.append('host:port')     # ✅ BỎ .txt
                    if self.add_vn2ray.get():
                        files_to_add.append('vn2ray')       # ✅ BỎ .txt  
                    if self.add_wwproxy.get():
                        files_to_add.append('wwproxy')      # ✅ BỎ .txt
                    if self.add_proxyno1.get():
                        files_to_add.append('proxyno1')    # ✅ BỎ .txt
                    
                    # Map tên file an toàn không có dấu ":" (Windows không cho phép)
                    file_name_map = {
                        'host:port': 'hostport.txt',
                        'vn2ray': 'vn2ray.txt',
                        'wwproxy': 'wwproxy.txt',
                        'proxyno1': 'proxyno1.txt'
                    }

                    for file_type in files_to_add:
                        if file_type in self.configs and self.configs[file_type]['data']:
                            chunks = self.split_data(self.configs[file_type]['data'], 
                                                self.configs[file_type]['split'])
                            if chunks:
                                chunk_index = (i - 1) % len(chunks)
                                data_for_folder = chunks[chunk_index]
                                
                                # Ghi dữ liệu vào file - THÊM .txt Ở ĐÂY
                                filename = file_name_map.get(file_type, f"{file_type}.txt")  # fallback nếu thiếu
                                file_path = os.path.join(folder_path, filename) # ✅ THÊM .txt khi tạo file
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write('\n'.join(data_for_folder))
                                
                                process_log.append(f"  ➕ Đã ghi {file_type}.txt: {len(data_for_folder)} dòng")
                                if len(data_for_folder) <= 3:
                                    process_log.append(f"     Dữ liệu: {', '.join(data_for_folder)}")
                                else:
                                    process_log.append(f"     Dữ liệu: {', '.join(data_for_folder[:2])}...")
                        else:
                            process_log.append(f"  ⚠️ Chưa cấu hình dữ liệu cho {file_type}.txt")
            
                       
            messagebox.showinfo("Thành công", f"Đã xử lý thành công {folder_count} folders LDPlayer!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

def main():
    root = tk.Tk()
    app = LDPlayerManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()