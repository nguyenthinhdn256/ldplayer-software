import tkinter as tk
from tkinter import ttk

class Groupbox3Manager:
    def __init__(self, parent):
        self.parent = parent
        self.create_groupbox3()
    
    def create_groupbox3(self):
        self.groupbox3 = tk.Frame(self.parent, width=430, height=120, bg="#3b3b3b", relief="solid", bd=2, highlightbackground="white", highlightcolor="white", highlightthickness=2)
        self.groupbox3.place(x=760, y=5)
        self.groupbox3.pack_propagate(False)
        
