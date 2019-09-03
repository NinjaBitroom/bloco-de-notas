from tkinter import EW, W


class BarraInferior:
    def __init__(self, master):
        master.barraInferior.grid(row=3, column=1, columnspan=2, sticky=EW)
        master.status.grid(row=1, column=1, sticky=W)
