import tkinter as tk
from tkinter import ttk

class Groupbox1Manager:
    def __init__(self, parent):
        self.parent = parent
        self.create_groupbox1()
    
    def create_groupbox1(self):
        self.groupbox1 = tk.Frame(self.parent, width=300, height=120, bg="#3b3b3b", relief="solid", bd=2, highlightbackground="white", highlightcolor="white", highlightthickness=2)
        self.groupbox1.place(x=10, y=5)
        self.groupbox1.pack_propagate(False)

        self.logo_text1 = tk.Label(self.groupbox1, text="TClone", font=("Arial Black", 28), fg="white", bg="#3b3b3b")
        self.logo_text1.pack()
        
        self.logo_text2 = tk.Label(self.groupbox1, text="Register", font=("Arial Black", 28), fg="white", bg="#3b3b3b")
        self.logo_text2.pack()