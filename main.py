from interface import App
from Tkinter import *


root = Tk()
#root.geometry("320x240")
root.wm_maxsize(950, 950)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
app = App(root)
root.mainloop()
