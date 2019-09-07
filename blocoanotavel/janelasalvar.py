from tkinter import Label, NSEW, Button, W, EW, E


class JanelaSalvar:
    def __init__(self, master):
        self.mestre = master
        master.janelaDeSalvar.geometry('250x100+500+500')
        master.janelaDeSalvar.title(master.diretorio)
        master.janelaDeSalvar.grid_columnconfigure(0, weight=1)
        master.janelaDeSalvar.grid_columnconfigure(1, weight=1)
        master.janelaDeSalvar.grid_columnconfigure(2, weight=1)
        master.janelaDeSalvar.grid_rowconfigure(0, weight=3)
        master.janelaDeSalvar.grid_rowconfigure(1, weight=1)

        pergunta = Label(master.janelaDeSalvar, text='Deseja salvar?')
        pergunta.grid(column=0, row=0, columnspan=3, sticky=NSEW)
        pergunta['font'] = ('Arial', 20)

        botaoSalvar = Button(master.janelaDeSalvar, text='Salvar', width=9, command=self.sairSalvando)
        botaoSalvar.grid(column=0, row=1)

        botaoNaoSalvar = Button(master.janelaDeSalvar, text='Não salvar', width=9, command=self.sairSemSalvar)
        botaoNaoSalvar.grid(column=1, row=1)

        botaoCancelar = Button(master.janelaDeSalvar, text='Cancelar', width=9, command=self.cancelar)
        botaoCancelar.grid(column=2, row=1)

        master.janelaDeSalvar.resizable(False, False)
        master.janelaDeSalvar.transient(master.atual)
        master.janelaDeSalvar.focus_force()
        master.janelaDeSalvar.grab_set()
        master.janelaDeSalvar.protocol('WM_DELETE_WINDOW', self.cancelar)

    def sairSalvando(self):
        self.mestre.salvar()
        self.mestre.janelaDeSalvar.destroy()
        self.mestre.atual.destroy()

    def sairSemSalvar(self):
        self.mestre.janelaDeSalvar.destroy()
        self.mestre.atual.destroy()

    def cancelar(self):
        self.mestre.janelaDeSalvar.destroy()
        self.mestre.janelaDeSalvar = None
