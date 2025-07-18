import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import os
import subprocess
from datetime import datetime

class ProfileFetcher:
    def __init__(self, root):
        self.root = root
        self.root.title("GPM Profile Fetcher")
        self.root.geometry("700x600")
        
        # Variables
        self.profile_directory = tk.StringVar()
        self.profile_ids = tk.StringVar()
        self.api_base_url = "http://127.0.0.1:19995/api/v3/profiles"
        self.profile_paths = []
        self.selected_file_path = tk.StringVar()
        self.single_folder_path = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Profile Fetcher
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Profile Fetcher')
        self.setup_fetcher_tab()
        
        # Tab 2: Zip Profiles
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Zip Profiles')
        self.setup_zip_tab()
        
        # Tab 3: Zip Single Folder
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Zip Single Folder')
        self.setup_single_zip_tab()
    
    def setup_fetcher_tab(self):
        # Main frame for tab 1
        main_frame = ttk.Frame(self.tab1, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Profile Directory Input
        ttk.Label(main_frame, text="Đường dẫn thư mục Profile:").grid(row=0, column=0, sticky=tk.W, pady=5)
        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Entry(dir_frame, textvariable=self.profile_directory, width=50).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(dir_frame, text="Browse", command=self.browse_directory).grid(row=0, column=1, padx=(5, 0))
        
        # Profile IDs Input
        ttk.Label(main_frame, text="Danh sách ID (mỗi ID một dòng):").grid(row=2, column=0, sticky=tk.W, pady=(20, 5))
        
        # Text area for IDs
        ids_frame = ttk.Frame(main_frame)
        ids_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.ids_text = tk.Text(ids_frame, height=10, width=70)
        scrollbar = ttk.Scrollbar(ids_frame, orient="vertical", command=self.ids_text.yview)
        self.ids_text.configure(yscrollcommand=scrollbar.set)
        
        self.ids_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, pady=20)
        
        ttk.Button(button_frame, text="Get Path", command=self.get_paths).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Xuất Path", command=self.export_paths).grid(row=0, column=1, padx=5)
        
        # Results area
        ttk.Label(main_frame, text="Kết quả:").grid(row=5, column=0, sticky=tk.W, pady=(20, 5))
        
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.results_text = tk.Text(results_frame, height=8, width=70, state=tk.DISABLED)
        results_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights for tab 1
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        dir_frame.columnconfigure(0, weight=1)
        ids_frame.columnconfigure(0, weight=1)
        ids_frame.rowconfigure(0, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        self.tab1.columnconfigure(0, weight=1)
        self.tab1.rowconfigure(0, weight=1)
        
        # Set default profile directory
        self.profile_directory.set("D:\\GPM\\Profile")
    
    def setup_zip_tab(self):
        # Main frame for tab 2
        zip_frame = ttk.Frame(self.tab2, padding="10")
        zip_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # File selection
        ttk.Label(zip_frame, text="Chọn file path đã xuất:").grid(row=0, column=0, sticky=tk.W, pady=5)
        file_frame = ttk.Frame(zip_frame)
        file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Entry(file_frame, textvariable=self.selected_file_path, width=60).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="Browse", command=self.browse_path_file).grid(row=0, column=1, padx=(5, 0))
        
        # 7-Zip path configuration
        ttk.Label(zip_frame, text="Đường dẫn 7-Zip:").grid(row=2, column=0, sticky=tk.W, pady=(20, 5))
        self.zip_path = tk.StringVar()
        self.zip_path.set("C:\\Program Files\\7-Zip\\7z.exe")
        
        zip_path_frame = ttk.Frame(zip_frame)
        zip_path_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Entry(zip_path_frame, textvariable=self.zip_path, width=60).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(zip_path_frame, text="Browse", command=self.browse_7zip_path).grid(row=0, column=1, padx=(5, 0))
        
        # Output directory
        ttk.Label(zip_frame, text="Thư mục xuất file nén:").grid(row=4, column=0, sticky=tk.W, pady=(20, 5))
        self.output_zip_dir = tk.StringVar()
        self.output_zip_dir.set("C:\\Users\\ADMIN\\Desktop\\Profile Test")
        
        output_frame = ttk.Frame(zip_frame)
        output_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Entry(output_frame, textvariable=self.output_zip_dir, width=60).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(output_frame, text="Browse", command=self.browse_output_dir).grid(row=0, column=1, padx=(5, 0))
        
        # Compression level
        ttk.Label(zip_frame, text="Mức nén:").grid(row=6, column=0, sticky=tk.W, pady=(20, 5))
        self.compression_level = tk.StringVar()
        self.compression_level.set("5")
        
        compression_frame = ttk.Frame(zip_frame)
        compression_frame.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=5)
        
        compression_combo = ttk.Combobox(compression_frame, textvariable=self.compression_level, 
                                       values=["0", "1", "3", "5", "7", "9"], width=10, state="readonly")
        compression_combo.grid(row=0, column=0, sticky=tk.W)
        ttk.Label(compression_frame, text="(0=Không nén, 9=Nén tối đa)").grid(row=0, column=1, padx=(10, 0))
        
        # Zip button
        ttk.Button(zip_frame, text="Zip", command=self.zip_profiles).grid(row=8, column=0, pady=20)
        
        # Progress and results
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(zip_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Zip results area
        ttk.Label(zip_frame, text="Kết quả nén:").grid(row=10, column=0, sticky=tk.W, pady=(20, 5))
        
        zip_results_frame = ttk.Frame(zip_frame)
        zip_results_frame.grid(row=11, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.zip_results_text = tk.Text(zip_results_frame, height=10, width=70, state=tk.DISABLED)
        zip_results_scrollbar = ttk.Scrollbar(zip_results_frame, orient="vertical", command=self.zip_results_text.yview)
        self.zip_results_text.configure(yscrollcommand=zip_results_scrollbar.set)
        
        self.zip_results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        zip_results_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights for tab 2
        zip_frame.columnconfigure(0, weight=1)
        zip_frame.rowconfigure(11, weight=1)
        
        file_frame.columnconfigure(0, weight=1)
        zip_path_frame.columnconfigure(0, weight=1)
        output_frame.columnconfigure(0, weight=1)
        zip_results_frame.columnconfigure(0, weight=1)
        zip_results_frame.rowconfigure(0, weight=1)
        
        self.tab2.columnconfigure(0, weight=1)
        self.tab2.rowconfigure(0, weight=1)
    
    def setup_single_zip_tab(self):
        # Main frame for tab 3
        single_zip_frame = ttk.Frame(self.tab3, padding="10")
        single_zip_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Folder selection
        ttk.Label(single_zip_frame, text="Chọn thư mục cần nén:").grid(row=0, column=0, sticky=tk.W, pady=5)
        folder_frame = ttk.Frame(single_zip_frame)
        folder_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Entry(folder_frame, textvariable=self.single_folder_path, width=60).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(folder_frame, text="Browse", command=self.browse_single_folder).grid(row=0, column=1, padx=(5, 0))
        
        # 7-Zip path configuration
        ttk.Label(single_zip_frame, text="Đường dẫn 7-Zip:").grid(row=2, column=0, sticky=tk.W, pady=(20, 5))
        self.single_zip_path = tk.StringVar()
        self.single_zip_path.set("C:\\Program Files\\7-Zip\\7z.exe")
        
        single_zip_path_frame = ttk.Frame(single_zip_frame)
        single_zip_path_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Entry(single_zip_path_frame, textvariable=self.single_zip_path, width=60).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(single_zip_path_frame, text="Browse", command=self.browse_single_7zip_path).grid(row=0, column=1, padx=(5, 0))
        
        # Output directory
        ttk.Label(single_zip_frame, text="Thư mục xuất file nén:").grid(row=4, column=0, sticky=tk.W, pady=(20, 5))
        self.single_output_dir = tk.StringVar()
        self.single_output_dir.set("C:\\Users\\ADMIN\\Desktop\\Profile Test")
        
        single_output_frame = ttk.Frame(single_zip_frame)
        single_output_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Entry(single_output_frame, textvariable=self.single_output_dir, width=60).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(single_output_frame, text="Browse", command=self.browse_single_output_dir).grid(row=0, column=1, padx=(5, 0))
        
        # Compression level
        ttk.Label(single_zip_frame, text="Mức nén:").grid(row=6, column=0, sticky=tk.W, pady=(20, 5))
        self.single_compression_level = tk.StringVar()
        self.single_compression_level.set("5")
        
        single_compression_frame = ttk.Frame(single_zip_frame)
        single_compression_frame.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=5)
        
        single_compression_combo = ttk.Combobox(single_compression_frame, textvariable=self.single_compression_level, 
                                              values=["0", "1", "3", "5", "7", "9"], width=10, state="readonly")
        single_compression_combo.grid(row=0, column=0, sticky=tk.W)
        ttk.Label(single_compression_frame, text="(0=Không nén, 9=Nén tối đa)").grid(row=0, column=1, padx=(10, 0))
        
        # Archive name
        ttk.Label(single_zip_frame, text="Tên file nén (không cần .7z):").grid(row=8, column=0, sticky=tk.W, pady=(20, 5))
        self.archive_name = tk.StringVar()
        self.archive_name.set("archive")
        
        ttk.Entry(single_zip_frame, textvariable=self.archive_name, width=40).grid(row=9, column=0, sticky=tk.W, pady=5)
        
        # Options
        self.add_timestamp = tk.BooleanVar()
        self.add_timestamp.set(True)
        ttk.Checkbutton(single_zip_frame, text="Thêm timestamp vào tên file", 
                       variable=self.add_timestamp).grid(row=10, column=0, sticky=tk.W, pady=5)
        
        # Zip button
        ttk.Button(single_zip_frame, text="Zip Folder", command=self.zip_single_folder).grid(row=11, column=0, pady=20)
        
        # Progress and results
        self.single_progress_var = tk.DoubleVar()
        self.single_progress_bar = ttk.Progressbar(single_zip_frame, variable=self.single_progress_var, maximum=100)
        self.single_progress_bar.grid(row=12, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Results area
        ttk.Label(single_zip_frame, text="Kết quả nén:").grid(row=13, column=0, sticky=tk.W, pady=(20, 5))
        
        single_results_frame = ttk.Frame(single_zip_frame)
        single_results_frame.grid(row=14, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.single_results_text = tk.Text(single_results_frame, height=10, width=70, state=tk.DISABLED)
        single_results_scrollbar = ttk.Scrollbar(single_results_frame, orient="vertical", command=self.single_results_text.yview)
        self.single_results_text.configure(yscrollcommand=single_results_scrollbar.set)
        
        self.single_results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        single_results_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights for tab 3
        single_zip_frame.columnconfigure(0, weight=1)
        single_zip_frame.rowconfigure(14, weight=1)
        
        folder_frame.columnconfigure(0, weight=1)
        single_zip_path_frame.columnconfigure(0, weight=1)
        single_output_frame.columnconfigure(0, weight=1)
        single_results_frame.columnconfigure(0, weight=1)
        single_results_frame.rowconfigure(0, weight=1)
        
        self.tab3.columnconfigure(0, weight=1)
        self.tab3.rowconfigure(0, weight=1)
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.profile_directory.set(directory)
    
    def browse_path_file(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file path",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir="C:\\Users\\ADMIN\\Desktop\\Profile Test"
        )
        if file_path:
            self.selected_file_path.set(file_path)
    
    def browse_7zip_path(self):
        file_path = filedialog.askopenfilename(
            title="Chọn 7z.exe",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")],
            initialdir="C:\\Program Files\\7-Zip"
        )
        if file_path:
            self.zip_path.set(file_path)
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Chọn thư mục xuất file nén")
        if directory:
            self.output_zip_dir.set(directory)
    
    def browse_single_folder(self):
        directory = filedialog.askdirectory(title="Chọn thư mục cần nén")
        if directory:
            self.single_folder_path.set(directory)
    
    def browse_single_7zip_path(self):
        file_path = filedialog.askopenfilename(
            title="Chọn 7z.exe",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")],
            initialdir="C:\\Program Files\\7-Zip"
        )
        if file_path:
            self.single_zip_path.set(file_path)
    
    def browse_single_output_dir(self):
        directory = filedialog.askdirectory(title="Chọn thư mục xuất file nén")
        if directory:
            self.single_output_dir.set(directory)
    
    def get_paths(self):
        # Clear previous results
        self.profile_paths = []
        self.update_results_text("")
        
        # Get IDs from text area
        ids_text = self.ids_text.get("1.0", tk.END).strip()
        if not ids_text:
            messagebox.showwarning("Warning", "Vui lòng nhập danh sách ID!")
            return
        
        # Get profile directory
        profile_dir = self.profile_directory.get().strip()
        if not profile_dir:
            messagebox.showwarning("Warning", "Vui lòng nhập đường dẫn thư mục Profile!")
            return
        
        # Parse IDs
        ids = [id.strip() for id in ids_text.split('\n') if id.strip()]
        
        if not ids:
            messagebox.showwarning("Warning", "Không tìm thấy ID hợp lệ!")
            return
        
        # Process each ID
        results = []
        success_count = 0
        
        for profile_id in ids:
            try:
                # Make API request
                url = f"{self.api_base_url}/{profile_id}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success") and data.get("data"):
                        profile_path = data["data"].get("profile_path", "")
                        if profile_path:
                            full_path = os.path.join(profile_dir, profile_path).replace("/", "\\")
                            self.profile_paths.append(full_path)
                            results.append(f"✓ {profile_id}: {profile_path}")
                            success_count += 1
                        else:
                            results.append(f"✗ {profile_id}: Không tìm thấy profile_path")
                    else:
                        results.append(f"✗ {profile_id}: API trả về lỗi")
                else:
                    results.append(f"✗ {profile_id}: HTTP {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                results.append(f"✗ {profile_id}: Lỗi kết nối - {str(e)}")
            except Exception as e:
                results.append(f"✗ {profile_id}: Lỗi - {str(e)}")
        
        # Display results
        results_text = f"Đã xử lý {len(ids)} ID, thành công: {success_count}\n\n" + "\n".join(results)
        self.update_results_text(results_text)
        
        if success_count > 0:
            messagebox.showinfo("Success", f"Đã lấy thành công {success_count} đường dẫn profile!")
        else:
            messagebox.showwarning("Warning", "Không lấy được đường dẫn profile nào!")
    
    def export_paths(self):
        if not self.profile_paths:
            messagebox.showwarning("Warning", "Không có đường dẫn nào để xuất! Vui lòng click 'Get Path' trước.")
            return
        
        # Create output directory if it doesn't exist
        output_dir = "C:\\Users\\ADMIN\\Desktop\\Profile Test"
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Không thể tạo thư mục xuất: {str(e)}")
            return
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"profile_paths_{timestamp}.txt"
        filepath = os.path.join(output_dir, filename)
        
        try:
            # Write paths to file
            with open(filepath, 'w', encoding='utf-8') as f:
                for path in self.profile_paths:
                    f.write(path + '\n')
            
            messagebox.showinfo("Success", f"Đã xuất {len(self.profile_paths)} đường dẫn vào file:\n{filepath}")
            
            # Ask if user wants to open the file
            if messagebox.askyesno("Open File", "Bạn có muốn mở file vừa xuất không?"):
                os.startfile(filepath)
                
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi xuất file: {str(e)}")
    
    def zip_profiles(self):
        # Check if file is selected
        file_path = self.selected_file_path.get().strip()
        if not file_path:
            messagebox.showwarning("Warning", "Vui lòng chọn file path!")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File không tồn tại!")
            return
        
        # Check if 7-Zip exists
        zip_exe = self.zip_path.get().strip()
        if not os.path.exists(zip_exe):
            messagebox.showerror("Error", "Không tìm thấy 7z.exe! Vui lòng kiểm tra đường dẫn.")
            return
        
        # Create output directory
        output_dir = self.output_zip_dir.get().strip()
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Không thể tạo thư mục xuất: {str(e)}")
            return
        
        # Read paths from file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                paths = [line.strip() for line in f.readlines() if line.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Không thể đọc file: {str(e)}")
            return
        
        if not paths:
            messagebox.showwarning("Warning", "File không chứa đường dẫn nào!")
            return
        
        # Filter existing paths
        existing_paths = []
        missing_paths = []
        
        for path in paths:
            if os.path.exists(path):
                existing_paths.append(path)
            else:
                missing_paths.append(path)
        
        if not existing_paths:
            messagebox.showwarning("Warning", "Không tìm thấy thư mục nào tồn tại!")
            return
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"profiles_{timestamp}.7z"
        output_filepath = os.path.join(output_dir, output_filename)
        
        # Update results text
        results = []
        results.append(f"Bắt đầu nén {len(existing_paths)} thư mục...")
        if missing_paths:
            results.append(f"Cảnh báo: {len(missing_paths)} thư mục không tồn tại và sẽ bị bỏ qua")
        results.append("")
        
        self.update_zip_results_text("\n".join(results))
        
        # Reset progress bar
        self.progress_var.set(0)
        self.root.update()
        
        try:
            # Build 7-Zip command
            cmd = [
                zip_exe,
                "a",  # Add to archive
                f"-mx{self.compression_level.get()}",  # Compression level
                output_filepath
            ]
            cmd.extend(existing_paths)
            
            # Execute 7-Zip command
            self.progress_var.set(50)
            self.root.update()
            
            process = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            self.progress_var.set(100)
            self.root.update()
            
            if process.returncode == 0:
                file_size = os.path.getsize(output_filepath)
                file_size_mb = file_size / (1024 * 1024)
                
                success_msg = f"✓ Nén thành công!\n"
                success_msg += f"File: {output_filepath}\n"
                success_msg += f"Kích thước: {file_size_mb:.2f} MB\n"
                success_msg += f"Đã nén: {len(existing_paths)} thư mục"
                
                results.append(success_msg)
                self.update_zip_results_text("\n".join(results))
                
                messagebox.showinfo("Success", f"Nén thành công!\nFile: {output_filename}\nKích thước: {file_size_mb:.2f} MB")
                
                # Ask if user wants to open the output directory
                if messagebox.askyesno("Open Directory", "Bạn có muốn mở thư mục chứa file nén không?"):
                    os.startfile(output_dir)
            else:
                error_msg = f"✗ Lỗi nén: {process.stderr}"
                results.append(error_msg)
                self.update_zip_results_text("\n".join(results))
                messagebox.showerror("Error", f"Lỗi nén: {process.stderr}")
                
        except Exception as e:
            results.append(f"✗ Lỗi: {str(e)}")
            self.update_zip_results_text("\n".join(results))
            messagebox.showerror("Error", f"Lỗi khi nén: {str(e)}")
        finally:
            self.progress_var.set(0)
    
    def zip_single_folder(self):
        # Check if folder is selected
        folder_path = self.single_folder_path.get().strip()
        if not folder_path:
            messagebox.showwarning("Warning", "Vui lòng chọn thư mục cần nén!")
            return
        
        if not os.path.exists(folder_path):
            messagebox.showerror("Error", "Thư mục không tồn tại!")
            return
        
        if not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Đường dẫn không phải là thư mục!")
            return
        
        # Check if 7-Zip exists
        zip_exe = self.single_zip_path.get().strip()
        if not os.path.exists(zip_exe):
            messagebox.showerror("Error", "Không tìm thấy 7z.exe! Vui lòng kiểm tra đường dẫn.")
            return
        
        # Create output directory
        output_dir = self.single_output_dir.get().strip()
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Không thể tạo thư mục xuất: {str(e)}")
            return
        
        # Generate output filename
        archive_name = self.archive_name.get().strip()
        if not archive_name:
            archive_name = "archive"
        
        # Add timestamp if requested
        if self.add_timestamp.get():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{archive_name}_{timestamp}.7z"
        else:
            output_filename = f"{archive_name}.7z"
        
        output_filepath = os.path.join(output_dir, output_filename)
        
        # Check if file already exists
        if os.path.exists(output_filepath):
            if not messagebox.askyesno("File Exists", f"File {output_filename} đã tồn tại. Bạn có muốn ghi đè không?"):
                return
        
        # Get folder info
        folder_name = os.path.basename(folder_path)
        folder_size = self.get_folder_size(folder_path)
        folder_size_mb = folder_size / (1024 * 1024)
        
        # Update results text
        results = []
        results.append(f"Bắt đầu nén thư mục: {folder_name}")
        results.append(f"Đường dẫn: {folder_path}")
        results.append(f"Kích thước gốc: {folder_size_mb:.2f} MB")
        results.append(f"Mức nén: {self.single_compression_level.get()}")
        results.append("")
        
        self.update_single_results_text("\n".join(results))
        
        # Reset progress bar
        self.single_progress_var.set(0)
        self.root.update()
        
        try:
            # Build 7-Zip command
            cmd = [
                zip_exe,
                "a",  # Add to archive
                f"-mx{self.single_compression_level.get()}",  # Compression level
                output_filepath,
                folder_path
            ]
            
            # Execute 7-Zip command
            self.single_progress_var.set(50)
            self.root.update()
            
            process = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            self.single_progress_var.set(100)
            self.root.update()
            
            if process.returncode == 0:
                compressed_size = os.path.getsize(output_filepath)
                compressed_size_mb = compressed_size / (1024 * 1024)
                compression_ratio = ((folder_size - compressed_size) / folder_size) * 100 if folder_size > 0 else 0
                
                success_msg = f"✓ Nén thành công!\n"
                success_msg += f"File xuất: {output_filepath}\n"
                success_msg += f"Kích thước nén: {compressed_size_mb:.2f} MB\n"
                success_msg += f"Tỷ lệ nén: {compression_ratio:.1f}%\n"
                success_msg += f"Tiết kiệm: {(folder_size_mb - compressed_size_mb):.2f} MB"
                
                results.append(success_msg)
                self.update_single_results_text("\n".join(results))
                
                messagebox.showinfo("Success", 
                    f"Nén thành công!\n"
                    f"File: {output_filename}\n"
                    f"Kích thước: {compressed_size_mb:.2f} MB\n"
                    f"Tỷ lệ nén: {compression_ratio:.1f}%")
                
                # Ask if user wants to open the output directory
                if messagebox.askyesno("Open Directory", "Bạn có muốn mở thư mục chứa file nén không?"):
                    os.startfile(output_dir)
            else:
                error_msg = f"✗ Lỗi nén: {process.stderr}"
                results.append(error_msg)
                self.update_single_results_text("\n".join(results))
                messagebox.showerror("Error", f"Lỗi nén: {process.stderr}")
                
        except Exception as e:
            results.append(f"✗ Lỗi: {str(e)}")
            self.update_single_results_text("\n".join(results))
            messagebox.showerror("Error", f"Lỗi khi nén: {str(e)}")
        finally:
            self.single_progress_var.set(0)
    
    def get_folder_size(self, folder_path):
        """Calculate total size of a folder"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
        except Exception:
            pass
        return total_size
    
    def update_results_text(self, text):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", text)
        self.results_text.config(state=tk.DISABLED)
    
    def update_zip_results_text(self, text):
        self.zip_results_text.config(state=tk.NORMAL)
        self.zip_results_text.delete("1.0", tk.END)
        self.zip_results_text.insert("1.0", text)
        self.zip_results_text.config(state=tk.DISABLED)
    
    def update_single_results_text(self, text):
        self.single_results_text.config(state=tk.NORMAL)
        self.single_results_text.delete("1.0", tk.END)
        self.single_results_text.insert("1.0", text)
        self.single_results_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = ProfileFetcher(root)
    root.mainloop()

if __name__ == "__main__":
    main()