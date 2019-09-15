#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog

import threading
import chardet
import sys
import os

from barrasuperior import BarraSuperior
from conteudo import Conteudo
from barrainferior import BarraInferior
from janelasalvar import JanelaSalvar


class Aplicativo:
    def __init__(self, master=None):
        if len(sys.argv) < 2:
            self.diretorio = 'Arquivo novo'
        else:
            self.diretorio = sys.argv[1]
            try:
                arquivo = open(self.diretorio)
                arquivo.close()
            except FileNotFoundError:
                self.diretorio = 'Arquivo novo'

        self.arquivoSalvo = False
        self.chaveAtual = 'UTF-8'
        self.atual = master

        self.barraDeMenu = Menu(master)
        self.menuDeArquivo = Menu(self.barraDeMenu, tearoff=0)
        self.menuDeCodigo = Menu(self.barraDeMenu, tearoff=0)

        self.barraVertical = Scrollbar(master, orient=VERTICAL)
        self.barraHorizontal = Scrollbar(master, orient=HORIZONTAL)
        self.conteudo = Text(master, height=0, width=0, wrap=NONE,
                             xscrollcommand=self.barraHorizontal.set,
                             yscrollcommand=self.barraVertical.set)

        self.barraInferior = Label(master)
        self.status = Label(self.barraInferior, text=self.chaveAtual)

        self.janelaDeSalvar = None
        self.mensagem = self.conteudo.get(1.0, END)

        BarraSuperior(self)
        Conteudo(self)
        BarraInferior(self)

        master.protocol('WM_DELETE_WINDOW', self.fecharJanela)
        master.bind('<KeyPress>', self.verificarSalvamento)

        if self.diretorio != 'Arquivo novo':
            self.tentarAbrir()
            self.conteudo.delete(1.0, END)
            self.conteudo.insert(END, self.mensagem)
            self.conteudo.delete(float(self.conteudo.index(END)) - 1.0)

        self.verificarSalvamento()

    # Funções da Barra Superior
    def novo(self):
        if self.arquivoSalvo:
            self.diretorio = 'Arquivo novo'
            self.conteudo.delete(1.0, END)
            self.mensagem = self.conteudo.get(1.0, END)
        else:
            self.janelaDeSalvar = Toplevel()
            JanelaSalvar(self, 'novo')

    def novaJanela(self):
        aplicativo = threading.Thread(target=self.abrirApp)
        aplicativo.start()

    def carregar(self):
        copia = self.diretorio
        self.diretorio = filedialog.askopenfilename(defaultextension='.txt',
                                                    filetypes=[('Arquivos de texto', '.txt'),
                                                               ('Todos arquivos', '.*')])
        if not self.diretorio:
            self.diretorio = copia
        else:
            self.tentarAbrir()
            self.conteudo.delete(1.0, END)
            self.conteudo.insert(END, self.mensagem)
            self.conteudo.delete(float(self.conteudo.index(END)) - 1.0)

    def salvar(self):
        if self.diretorio == 'Arquivo novo':
            self.salvarComo()
        else:
            self.salvarArquivo()

    def salvarComo(self):
        copia = self.diretorio
        self.diretorio = filedialog.asksaveasfilename(defaultextension='.txt',
                                                      filetypes=[('Arquivos de texto', '.txt'),
                                                                 ('Todos arquivos', '.*')],
                                                      initialfile='*.txt')
        if not self.diretorio:
            self.diretorio = copia
        else:
            self.salvarArquivo()

    def mudarCodificacao(self, norma):
        self.chaveAtual = norma
        self.status['text'] = self.chaveAtual

    # Métodos de manipulação de arquivos
    def tentarAbrir(self):
        try:
            arquivo = open(self.diretorio, 'r', encoding=self.chaveAtual)
            self.mensagem = arquivo.read()
        except (UnicodeDecodeError, UnicodeError):
            arquivo = open(self.diretorio, 'br')
            self.mensagem = arquivo.read()
            chute = chardet.detect(self.mensagem)
            arquivo = open(self.diretorio, 'r', encoding=chute['encoding'])
            self.mensagem = arquivo.read()
            self.chaveAtual = chute['encoding']
        finally:
            arquivo.close()
            self.status['text'] = self.chaveAtual

    def salvarArquivo(self):
        arquivo = open(self.diretorio, 'w', encoding=self.chaveAtual)
        texto = self.conteudo.get(1.0, END)
        arquivo.write(texto)
        arquivo = open(self.diretorio, 'r', encoding=self.chaveAtual)
        self.mensagem = arquivo.read()
        arquivo.close()

    # Funções que verificam o estado do texto do conteúdo
    def verificarSalvamento(self, evento=None):
        if self.mensagem == self.conteudo.get(0.0, END):
            self.atual.title(f'{self.diretorio}   -   Bloco de Notas')
            self.arquivoSalvo = True
        else:
            self.atual.title(f'{self.diretorio} * -   Bloco de Notas')
            self.arquivoSalvo = False

    def fecharJanela(self):
        if self.janelaDeSalvar:
            self.janelaDeSalvar.lift()
        elif not self.arquivoSalvo:
            self.janelaDeSalvar = Toplevel()
            JanelaSalvar(self, 'fechar')
        else:
            self.atual.destroy()

    # Outras funções
    def abrirApp(self):
        if os.name == 'nt':
            os.system('python aplicativo.pyw')
        else:
            os.system('chmod +X aplicativo.pyw')
            os.system('./aplicativo.pyw')


class Aspecto:
    def __init__(self, master=None):
        master.geometry('600x400')
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(1, weight=1)
        if os.name == 'nt':
            master.iconbitmap('arquivos/icone.ico')
        else:
            img = PhotoImage(file='arquivos/icone.gif')
            master.tk.call('wm', 'iconphoto', master._w, img)


def principal():
    janela = Tk()
    Aplicativo(janela)
    Aspecto(janela)
    janela.mainloop()


principal()
