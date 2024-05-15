import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd


class possibleAnalysisFilesUI:
    def __init__(self, master=None):
        # build ui
        tk1 = tk.Tk(master)
        tk1.configure(height=200, width=200)
        self.possibleAnalysisFiles = ttk.Combobox(
            tk1, name="possibleanalysisfiles")
        self.possibleAnalysisFiles.configure(
            cursor="arrow",
            exportselection=True,
            justify="right",
            state="readonly",
            takefocus=False,
            width=40,
            values=('Arquivo .csv modelo BPS','Arquivo .csv modelo SIASG','Arquivo Excel (.xlsx) modelo Painel de Preços'))
        self.possibleAnalysisFiles.pack(side="top")
        self.possibleAnalysisFiles.bind(
            "<<ComboboxSelected>>", self.callback, add="")

        # Main widget
        self.mainwindow = tk1

    def run(self):
        self.mainwindow.mainloop()

    def callback(self, event=None):
        selected_value = self.possibleAnalysisFiles.get()
        if selected_value == "Arquivo .csv modelo BPS" or selected_value == "Arquivo .csv modelo SIASG":
            file_path = fd.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
            msgbox = tk.messagebox.askquestion(title='',message='Arquivo selecionado: '+'\n'+file_path+'\n\n'+'Deseja prosseguir?',icon = 'question')

            while(msgbox == 'no'):
                file_path = fd.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
                msgbox = tk.messagebox.askquestion(title='',message='Arquivo selecionado: '+'\n'+file_path+'\n\n'+'Deseja prosseguir?',icon = 'question')

            print(file_path)

        elif selected_value == "Arquivo Excel (.xlsx) modelo Painel de Preços":
            file_paths = fd.askopenfilenames(filetypes=[("Arquivos Excel", "*.xlsx")])
            if file_paths:
                print("Arquivos selecionados:", file_paths)
            


if __name__ == "__main__":
    app = possibleAnalysisFilesUI()
    app.run()
