import tkinter as tk
from gui.groupbox_1 import Groupbox1Manager
from gui.groupbox_2 import Groupbox2Manager
from gui.groupbox_3 import Groupbox3Manager
from gui.groupbox_4 import Groupbox4Manager

class AppWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TClone Register")
        self.root.geometry("1200x1000")
        self.root.configure(bg="#2b2b2b")
        self.groupbox1_manager = Groupbox1Manager(self.root)
        self.groupbox2_manager = Groupbox2Manager(self.root)
        self.groupbox3_manager = Groupbox3Manager(self.root)
        self.groupbox4_manager = Groupbox4Manager(self.root)
        self.root.groupbox4_manager = self.groupbox4_manager
    
    def run(self):
        self.root.mainloop()
