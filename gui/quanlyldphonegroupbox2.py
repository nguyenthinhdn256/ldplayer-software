import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class QuanLyLDPhoneGroupbox2:
    def __init__(self, parent):
        self.parent = parent
        self.app_selection_var = tk.StringVar(value="kantana")
        self.app_radio_buttons = []
        self.create_quanlyldphonegroupbox2()
    
    def create_quanlyldphonegroupbox2(self):
        self.quanlyldphonegroupbox2 = tk.Frame(self.parent, width=567, height=780, bg="#3b3b3b", relief="solid", bd=1, highlightbackground="white", highlightcolor="white", highlightthickness=1) 
        self.quanlyldphonegroupbox2.place(x=592, y=10)
        self.quanlyldphonegroupbox2.pack_propagate(False)
        
        
