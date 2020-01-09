from tkinter import EW, W, Label


class BarraInferior:
    def __init__(self, master):
        self.barraInferior = Label(master)
        self.status = Label(self.barraInferior, text=master.chaveAtual)

        self.barraInferior.grid(row=3, column=1, columnspan=2, sticky=EW)
        self.status.grid(row=1, column=1, sticky=W)
