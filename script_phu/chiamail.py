import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import shutil
from datetime import datetime
import json

class LDPlayerManager:
    def __init__(self, root):
        if root is None:
            self.root = tk.Tk()
            self.is_standalone = True
        else:
            self.root = root
            self.is_standalone = False
        self.root.title("Chia Dữ Liệu")
        self.root.geometry("800x900")
        self.root.configure(bg='#f0f0f0')
        
        # Cấu hình lưu trữ - THAY ĐỔI SANG EMAIL
        self.configs = {'gmail': {'data': [], 'split': 1}, 'hotmail': {'data': [], 'split': 1}, 'outlookmail': {'data': [], 'split': 1}}
        self.setup_ui()

    def run_standalone(self):
        """Chạy standalone nếu được gọi trực tiếp"""
        if self.is_standalone:
            self.root.mainloop()    
        
    def setup_ui(self):
        # Title frame - fixed position
        title_frame = tk.Frame(self.root, bg='#3b3b3b', height=80)
        title_frame.place(x=0, y=0, width=800, height=80)
        
        title_label = tk.Label(title_frame, text="QUẢN LÝ DỮ LIỆU EMAIL", font=('Arial', 24, 'bold'), fg='white', bg='#3b3b3b')
        title_label.place(x=400, y=25, anchor='center')
        
        subtitle_label = tk.Label(title_frame, text="Tool quản lý dữ liệu email folders LDPlayer",  font=('Arial', 12), fg='#ecf0f1', bg='#3b3b3b')
        subtitle_label.place(x=400, y=55, anchor='center')
        
        # Main content area - sử dụng Frame thông thường thay vì Canvas
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.place(x=0, y=80, width=800, height=820)
        
        # Folder count section
        folder_frame = tk.LabelFrame(main_frame, text="CẤU HÌNH FOLDER", font=('Arial', 12, 'bold'), fg='#2c3e50', bg='#f8f9fa')
        folder_frame.place(x=20, y=20, width=760, height=100)
        
        folder_label = tk.Label(folder_frame, text="Số folder LDPlayer", font=('Arial', 12, 'bold'), bg='#f8f9fa')
        folder_label.place(x=15, y=5)
        
        self.folder_count = tk.StringVar(value="1")
        folder_spinbox = tk.Spinbox(folder_frame, from_=1, to=40, width=10, textvariable=self.folder_count, font=('Arial', 11))
        folder_spinbox.place(x=15, y=45)
        
        self.folder_info = tk.Label(folder_frame, text="(Từ LDPlayer-1 đến LDPlayer-xx)", font=('Arial', 10), fg='#666', bg='#f8f9fa')
        self.folder_info.place(x=150, y=47)
        
        self.folder_count.trace('w', self.update_folder_info)
        
        # Delete section - THAY ĐỔI TEXT
        delete_frame = tk.LabelFrame(main_frame, text="XÓA DỮ LIỆU EMAIL", font=('Arial', 12, 'bold'), fg='#2c3e50', bg='#f8f9fa')
        delete_frame.place(x=20, y=130, width=760, height=210)
        
        self.enable_delete = tk.BooleanVar()
        delete_check = tk.Checkbutton(delete_frame, text="Xóa file email", variable=self.enable_delete, font=('Arial', 12, 'bold'), bg='#f8f9fa', command=self.toggle_delete_options)
        delete_check.place(x=15, y=5)
        
        self.delete_options_frame = tk.Frame(delete_frame, bg='white', relief='ridge', bd=1)
        
        # THAY ĐỔI CÁC BIẾN DELETE
        self.delete_gmail = tk.BooleanVar()
        self.delete_hotmail = tk.BooleanVar()
        self.delete_outlookmail = tk.BooleanVar()
        
        # THAY ĐỔI CÁC CHECKBOX DELETE
        gmail_del_check = tk.Checkbutton(self.delete_options_frame, text="Gmail", variable=self.delete_gmail, font=('Arial', 10), bg='white')
        gmail_del_check.place(x=20, y=10)
        
        hotmail_del_check = tk.Checkbutton(self.delete_options_frame, text="Hot Mail", variable=self.delete_hotmail, font=('Arial', 10), bg='white')
        hotmail_del_check.place(x=20, y=35)
        
        outlookmail_del_check = tk.Checkbutton(self.delete_options_frame, text="Outlook Mail", variable=self.delete_outlookmail, font=('Arial', 10), bg='white')
        outlookmail_del_check.place(x=20, y=60)
        
        # Add data section - THAY ĐỔI TEXT
        add_frame = tk.LabelFrame(main_frame, text="➕ Thêm dữ liệu email", font=('Arial', 12, 'bold'), fg='#2c3e50', bg='#f8f9fa')
        add_frame.place(x=20, y=350, width=760, height=410)
        
        self.enable_add = tk.BooleanVar()
        add_check = tk.Checkbutton(add_frame, text="Thêm file email", variable=self.enable_add, font=('Arial', 11, 'bold'), bg='#f8f9fa', command=self.toggle_add_options)
        add_check.place(x=15, y=5)
        
        # Container cho các file type checkboxes
        self.add_options_frame = tk.Frame(add_frame, bg='white', relief='ridge', bd=1)
        
        # THAY ĐỔI CÁC BIẾN ADD
        self.add_gmail = tk.BooleanVar()
        self.add_hotmail = tk.BooleanVar()
        self.add_outlookmail = tk.BooleanVar()
        
        # THAY ĐỔI CÁC CHECKBOX ADD
        gmail_check = tk.Checkbutton(self.add_options_frame, text="Gmail", variable=self.add_gmail, font=('Arial', 10), bg='white', command=lambda: self.toggle_file_config('gmail'))
        gmail_check.place(x=10, y=10)
        
        hotmail_check = tk.Checkbutton(self.add_options_frame, text="Hot Mail", variable=self.add_hotmail, font=('Arial', 10), bg='white', command=lambda: self.toggle_file_config('hotmail'))
        hotmail_check.place(x=150, y=10)
        
        outlookmail_check = tk.Checkbutton(self.add_options_frame, text="Outlook Mail", variable=self.add_outlookmail, font=('Arial', 10), bg='white', command=lambda: self.toggle_file_config('outlookmail'))
        outlookmail_check.place(x=280, y=10)
        
        # File configurations container
        self.file_configs_container = tk.Frame(self.add_options_frame, bg='white')
        
        # File configurations
        self.file_configs = {}
        self.create_file_configs()
        
        # Run button
        run_button = tk.Button(main_frame, text="XỬ LÝ", font=('Arial', 14, 'bold'), bg='#e74c3c', fg='white', width=10, height=1, command=self.run_process)
        run_button.place(x=400, y=790, anchor='center')
        
    def create_file_configs(self):
        # THAY ĐỔI DANH SÁCH FILE TYPES
        for i, file_type in enumerate(['gmail', 'hotmail', 'outlookmail']):
            config_frame = tk.Frame(self.file_configs_container, bg='#f8f9fa', relief='groove', bd=1)
            
            # Title - THAY ĐỔI TITLE MAP
            title_map = { 'gmail': 'Chia Gmail', 'hotmail': 'Chia Hotmail', 'outlookmail': 'Chia Outlook Mail' }
            
            title_label = tk.Label(config_frame, text=title_map[file_type], font=('Arial', 11, 'bold'), bg='#f8f9fa')
            title_label.place(x=10, y=10)
            
            # Data input label
            data_label = tk.Label(config_frame, text=f"Dữ liệu {file_type.upper()}:", font=('Arial', 10), bg='#f8f9fa')
            data_label.place(x=10, y=40)
            
            # Text widget
            text_widget = scrolledtext.ScrolledText(config_frame, height=4, width=80, font=('Courier', 9))
            text_widget.place(x=10, y=65, width=680, height=80)
            
            # Placeholder text - THAY ĐỔI PLACEHOLDER
            placeholders = {
                'gmail': 'user1@gmail.com:password123\nuser2@gmail.com:mypass456\nuser3@gmail.com:secret789',
                'hotmail': 'user1@hotmail.com:password123\nuser2@hotmail.com:mypass456\nuser3@hotmail.com:secret789',
                'outlookmail': 'user1@outlook.com:password123\nuser2@outlook.com:mypass456\nuser3@outlook.com:secret789'
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
            split_label = tk.Label(config_frame, text=f"Số lượng {file_type} mỗi file:", font=('Arial', 12), bg='#f8f9fa')
            split_label.place(x=10, y=165)
            
            split_var = tk.StringVar(value="1")
            split_spinbox = tk.Spinbox(config_frame, from_=1, to=100, width=5, textvariable=split_var, font=('Arial', 12))
            split_spinbox.place(x=230, y=168)
            
            # Save button
            save_btn = tk.Button(config_frame, text="Save", font=('Arial', 12), bg='#0dcaf0', fg='white', width=10, command=lambda ft=file_type: self.save_config(ft))
            save_btn.place(x=300, y=162)
            
            self.file_configs[file_type] = { 'frame': config_frame, 'text': text_widget, 'split': split_var }
    
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
        # THAY ĐỔI VAR MAP
        var_map = {
            'gmail': self.add_gmail, 
            'hotmail': self.add_hotmail, 
            'outlookmail': self.add_outlookmail
        }
        
        # Tính vị trí y cho từng config - THAY ĐỔI FILE TYPES
        file_types = ['gmail', 'hotmail', 'outlookmail']
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
        
        # Check if it's placeholder text - THAY ĐỔI PLACEHOLDER
        placeholders = {
            'gmail': 'user1@gmail.com:password123\nuser2@gmail.com:mypass456\nuser3@gmail.com:secret789',
            'hotmail': 'user1@hotmail.com:password123\nuser2@hotmail.com:mypass456\nuser3@hotmail.com:secret789',
            'outlookmail': 'user1@outlook.com:password123\nuser2@outlook.com:mypass456\nuser3@outlook.com:secret789'
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
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một tùy chọn (Xóa hoặc Thêm)")
                return
            
            process_log = []
            
            for i in range(1, folder_count + 1):
                folder_name = f"Profile-{i}"
                folder_path = os.path.join("Profile", folder_name)
                
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    process_log.append(f"📁 Đã tạo folder: {folder_name}")
                else:
                    process_log.append(f"📁 Xử lý folder: {folder_name}")
                
                # Xử lý xóa dữ liệu
                if enable_delete:
                    files_to_delete = []
                    if self.delete_gmail.get(): files_to_delete.append('gmail.txt')
                    if self.delete_hotmail.get(): files_to_delete.append('hotmail.txt') 
                    if self.delete_outlookmail.get(): files_to_delete.append('outlookmail.txt')
                    
                    for filename in files_to_delete:
                        file_path = os.path.join(folder_path, filename)
                        if os.path.exists(file_path):
                            backup_path = self.backup_file(file_path)
                            os.remove(file_path)
                            process_log.append(f"  🗑️ Đã xóa {filename} (backup: {os.path.basename(backup_path) if backup_path else 'N/A'})")
                        else:
                            process_log.append(f"  ⚠️ File không tồn tại: {filename}")
                
                # Xử lý thêm dữ liệu
                if enable_add:
                    files_to_add = []
                    if self.add_gmail.get(): files_to_add.append('gmail')
                    if self.add_hotmail.get(): files_to_add.append('hotmail')  
                    if self.add_outlookmail.get(): files_to_add.append('outlookmail')
                    
                    file_name_map = {'gmail': 'gmail.txt', 'hotmail': 'hotmail.txt', 'outlookmail': 'outlookmail.txt'}

                    for file_type in files_to_add:
                        if file_type in self.configs and self.configs[file_type]['data']:
                            chunks = self.split_data(self.configs[file_type]['data'], self.configs[file_type]['split'])
                            if chunks:
                                chunk_index = (i - 1) % len(chunks)
                                data_for_folder = chunks[chunk_index]
                                
                                filename = file_name_map.get(file_type, f"{file_type}.txt")
                                file_path = os.path.join(folder_path, filename)
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write('\n'.join(data_for_folder))
                                
                                process_log.append(f"  ➕ Đã ghi {filename}: {len(data_for_folder)} dòng")
                                if len(data_for_folder) <= 3:
                                    process_log.append(f"     Dữ liệu: {', '.join(data_for_folder)}")
                                else:
                                    process_log.append(f"     Dữ liệu: {', '.join(data_for_folder[:2])}...")
                        else:
                            process_log.append(f"  ⚠️ Chưa cấu hình dữ liệu cho {file_type}.txt")
            
            # Gọi callback để cập nhật bảng Ver Input Mail
            if hasattr(self, 'update_table_callback') and self.update_table_callback:
                print("DEBUG: Gọi callback cập nhật bảng")
                self.update_table_callback(self.configs, folder_count)
                print("DEBUG: Đã gọi callback thành công")
            else:
                print("DEBUG: Không có callback hoặc callback là None")
            
            messagebox.showinfo("Thành công", f"Đã xử lý thành công {folder_count} folders LDPlayer!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def set_update_table_callback(self, callback):
        """Đặt callback function để cập nhật bảng dữ liệu"""
        self.update_table_callback = callback

def main():
    app = LDPlayerManager()
    app.run_standalone()

if __name__ == "__main__":
    main()