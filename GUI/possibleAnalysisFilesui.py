import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import tkinter.filedialog as fd
from functools import partial

from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from apiRequests.apiOpenData import obter_itens
from utilities.apiOpenData import cleanData, uniqueItems, unitFilter
from analysis.ApiOpenDataAnalysis import apiOpenDataAnalysis
import re

from multiSelectButton import MultiSelectMenu, MultiSelectButton

import numpy as np


class PossibleAnalysisFilesUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.build_ui()

    def build_ui(self):
        self.item_entry_label = tk.Label(self, text="Digite o número do item:")
        self.item_entry_label.grid(row=0, column=0, padx=2)

        vcmd = (self.register(self.validate_digit), '%P')

        self.item_entry = tk.Entry(self, validate='key', validatecommand=vcmd)
        self.item_entry.grid(row=0, column=1, padx=(0,50))

        self.catmat_entry_label = tk.Label(self, text="Digite o CATMAT do item:")
        self.catmat_entry_label.grid(row=0, column=2, padx=2)

        self.catmat_entry = tk.Entry(self, validate='key', state='disabled')
        self.catmat_entry.grid(row=0, column=3)

        self.catmat_invalid_label = tk.Label(self, text="", fg="red")
        self.catmat_invalid_label.grid(row=1, column=3)

        self.photo = tk.PhotoImage(master = self,file = "GUI/catmat-search.png") 
        self.catmat_search = tk.Button(self, text="Pesquisar CATMAT", height= 16, width=16, image = self.photo, command=self.handle_catmat_search_button, state='disabled')
        self.catmat_search.grid(row=0, column=4, padx=(1,0))

        # self.possibleAnalysisFiles = ttk.Combobox(
        #     self, name="possibleanalysisfiles", 
        #     cursor="arrow", 
        #     exportselection=True, 
        #     justify="left", 
        #     state="disabled", 
        #     takefocus=False, 
        #     width=40, 
        #     values=('','Remover Pesquisa')
        # )
        # self.possibleAnalysisFiles.grid(row=0, column=5, padx=80)
        # self.possibleAnalysisFiles.set("Selecionar Pesquisa de Preços")
        # self.possibleAnalysisFiles.bind("<<ComboboxSelected>>", self.callbackComboBox)

        self.multi_select_button = MultiSelectButton(
            self,
            fg="darkgrey",
            activebackground="grey",
            values=(),
            state='disabled'
        )
        self.multi_select_button.grid(row=0, column=5, padx=80)

        self.send_button = tk.Button(self, text="Confirmar Operação", command=self.handle_send_button, state='disabled')
        self.send_button.grid(row=0, column=6, padx=10)

        self.item_entry.bind('<Leave>', self.handle_leave_item_entry)
        self.catmat_entry.bind('<Leave>', self.handle_leave_catmat_entry)
        self.bind('<<GETCatMat>>', self.get_catmat)

    def callbackComboBox(self, event=None):
        selected_value = self.possibleAnalysisFiles.get()
        msgbox = tk.messagebox.askquestion(title='',message='Filtros Selecionados: '+'\n'+selected_value+'\n\n'+'Deseja prosseguir?',icon = 'question')
        analysis_return = apiOpenDataAnalysis(file_path)
        if(analysis_return == -1):
            self.possibleAnalysisFiles.config(state="readonly")
            self.possibleAnalysisFiles.set("Selecionar Pesquisa de Preços")
            self.send_button.config(state='disabled')
            self.master.event_generate("<<WrongFileFormat>>", data=selected_value)
        else:
            self.medians_dict = analysis_return
            self.send_button.config(state='normal')

    def validate_digit(self, P):
        if P.isdigit() or P == "":
            return True
        else:
            return False
    
    def print_list(self, lst):
        temp_str = ''
        for elem in lst:
            temp_str = temp_str+str(elem)+'\n'
        return temp_str

    def handle_leave_item_entry(self, event):
        if(self.item_entry.get() != ""):
            self.catmat_entry.config(state="normal")
            self.item_for_catmat = self.item_entry.get()
            self.master.event_generate("<<GetCatmat>>")
            self.handle_leave_catmat_entry(event)
            self.multi_select_button.config(state="disabled")
            self.send_button.config(state='disabled')
        else:
            self.catmat_invalid_label.config(text="")
            self.catmat_entry.delete(0, tk.END)
            self.catmat_entry.config(state="disabled")
            self.multi_select_button.config(state="disabled")
            self.send_button.config(state='disabled')

    def handle_leave_catmat_entry(self, event):
        if(self.catmat_entry.get() != "" and str(self.catmat_entry.get()) != 'nan'):
            if(self.valid_catmat(self.catmat_entry.get())):
                self.catmat_invalid_label.config(text="")
                self.catmat_search.config(state="active")
                self.multi_select_button.config(state="active")
                self.send_button.config(state='disabled')
            else:
                self.catmat_invalid_label.config(text="Digite um CATMAT válido", font=('Arial', 8))
                self.catmat_search.config(state="disabled")
                self.multi_select_button.config(state="disabled")
                self.send_button.config(state='disabled')
        else:
            self.catmat_invalid_label.config(text="")
            self.catmat_search.config(state="disabled")
            self.multi_select_buttons.config(state="disabled")
            self.send_button.config(state='disabled')

    def handle_send_button(self):
        self.multi_select_button.config(state="disabled")
        self.send_button.config(state='disabled')
        self.chosen_item = self.item_entry.get()
        self.item_entry.delete(0, tk.END)
        self.catmat_entry.delete(0, tk.END)
        self.catmat_entry.config(state="disabled")
        self.master.event_generate("<<ItemChosen>>")

    def handle_catmat_search_button(self):
        self.json_itens_obtidos = obter_itens(self.catmat_entry.get())
        self.itens_df = cleanData(self.json_itens_obtidos)
        self.itens_units = uniqueItems(self.itens_df)
        self.multi_select_button.update_values(self.itens_units)
        self.multi_select_button.config(state="active")
        self.send_button.config(state='disabled')

    def get_catmat(self, event):
        self.catmat_entry.delete(0, tk.END)
        if(self.master.found_catmat != 'nan'):
            self.catmat_entry.insert(tk.INSERT, self.master.found_catmat)
        
    def valid_catmat(self, event):
        # Definir o padrão regex para 6 ou 7 dígitos
        pattern = r'^\d{6,7}$'
        
        # Usar re.match para verificar se a string corresponde ao padrão
        if re.match(pattern, self.catmat_entry.get()):
            return True
        else:
            return False


if __name__ == "__main__":
    root = tk.Tk()
    app = PossibleAnalysisFilesUI(master=root)
    app.pack()
    root.mainloop()