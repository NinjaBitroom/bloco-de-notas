class BarraSuperior:
    def __init__(self, master):
        master.barraDeMenu.add_cascade(label='Arquivo', menu=master.menuDeArquivo)
        master.menuDeArquivo.add_command(label='Novo', command=master.novo)
        master.menuDeArquivo.add_command(label='Nova janela')
        master.menuDeArquivo.add_command(label='Carregar...', command=master.carregar)
        master.menuDeArquivo.add_command(label='Salvar', command=master.salvar)
        master.menuDeArquivo.add_command(label='Salvar como...', command=master.salvarComo)
        master.menuDeArquivo.add_separator()
        master.menuDeArquivo.add_command(label='Fechar', command=master.fecharJanela)
        master.menuDeArquivo.add_command(label='Fechar tudo', command=exit)

        master.barraDeMenu.add_cascade(label='Codificação', menu=master.menuDeCodigo)
        master.menuDeCodigo.add_command(label='UTF-8', command=lambda: master.mudarCodificacao('UTF-8'))
        master.menuDeCodigo.add_command(label='UTF-16', command=lambda: master.mudarCodificacao('UTF-16'))
        master.menuDeCodigo.add_command(label='UTF-32', command=lambda: master.mudarCodificacao('UTF-32'))
        master.menuDeCodigo.add_command(label='ASCII', command=lambda: master.mudarCodificacao('ASCII'))
        master.atual.config(menu=master.barraDeMenu)