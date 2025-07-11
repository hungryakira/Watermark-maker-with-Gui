# Import Statements
from WaterMarkGui import WaterMarkGui
import tkinter as tk

# Main
if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(660, 410)
    root.maxsize(660, 410)
    app = WaterMarkGui(root)
    root.mainloop()
