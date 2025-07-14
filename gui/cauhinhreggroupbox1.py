import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class CauHinhRegGroupbox1:
    def __init__(self, parent):
        self.parent = parent
        self.app_selection_var = tk.StringVar(value="kantana")
        self.app_radio_buttons = []
        self.create_cauhinhreggroupbox1()
    
    def create_cauhinhreggroupbox1(self):
        self.cauhinhreggroupbox1 = tk.Frame(self.parent, width=1145, height=40, bg="#3b3b3b", relief="solid", bd=1, highlightbackground="white", highlightcolor="white", highlightthickness=1) 
        self.cauhinhreggroupbox1.place(x=10, y=10)
        self.cauhinhreggroupbox1.pack_propagate(False)
        
        title_label = ctk.CTkLabel(self.cauhinhreggroupbox1, text="KIỂU TẠO:", font=("Arial", 16, "bold"), text_color="#f8f9fa")
        title_label.place(x=20, y=5)

        def create_checkbox_icon(parent, x, y, checked=False):
            canvas = tk.Canvas(parent, width=18, height=18, bg="#3b3b3b", highlightthickness=0)
            canvas.place(x=x, y=y)
            canvas.create_rectangle(2, 2, 16, 16, outline="white", fill="", width=2) # Vẽ hình vuông
            if checked:
                canvas.create_line(5, 9, 8, 12, fill="white", width=2) # Vẽ dấu tick
                canvas.create_line(8, 12, 13, 6, fill="white", width=2) # Vẽ dấu tick
            return canvas

        def update_checkbox(canvas, checked):
            """Function để update trạng thái checkbox"""
            canvas.delete("all")  # Xóa tất cả drawings
            canvas.create_rectangle(2, 2, 16, 16, outline="white", fill="", width=2) # Vẽ lại hình vuông
            if checked:
                canvas.create_line(5, 9, 8, 12, fill="white", width=2) # Vẽ dấu tick
                canvas.create_line(8, 12, 13, 6, fill="white", width=2) # Vẽ dấu tick

        def on_checkbox_click(value):
            self.app_selection_var.set(value)
            self.update_all_checkboxes()

        # Tạo các checkbox
        icon_kantana = create_checkbox_icon(self.cauhinhreggroupbox1, 300, 11, False)
        icon_kantana.bind('<Button-1>', lambda e: on_checkbox_click("kantana"))
        # Tạo labels
        label_kantana = tk.Label(self.cauhinhreggroupbox1, text="Reg Kantana App", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_kantana.place(x=325, y=7)
        label_kantana.bind('<Button-1>', lambda e: on_checkbox_click("kantana"))


        icon_facebook_lite = create_checkbox_icon(self.cauhinhreggroupbox1, 600, 11, False)
        icon_facebook_lite.bind('<Button-1>', lambda e: on_checkbox_click("facebook_lite"))
        # Tạo labels
        label_facebook_lite = tk.Label(self.cauhinhreggroupbox1, text="Reg Facebook Lite App", font=('Arial', 12, 'bold'), bg="#3b3b3b", fg='white')
        label_facebook_lite.place(x=625, y=7)
        label_facebook_lite.bind('<Button-1>', lambda e: on_checkbox_click("facebook_lite"))

        # Lưu trữ các checkbox để quản lý
        self.checkboxes = {"kantana": icon_kantana, "facebook_lite": icon_facebook_lite}

        # Function để update tất cả checkboxes
        def update_all_checkboxes():
            selected_value = self.app_selection_var.get()
            for value, checkbox_canvas in self.checkboxes.items():
                is_checked = (value == selected_value)
                update_checkbox(checkbox_canvas, is_checked)

        self.update_all_checkboxes = update_all_checkboxes

        # Set default selection
        update_all_checkboxes()
