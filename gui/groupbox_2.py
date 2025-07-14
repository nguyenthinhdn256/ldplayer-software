import tkinter as tk
from tkinter import ttk
from gui.groupbox_4 import Groupbox4Manager
from gui.cauhinhreggroupbox3 import CauHinhRegGroupbox3

class Groupbox2Manager:
    def __init__(self, parent):
        self.parent = parent
        self.create_groupbox2()
    
    def create_groupbox2(self):
        self.groupbox2 = tk.Frame(self.parent, width=430, height=120, bg="#3b3b3b", relief="solid", bd=2, highlightbackground="white", highlightcolor="white", highlightthickness=2)
        self.groupbox2.place(x=320, y=5)
        self.groupbox2.pack_propagate(False)

        # App Settings button
        self.settings_button = tk.Button(self.groupbox2, text="App Settings", bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=15, height=1)
        self.settings_button.place(x=10, y=4)

        # Save ADB button
        self.save_button = tk.Button(self.groupbox2, text="Connect ADB", bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=15, height=1)
        self.save_button.place(x=10, y=42)
        
        # Start Appium button 
        self.appium_button = tk.Button(self.groupbox2, text="Start Appium", bg='#404040', fg='white', font=('Arial', 10, 'bold'), width=15, height=1)
        self.appium_button.place(x=10, y=82)

        # START REG button
        self.start_reg_button = tk.Button(self.groupbox2, text="Start", bg='#dc3545', fg='white', font=('Arial', 10, 'bold'), width=15, height=1, command=self.on_start_reg_click)
        self.start_reg_button.place(x=290, y=4)

    def on_start_reg_click(self):
        try:
            app_window = self.parent
            while app_window and not hasattr(app_window, 'groupbox4_manager'):
                app_window = app_window.master
            if app_window and hasattr(app_window, 'groupbox4_manager'):
                groupbox4_manager = app_window.groupbox4_manager
                if hasattr(groupbox4_manager, 'groupbox3_manager') and hasattr(groupbox4_manager.groupbox3_manager, 'so_ld_var'):
                    so_ld_value = int(groupbox4_manager.groupbox3_manager.so_ld_var.get())
                    groupbox4_manager.show_tab("QUẢN LÝ REG")
                    if hasattr(groupbox4_manager, 'groupbox1_manager'):
                        groupbox4_manager.groupbox1_manager.create_rows_from_so_ld(so_ld_value)
        except Exception as e:
            print(f"Error in start reg click: {e}")
        
