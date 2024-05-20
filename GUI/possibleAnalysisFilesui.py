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


class PossibleAnalysisFilesUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.build_ui()

    def build_ui(self):
        self.possibleAnalysisFiles = ttk.Combobox(
            self, name="possibleanalysisfiles", 
            cursor="arrow", 
            exportselection=True, 
            justify="left", 
            state="readonly", 
            takefocus=False, 
            width=40, 
            values=('Arquivo .csv modelo BPS','Arquivo .csv modelo SIASG','Arquivo Excel (.xlsx) modelo Painel de Preços')
        )
        self.possibleAnalysisFiles.pack(side="top")
        self.possibleAnalysisFiles.set("Selecionar Pesquisa de Preços")
        self.possibleAnalysisFiles.bind("<<ComboboxSelected>>", self.callback)

    def callback(self, event=None):

        selected_value = self.possibleAnalysisFiles.get()
        if selected_value == "Arquivo .csv modelo BPS" or selected_value == "Arquivo .csv modelo SIASG":
            file_path = fd.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
            if(file_path):
                msgbox = tk.messagebox.askquestion(title='',message='Arquivo selecionado: '+'\n'+file_path+'\n\n'+'Deseja prosseguir?',icon = 'question')

                while(msgbox == 'no'):
                    file_path = fd.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
                    msgbox = tk.messagebox.askquestion(title='',message='Arquivo selecionado: '+'\n'+file_path+'\n\n'+'Deseja prosseguir?',icon = 'question')

                if(selected_value== "Arquivo .csv modelo BPS"): return BPS.bpsBpsAnalysis(file_path)
                if(selected_value== "Arquivo .csv modelo SIASG"): return SIASG.bpsSiasgAnalysis(file_path)

        elif selected_value == "Arquivo Excel (.xlsx) modelo Painel de Preços":
            msgbox = 'no'
            while(msgbox == 'no'):
                file_paths = fd.askopenfilenames(filetypes=[("Arquivos Excel", "*.xlsx")])
                if(file_paths):
                    file_paths_list = list(file_paths)
                    msgbox = tk.messagebox.askquestion(title='',message='Arquivos selecionados: '+'\n'+print_list(file_paths_list)+'\n\n'+'Deseja adicionar mais algum arquivo?',icon = 'question')

                    while(msgbox == 'yes'):
                        file_paths = fd.askopenfilenames(filetypes=[("Arquivos Excel", "*.xlsx")])
                        file_paths_list = file_paths_list + list(file_paths)
                        file_paths_list = list(dict.fromkeys(file_paths_list))
                        msgbox = tk.messagebox.askquestion(title='',message='Arquivos selecionados: '+'\n'+print_list(file_paths_list)+'\n\n'+'Deseja adicionar mais algum arquivo?',icon = 'question')

                    msgbox = tk.messagebox.askquestion(title='',message='Seleção de arquivos total: '+'\n'+print_list(file_paths_list)+'\n\n'+'Deseja prosseguir?',icon = 'question')
                    if(msgbox == 'no'):
                        file_paths_list = []
                    else:
                        return PANEL.panelAnalysis(file_paths_list)
                else:
                    break
            
def print_list(lst):
    temp_str = ''
    for elem in lst:
        temp_str = temp_str+str(elem)+'\n'
    return temp_str

if __name__ == "__main__":
    root = tk.Tk()
    app = PossibleAnalysisFilesUI(master=root)
    app.pack()
    root.mainloop()