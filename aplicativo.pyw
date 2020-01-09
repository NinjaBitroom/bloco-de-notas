#! /usr/bin/python3.7
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog

import subprocess
import threading
import chardet
import sys
import os

from aspecto import Aspecto
from widgets.barrasuperior import BarraSuperior
from widgets.conteudo import Conteudo
from widgets.barrainferior import BarraInferior
from widgets.janelasalvar import JanelaSalvar


class Aplicativo(Tk):
    def __init__(self):
        super().__init__()

        self.aspecto = Aspecto(self)

        self.diretorio = ''
        self.receberArquivo()

        self.arquivoSalvo = False
        self.chaveAtual = 'UTF-8'

        self.janelaDeSalvar = None

        self.barraSuperior = BarraSuperior(self)
        self.conteudo = Conteudo(self)
        self.barraInferior = BarraInferior(self)

        self.mensagem = self.conteudo.conteudo.get(1.0, END)

        self.protocol('WM_DELETE_WINDOW', self.fecharJanela)
        self.bind('<KeyPress>', self.verificarSalvamento)

        self.verificarDiretorio()
        self.verificarSalvamento()

    # Funções da Barra Superior
    def novo(self):
        if self.janelaDeSalvar or self.arquivoSalvo:
            self.diretorio = 'Arquivo novo'
            self.conteudo.conteudo.delete(1.0, END)
            self.mensagem = self.conteudo.conteudo.get(1.0, END)
        else:
            self.janelaDeSalvar = JanelaSalvar(self, 'novo')
        self.verificarSalvamento()

    def novaJanela(self):
        aplicativo = threading.Thread(target=self.abrirApp)
        aplicativo.start()

    def carregar(self):
        if self.janelaDeSalvar or self.arquivoSalvo:
            copia = self.diretorio
            self.diretorio = filedialog.askopenfilename(defaultextension='.txt',
                                                        filetypes=[('Arquivos de texto', '.txt'),
                                                                   ('Todos arquivos', '.*')])
            if not self.diretorio:
                self.diretorio = copia
            else:
                self.substituirConteudo()
        else:
            self.janelaDeSalvar = JanelaSalvar(self, 'carregar')
        self.verificarSalvamento()

    def salvar(self):
        if self.diretorio == 'Arquivo novo':
            self.salvarComo()
        else:
            self.salvarArquivo()
        self.verificarSalvamento()

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
        self.verificarSalvamento()

    def mudarCodificacao(self, norma):
        self.chaveAtual = norma
        self.barraInferior.status['text'] = self.chaveAtual

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
            self.barraInferior.status['text'] = self.chaveAtual

    def salvarArquivo(self):
        arquivo = open(self.diretorio, 'w', encoding=self.chaveAtual)
        texto = self.conteudo.conteudo.get(1.0, END)
        arquivo.write(texto)
        arquivo = open(self.diretorio, 'r', encoding=self.chaveAtual)
        self.mensagem = arquivo.read()
        arquivo.close()

    # Funções que verificam o estado do texto do conteúdo
    def verificarSalvamento(self, evento=None):
        if self.mensagem == self.conteudo.conteudo.get(0.0, END):
            self.title(f'{self.diretorio}   -   Bloco de Notas')
            self.arquivoSalvo = True
        else:
            self.title(f'{self.diretorio} * -   Bloco de Notas')
            self.arquivoSalvo = False

    def fecharJanela(self):
        self.verificarSalvamento()
        if self.janelaDeSalvar:
            self.janelaDeSalvar.lift()
        elif not self.arquivoSalvo:
            self.janelaDeSalvar = JanelaSalvar(self, 'fechar')
        else:
            self.destroy()

    # Outras funções
    def abrirApp(self):
        if os.name == 'nt':
            subprocess.call(['pythonw', 'aplicativo.pyw'])
        else:
            os.system('./aplicativo.pyw')

    def receberArquivo(self):
        if len(sys.argv) < 2:
            self.diretorio = 'Arquivo novo'
        else:
            self.diretorio = sys.argv[1]
            try:
                arquivo = open(self.diretorio)
                arquivo.close()
            except FileNotFoundError:
                self.diretorio = 'Arquivo novo'

    def verificarDiretorio(self):
        if self.diretorio != 'Arquivo novo':
            self.substituirConteudo()

    def substituirConteudo(self):
        self.tentarAbrir()
        self.conteudo.conteudo.delete(1.0, END)
        self.conteudo.conteudo.insert(END, self.mensagem)
        self.conteudo.conteudo.delete(float(self.conteudo.conteudo.index(END)) - 1.0)


if __name__ == '__main__':
    Aplicativo().mainloop()
