import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
import os

def dotAndComma (df):
    if(df.dtype == object):
        df = df.apply(lambda x: float(x.replace('.', '')) if ('.' in x) else x)
        df = df.apply(lambda x: float(x.replace(',', '.')) if (',' in x) else x)
    return df

def ABCCurve(filePath):
    excelRaw = pd.read_excel(filePath)

    print("Arquivo em excel contendo apenas a tabela na seguinte ordem\n[ITEM] [DISCRIMINAÇÃO] [UNIDADE] [QUANTIDADE] [VALOR UNITÁRIO] [VALOR TOTAL] [PARTICIPAÇÃO]")
    maxNum = len(excelRaw)-1

    df = excelRaw
    ind = np.arange(1, maxNum+1, 1)

    df.insert(6,'VTC', dotAndComma(df[df.columns[3]]) * dotAndComma(df[df.columns[4]]))
    df.insert(7,'PERCENTUAL', df['VTC'] / sum(df['VTC']) * 100)

    ABC_curve = df.sort_values(by='PERCENTUAL', ascending=False)
    ABC_curve = ABC_curve.reset_index(drop=True)

    ABC_curve.index = ABC_curve.index + 1
    ABC_curve.index.name = "ABC"

    df["MÉDIA BPS"] = np.nan
    df["MÉDIA TCU"] = np.nan
    df["MÉDIA TCE"] = np.nan
    df["MÉDIA AIQ"] = np.nan
    df["MÉDIA CHAUVENET"] = np.nan

    df["DISTINTO EM RELAÇÃO À MÉDIA BPS"] = np.nan
    df["DISTINTO EM RELAÇÃO À MÉDIA TCU"] = np.nan
    df["DISTINTO EM RELAÇÃO À MÉDIA TCE"] = np.nan
    df["DISTINTO EM RELAÇÃO À MÉDIA AIQ"] = np.nan
    df["DISTINTO EM RELAÇÃO À MÉDIA CHAUVENET"] = np.nan

    df["ANÁLISE EM RELAÇÃO AO BPS"] = np.nan
    df["ANÁLISE EM RELAÇÃO AO TCU"] = np.nan
    df["ANÁLISE EM RELAÇÃO AO TCE"] = np.nan
    df["ANÁLISE EM RELAÇÃO AO AIQ"] = np.nan
    df["ANÁLISE EM RELAÇÃO AO "] = np.nan

    df["OBSERVAÇÕES"] = np.nan

    caminho_novo_arquivo = os.path.join(pasta_criada, 'olha a curva.xlsx')
    ABC_curve.to_excel(caminho_novo_arquivo)

def buscar_arquivo():
    filename = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx")])
    if filename:
        arquivo_selecionado_label.config(text="Arquivo selecionado: " + os.path.basename(filename))
        global arquivo_selecionado
        arquivo_selecionado = filename
        print(arquivo_selecionado)

def abrir_tutorial():
    # Adicione aqui a lógica para abrir um tutorial
    print("Abrir tutorial")

def proximo():
    global arquivo_selecionado, pasta_criada, pasta_selecionada
    aviso = ""
    if ((arquivo_selecionado != None) & (pasta_criada != None)):
        ABCCurve(arquivo_selecionado)
        aviso = "prosseguiu 1"
    elif (pasta_selecionada != None):
        aviso = "prosseguiu 2"
    elif ((pasta_criada == None)|(arquivo_selecionado == None)):

        if((pasta_criada == None) & (arquivo_selecionado == None)):
            aviso = "Para iniciar uma nova pesquisa:\n * selecione um arquivo" \
            " e crie uma nova pasta\n\nPara continuar de onde parou:\n * selecione a pasta da pesquisa em andamento"

    messagebox.showwarning("aviso", aviso)

def selecionar_pasta():
    global pasta_selecionada
    global pasta_criada
    if (pasta_criada == None) & (pasta_selecionada == None):
        nome_pasta = filedialog.askdirectory(title="Selecione o diretório para criar a pasta")
        status_label.config(text=f"Pasta '{os.path.basename(nome_pasta)} selecionada!")
        pasta_selecionada = nome_pasta
    else:
        status_label.config(text=f"A pasta que você criou já foi selecionada")

def criar_pasta():
    nome_pasta = entrada_nome_pasta.get()
    pasta_destino = filedialog.askdirectory(title="Selecione o diretório para criar a pasta")
    if nome_pasta and pasta_destino:
        caminho_completo = os.path.join(pasta_destino, nome_pasta)
        if not os.path.exists(caminho_completo):
            os.makedirs(caminho_completo)
            status_label.config(text=f"Pasta '{nome_pasta}' criada com sucesso!")
            global pasta_criada
            pasta_criada = nome_pasta
        else:
            status_label.config(text=f"Pasta '{nome_pasta}' já existe nesse diretório, escolha outro nome!")

# Criando a janela principal
root = tk.Tk()
root.title("Interface com Tkinter")
root.geometry("800x600")

arquivo_selecionado = None
pasta_selecionada = None
pasta_criada = None

# Criando o frame para os botões superiores
frame_superior = tk.Frame(root)
frame_superior.pack(pady=20)

# Botão para buscar arquivo
btn_buscar_arquivo = tk.Button(frame_superior, text="Buscar Arquivo", command=buscar_arquivo)
btn_buscar_arquivo.grid(row=0, column=0, padx=10)

# Botão "Continuar de onde parei"
btn_continuar = tk.Button(frame_superior, text="selecionar_pasta", command=selecionar_pasta)
btn_continuar.grid(row=0, column=1, padx=10)

# Botão para abrir tutorial
btn_abrir_tutorial = tk.Button(frame_superior, text="Tutorial", command=abrir_tutorial)
btn_abrir_tutorial.grid(row=0, column=2, padx=10)

# Criando o frame para o botão de criar pasta e o campo de entrada
frame_criar_pasta = tk.Frame(root)
frame_criar_pasta.pack(pady=30)


# Rótulo para indicar o campo de entrada
lbl_nome_pasta = tk.Label(frame_criar_pasta, text="Nome para pasta do edital:")
lbl_nome_pasta.grid(row=0, column=0)

# Campo de entrada para o nome da pasta
entrada_nome_pasta = tk.Entry(frame_criar_pasta, width=30)
entrada_nome_pasta.grid(row=1, column=0, padx=10)

# Botão para criar a pasta
btn_criar_pasta = tk.Button(frame_criar_pasta, text="Criar Pasta", command=criar_pasta)
btn_criar_pasta.grid(row=1, column=1, padx=10)

# Rótulo para exibir status da criação da pasta
status_label = tk.Label(root, text="")
status_label.pack(pady=20)

# Rótulo para exibir o arquivo selecionado
arquivo_selecionado_label = tk.Label(root, text="Nenhum arquivo selecionado")
arquivo_selecionado_label.pack(pady=20)

# Botão "Próximo"
btn_proximo = tk.Button(root, text="Próximo", command=proximo)
btn_proximo.pack(side=tk.BOTTOM, pady=20)

root.mainloop()
