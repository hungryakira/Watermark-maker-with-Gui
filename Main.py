# Import Statements
from WaterMarkGui import WaterMarkGui
import tkinter as tk

# Main
if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(810, 410)
    root.maxsize(810, 410)
    app = WaterMarkGui(root)
    root.mainloop()
