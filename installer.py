import PyInstaller.__main__

PyInstaller.__main__.run([
    'aplicativo.pyw',
    '--onefile',
    '--windowed',
    '--icon=arquivos/icone.ico',
    '--name=aplicativo',
    '--add-data=arquivos/icone.ico;.',
])
