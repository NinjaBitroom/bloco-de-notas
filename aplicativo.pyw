#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog

import threading
import chardet
import logging
import sys

from aspecto import Aspecto
from widgets.barrasuperior import BarraSuperior
from widgets.conteudo import Conteudo
from widgets.barrainferior import BarraInferior
from widgets.janelasalvar import JanelaSalvar


logging.basicConfig(filename='debug.log', level=logging.DEBUG)


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

        self.mensagem = ''
        self.bytes = bytes(self.mensagem, self.chaveAtual)

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
        with open(self.diretorio, 'rb') as arquivo:
            self.bytes = arquivo.read()
        try:
            self.mensagem = self.bytes.decode(self.chaveAtual)
        except UnicodeDecodeError:
            chute = chardet.detect(self.bytes)
            self.mensagem = self.bytes.decode(chute['encoding'])
            self.chaveAtual = chute['encoding']
        finally:
            self.barraInferior.status['text'] = self.chaveAtual

    def salvarArquivo(self):
        with open(self.diretorio, 'wb') as arquivo:
            texto = self.conteudo.conteudo.get(0.0, END)[:-1]
            self.bytes = texto.encode(self.chaveAtual)
            arquivo.write(self.bytes)
            self.mensagem = self.bytes.decode(self.chaveAtual)

    # Funções que verificam o estado do texto do conteúdo
    def verificarSalvamento(self, evento=None):
        if self.mensagem == self.conteudo.conteudo.get(0.0, END)[:-1]:
            self.title(f'{self.diretorio}   -   Bloco de Notas')
            self.arquivoSalvo = True
        else:
            self.title(f'{self.diretorio} * -   Bloco de Notas')
            self.arquivoSalvo = False

        self.bytes = bytes(self.mensagem, self.chaveAtual)

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
        from aplicativo import executar
        executar()

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
        self.conteudo.conteudo.replace(0.0, END, self.mensagem)


def executar():
    Aplicativo().mainloop()


if __name__ == '__main__':
    executar()
