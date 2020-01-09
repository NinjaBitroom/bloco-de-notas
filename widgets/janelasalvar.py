from tkinter import Label, NSEW, Button, Toplevel


class JanelaSalvar(Toplevel):
    def __init__(self, master, atividade='fechar'):
        super().__init__()

        self.mestre = master
        self.atividade = atividade
        self.atos = {'fechar': self.mestre.destroy,
                     'novo': self.mestre.novo,
                     'carregar': self.mestre.carregar}

        self.geometry('250x100+500+500')
        self.title(master.diretorio)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)

        pergunta = Label(self, text='Deseja salvar?')
        pergunta.grid(column=0, row=0, columnspan=3, sticky=NSEW)
        pergunta['font'] = ('Arial', 20)

        botaoSalvar = Button(self, text='Salvar', width=9, command=self.sairSalvando)
        botaoSalvar.grid(column=0, row=1)

        botaoNaoSalvar = Button(self, text='Não salvar', width=9, command=self.sairSemSalvar)
        botaoNaoSalvar.grid(column=1, row=1)

        botaoCancelar = Button(self, text='Cancelar', width=9, command=self.cancelar)
        botaoCancelar.grid(column=2, row=1)

        self.resizable(False, False)
        self.transient(master)
        self.focus_force()
        self.grab_set()
        self.protocol('WM_DELETE_WINDOW', self.cancelar)

    def sairSalvando(self):
        self.mestre.salvar()
        self.destroy()
        self.atos[self.atividade]()
        self.mestre.janelaDeSalvar = None

    def sairSemSalvar(self):
        self.destroy()
        self.atos[self.atividade]()
        self.mestre.janelaDeSalvar = None

    def cancelar(self):
        self.destroy()
        self.mestre.janelaDeSalvar = None
