from tkinter import EW, NS, NSEW


class Conteudo:
    def __init__(self, master):
        master.barraHorizontal.grid(row=2, column=1, sticky=EW)
        master.barraVertical.grid(row=1, column=2, sticky=NS)
        master.conteudo.grid(row=1, column=1, sticky=NSEW)

        master.barraHorizontal.config(command=master.conteudo.xview)
        master.barraVertical.config(command=master.conteudo.yview)
