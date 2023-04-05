from tkinter import PhotoImage
from os import name
import sys
import os

class Aspecto:
    def __init__(self, master=None):
        master.geometry('600x400')
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(1, weight=1)
        if name == 'nt':
            master.iconbitmap(resource_path('arquivos/icone.ico'))
        else:
            img = PhotoImage(file='arquivos/icone.gif')
            master.tk.call('wm', 'iconphoto', master._w, img)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
