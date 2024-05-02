import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

def browse_file():
    filename = filedialog.askopenfilename()
    if filename:
        label.config(text="Arquivo selecionado: " + filename)
        return filename  # Retorna o caminho do arquivo selecionado
    else:
        label.config(text="Nenhum arquivo selecionado")
        return None

root = tk.Tk()
root.title("File Browser")

browse_button = tk.Button(root, text="Navegar", command=browse_file)
browse_button.pack(pady=10)

label = tk.Label(root, text="")
label.pack()

arquivo_selecionado = browse_file()

root.mainloop()

filePath = arquivo_selecionado
curvaABC = pd.read_excel(filePath,index_col=0)
print(curvaABC)

