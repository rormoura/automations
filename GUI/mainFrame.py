import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
import os

from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from mainFiles.ABCCurve import ABCCurve

class App:
    def __init__(self, root):
        self.root = root

        self.arquivo_selecionado = None
        self.analise_selecionada = None
        self.pasta_criada = None

        # Criando o frame para o botão de criar pasta e o campo de entrada
        self.frame_criar_pasta = tk.Frame(self.root)
        self.frame_criar_pasta.pack(pady=30)

        # Label "Iniciar nova Pesquisa"
        self.lbl_iniciar_pesquisa = tk.Label(self.frame_criar_pasta, text="Iniciar nova Pesquisa:", font=("Helvetica", 16))
        self.lbl_iniciar_pesquisa.grid(row=0, column=0, columnspan=3, pady=10)

        # Label com a instrução sobre o arquivo Excel
        self.lbl_instrucao = tk.Label(self.frame_criar_pasta, text=("O arquivo Excel (.xlsx) deve conter SOMENTE o seguinte conteúdo:\n\nAs colunas na seguinte ordem:\n"
                                                                    "(Item, Discriminação, Unid, Quant, "
                                                                    "Valor Unit, Valor Total, Participação)"), font=("Helvetica", 10))
        self.lbl_instrucao.grid(row=1, column=0, columnspan=3, pady=5)

        # Rótulo para indicar o campo de entrada
        self.lbl_nome_pasta = tk.Label(self.frame_criar_pasta, text="Nome para pasta do edital:")
        self.lbl_nome_pasta.grid(row=2, column=0, columnspan=3, pady=5)

        # Botão para buscar arquivo
        self.btn_buscar_arquivo = tk.Button(self.frame_criar_pasta, text="Buscar Arquivo", command=self.buscar_arquivo)
        self.btn_buscar_arquivo.grid(row=3, column=0, padx=10)

        # Campo de entrada para o nome da pasta
        self.entrada_nome_pasta = tk.Entry(self.frame_criar_pasta, width=30, state='disabled')
        self.entrada_nome_pasta.bind('<Leave>', self.handle_leave_entry)
        self.entrada_nome_pasta.grid(row=3, column=1, padx=10)

        # Botão para criar a pasta
        self.btn_criar_pasta = tk.Button(self.frame_criar_pasta, text="Criar Pasta", command=self.criar_pasta, state='disabled')
        self.btn_criar_pasta.grid(row=3, column=2, padx=10)

        # Criando o frame para continuar pesquisa em andamento
        self.frame_continuar_pesquisa = tk.Frame(self.root)
        self.frame_continuar_pesquisa.pack(pady=30)

        # Label "Continuar pesquisa em andamento"
        self.lbl_continuar_pesquisa = tk.Label(self.frame_continuar_pesquisa, text="Continuar pesquisa em andamento:", font=("Helvetica", 16))
        self.lbl_continuar_pesquisa.pack(pady=10)

        self.lbl_instrucao_continuar_pesquisa = tk.Label(self.frame_continuar_pesquisa, text=("O arquivo Excel (.xlsx) selecionado deve ser uma Análise Completa"
                                                                                              " gerada previamente por esse aplicativo"), font=("Helvetica", 10))
        self.lbl_instrucao_continuar_pesquisa.pack(pady=5)

        # Botão "Selecionar Análise Completa"
        self.btn_continuar = tk.Button(self.frame_continuar_pesquisa, text="Selecionar Análise Completa", command=self.selecionar_analise)
        self.btn_continuar.pack(pady=10)

        # Botão "Próximo"
        self.btn_proximo = tk.Button(self.root, text="Próximo", command=self.proximo)
        self.btn_proximo.pack(side=tk.BOTTOM, pady=20)

    def handle_leave_entry(self, event):
        if(self.entrada_nome_pasta.get() != ""):
            self.btn_criar_pasta.config(state='normal')
        else:
            self.btn_criar_pasta.config(state='disabled')

    def buscar_arquivo(self):
        filename = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx")])
        if filename:
            self.arquivo_selecionado = filename
            self.entrada_nome_pasta.config(state='normal')
            self.btn_continuar.config(state='disabled')

    def selecionar_analise(self):
        if self.pasta_criada is None and self.analise_selecionada is None:
            nome_analise = filedialog.askopenfilename(title="Selecione o arquivo de Análise Completa já criada", filetypes=[("Arquivos Excel", "*.xlsx")])
            self.analise_selecionada = nome_analise
            self.btn_buscar_arquivo.config(state='disabled')


    def criar_pasta(self):
        nome_pasta = self.entrada_nome_pasta.get()
        self.entrada_nome_pasta.delete(0, tk.END)
        pasta_destino = filedialog.askdirectory(title="Selecione o diretório para criar a pasta")
        if nome_pasta and pasta_destino:
            caminho_completo = os.path.join(pasta_destino, nome_pasta)
            if not os.path.exists(caminho_completo):
                os.makedirs(caminho_completo)
                messagebox.showinfo("Sucesso","Pasta criada com sucesso!")
                self.pasta_criada = caminho_completo
            else:
                messagebox.showinfo("Erro", "Pasta já existe nesse diretório, escolha outro nome!")
        else:
            messagebox.showinfo("Erro", "Defina um nome para a pasta!")
    def proximo(self):
        aviso = ""
        if self.arquivo_selecionado and self.pasta_criada:
            self.arquivo_selecionado = ABCCurve(self.arquivo_selecionado, self.pasta_criada)
            self.root.event_generate("<<NextFrame>>")
        elif self.analise_selecionada:
            self.root.event_generate("<<NextFrame>>")
        else:
            if not self.pasta_criada and not self.arquivo_selecionado:
                aviso = ("Para iniciar uma nova pesquisa:\n * selecione um arquivo"
                         " e crie uma nova pasta\n\nPara continuar de onde parou:\n * selecione o arquivo de Análise Completa"
                          " da pesquisa em andamento")

        if aviso:
            messagebox.showinfo("Aviso", aviso)