from tkinter import PhotoImage
from os import name


class Aspecto:
    def __init__(self, master=None):
        master.geometry('600x400')
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(1, weight=1)
        if name == 'nt':
            master.iconbitmap('arquivos/icone.ico')
        else:
            img = PhotoImage(file='arquivos/icone.gif')
            master.tk.call('wm', 'iconphoto', master._w, img)
