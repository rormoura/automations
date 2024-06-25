import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd

from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))


import analysis.BpsBpsAnalysis as BPS
import analysis.BpsSiasgAnalysis as SIASG
import analysis.PanelAnalysis as PANEL

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

        self.possibleAnalysisFiles = ttk.Combobox(
            self, name="possibleanalysisfiles", 
            cursor="arrow", 
            exportselection=True, 
            justify="left", 
            state="disabled", 
            takefocus=False, 
            width=40, 
            values=('Arquivo .csv modelo BPS','Arquivo .csv modelo SIASG','Arquivo Excel (.xlsx) modelo Painel de Preços','Remover Pesquisa')
        )
        self.possibleAnalysisFiles.grid(row=0, column=4, padx=80)
        self.possibleAnalysisFiles.set("Selecionar Pesquisa de Preços")
        self.possibleAnalysisFiles.bind("<<ComboboxSelected>>", self.callbackComboBox)

        self.send_button = tk.Button(self, text="Confirmar Operação", command=self.handle_send_button, state='disabled')
        self.send_button.grid(row=0, column=5, padx=10)

        self.item_entry.bind('<Leave>', self.handle_leave_item_entry)
        self.catmat_entry.bind('<Leave>', self.handle_leave_catmat_entry)
        self.bind('<<GETCatMat>>', self.get_catmat)

    def callbackComboBox(self, event=None):

        selected_value = self.possibleAnalysisFiles.get()
        if selected_value == "Arquivo .csv modelo BPS" or selected_value == "Arquivo .csv modelo SIASG":
            file_path = fd.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
            if(file_path):
                msgbox = tk.messagebox.askquestion(title='',message='Arquivo selecionado: '+'\n'+file_path+'\n\n'+'Deseja prosseguir?',icon = 'question')

                while(msgbox == 'no'):
                    file_path = fd.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
                    msgbox = tk.messagebox.askquestion(title='',message='Arquivo selecionado: '+'\n'+file_path+'\n\n'+'Deseja prosseguir?',icon = 'question')

                if(selected_value== "Arquivo .csv modelo BPS"):
                    analysis_return = BPS.bpsBpsAnalysis(file_path)
                    if(analysis_return == -1):
                        self.possibleAnalysisFiles.config(state="readonly")
                        self.possibleAnalysisFiles.set("Selecionar Pesquisa de Preços")
                        self.send_button.config(state='disabled')
                        self.master.event_generate("<<WrongFileFormat>>", data=selected_value)
                    else:
                        self.medians_dict = analysis_return
                        self.send_button.config(state='normal')
                if(selected_value== "Arquivo .csv modelo SIASG"):
                    analysis_return = SIASG.bpsSiasgAnalysis(file_path)
                    if(analysis_return == -1):
                        self.possibleAnalysisFiles.config(state="readonly")
                        self.possibleAnalysisFiles.set("Selecionar Pesquisa de Preços")
                        self.send_button.config(state='disabled')
                        self.master.event_generate("<<WrongFileFormat>>", data=selected_value)
                    else:
                        self.medians_dict = analysis_return
                        self.send_button.config(state='normal')

        elif selected_value == "Arquivo Excel (.xlsx) modelo Painel de Preços":
            msgbox = 'no'
            while(msgbox == 'no'):
                file_paths = fd.askopenfilenames(filetypes=[("Arquivos Excel", "*.xlsx")])
                if(file_paths):
                    file_paths_list = list(file_paths)
                    msgbox = tk.messagebox.askquestion(title='',message='Arquivos selecionados: '+'\n'+self.print_list(file_paths_list)+'\n\n'+'Deseja adicionar mais algum arquivo?',icon = 'question')

                    while(msgbox == 'yes'):
                        file_paths = fd.askopenfilenames(filetypes=[("Arquivos Excel", "*.xlsx")])
                        file_paths_list = file_paths_list + list(file_paths)
                        file_paths_list = list(dict.fromkeys(file_paths_list))
                        msgbox = tk.messagebox.askquestion(title='',message='Arquivos selecionados: '+'\n'+self.print_list(file_paths_list)+'\n\n'+'Deseja adicionar mais algum arquivo?',icon = 'question')

                    msgbox = tk.messagebox.askquestion(title='',message='Seleção de arquivos total: '+'\n'+self.print_list(file_paths_list)+'\n\n'+'Deseja prosseguir?',icon = 'question')
                    if(msgbox == 'no'):
                        file_paths_list = []
                    else:
                        analysis_return = PANEL.panelAnalysis(file_paths_list)
                        if(analysis_return == -1):
                            self.possibleAnalysisFiles.config(state="readonly")
                            self.possibleAnalysisFiles.set("Selecionar Pesquisa de Preços")
                            self.send_button.config(state='disabled')
                            self.master.event_generate("<<WrongFileFormat>>", data=selected_value)
                        else:
                            self.medians_dict = analysis_return
                            self.send_button.config(state='normal')
                else:
                    break
        elif selected_value == "Remover Pesquisa":
            self.medians_dict = {'BPS': np.nan, 'TCU': np.nan, 'TCE': np.nan, 'AIQ': np.nan, 'Chauvenet': np.nan}
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
            self.possibleAnalysisFiles.config(state="disabled")
            self.send_button.config(state='disabled')
        else:
            self.catmat_entry.delete(0, tk.END)
            self.catmat_entry.config(state="disabled")
            self.possibleAnalysisFiles.config(state="disabled")
            self.possibleAnalysisFiles.set("Selecionar Pesquisa de Preços")
            self.send_button.config(state='disabled')

    def handle_leave_catmat_entry(self, event):
        if(self.catmat_entry.get() != "" and str(self.catmat_entry.get()) != 'nan'):
            self.possibleAnalysisFiles.config(state="readonly")
            self.send_button.config(state='disabled')
        else:
            self.possibleAnalysisFiles.config(state="disabled")
            self.possibleAnalysisFiles.set("Selecionar Pesquisa de Preços")
            self.send_button.config(state='disabled')

    def handle_send_button(self):
        self.possibleAnalysisFiles.config(state="disabled")
        self.possibleAnalysisFiles.set("Selecionar Pesquisa de Preços")
        self.send_button.config(state='disabled')
        self.chosen_item = self.item_entry.get()
        self.item_entry.delete(0, tk.END)
        self.catmat_entry.delete(0, tk.END)
        self.catmat_entry.config(state="disabled")
        self.master.event_generate("<<ItemChosen>>")

    def get_catmat(self, event):
        self.catmat_entry.delete(0, tk.END)
        if(self.master.found_catmat != 'nan'):
            self.catmat_entry.insert(tk.INSERT, self.master.found_catmat)

if __name__ == "__main__":
    root = tk.Tk()
    app = PossibleAnalysisFilesUI(master=root)
    app.pack()
    root.mainloop()