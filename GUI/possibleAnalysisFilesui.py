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
        self.item_entry_label = tk.Label(self, text="Digite o número do item:")
        self.item_entry_label.grid(row=0, column=0, padx=2)

        vcmd = (self.register(self.validate_digit), '%P')

        self.item_entry = tk.Entry(self, validate='key', validatecommand=vcmd)
        self.item_entry.grid(row=0, column=1)

        self.possibleAnalysisFiles = ttk.Combobox(
            self, name="possibleanalysisfiles", 
            cursor="arrow", 
            exportselection=True, 
            justify="left", 
            state="disabled", 
            takefocus=False, 
            width=40, 
            values=('Arquivo .csv modelo BPS','Arquivo .csv modelo SIASG','Arquivo Excel (.xlsx) modelo Painel de Preços')
        )
        self.possibleAnalysisFiles.grid(row=0, column=2, padx=80)
        self.possibleAnalysisFiles.set("Selecionar Pesquisa de Preços")
        self.possibleAnalysisFiles.bind("<<ComboboxSelected>>", self.callbackComboBox)

        self.send_button = tk.Button(self, text="Enviar Pesquisa de Preço", command=self.handle_send_button, state='disabled')
        self.send_button.grid(row=0, column=3, padx=10)

        self.item_entry.bind('<Leave>', self.handle_leave)

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
                    print(BPS.bpsBpsAnalysis(file_path))
                    self.send_button.config(state='normal')
                if(selected_value== "Arquivo .csv modelo SIASG"):
                    print(SIASG.bpsSiasgAnalysis(file_path))
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
                        print(PANEL.panelAnalysis(file_paths_list))
                        self.send_button.config(state='normal')
                else:
                    break


    def validate_digit(self, P):
        if P.isdigit() or P == "":
            return True
        else:
            return False
    
    def print_list(lst):
        temp_str = ''
        for elem in lst:
            temp_str = temp_str+str(elem)+'\n'
        return temp_str

    def handle_leave(self, event):
        if(self.item_entry.get() != ""):
            self.possibleAnalysisFiles.config(state="readonly")
            self.send_button.config(state='disabled')
        else:
            self.possibleAnalysisFiles.config(state="disabled")
            self.possibleAnalysisFiles.set("Selecionar Pesquisa de Preços")
            self.send_button.config(state='disabled')

    def handle_send_button(self):
        print("xing")


if __name__ == "__main__":
    root = tk.Tk()
    app = PossibleAnalysisFilesUI(master=root)
    app.pack()
    root.mainloop()