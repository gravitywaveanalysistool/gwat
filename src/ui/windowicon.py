import platform
from src import datapath
import tkinter as tk

def set_icon(gui):
    if platform.system() == 'Windows':
        gui.iconbitmap(datapath.getDataPath("media/logo_notext_icon.ico"))
    else:
        gui.iconphoto(False, tk.PhotoImage(file=datapath.getDataPath("media/logo_notext_icon16.png")))
