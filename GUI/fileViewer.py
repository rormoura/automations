import pandas as pd
import tkinter as tk
from tkinter import ttk
import possibleAnalysisFilesui as analysis

class FileViewerFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.init_ui()

    def init_ui(self):
        self.arquivo_selecionado = None
        self.pasta_selecionada = None
        self.pasta_criada = None

        self.frame1 = None
        self.frame2 = ControlFrame(self)

        self.grid_frames()

    def grid_frames(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        if self.frame1:
            self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame2.grid(row=1, column=0, sticky="ew")

    def update_values(self, arquivo_selecionado, pasta_selecionada, pasta_criada):
        self.arquivo_selecionado = arquivo_selecionado
        self.pasta_selecionada = pasta_selecionada
        self.pasta_criada = pasta_criada

        self.open_file_viewer(self.arquivo_selecionado, self.pasta_selecionada)

    def open_file_viewer(self, arquivo_selecionado, pasta_selecionada):
        if arquivo_selecionado:
            if self.frame1 is not None:
                self.frame1.destroy()
            self.frame1 = DataViewerFrame(self, arquivo_selecionado)
            #self.frame1.bind("<<ItemChosen>>", self.frame1.item_chosen)
            self.grid_frames()
            print(arquivo_selecionado)
        elif pasta_selecionada:
            print("ainda nao fiz")

class DataViewerFrame(tk.Frame):
    def __init__(self, master, file_path):
        super().__init__(master)
        self.file_path = file_path
        self.bind("<<ItemChosen>>", self.item_chosen)
        self.data_frame = pd.read_excel(self.file_path) if self.file_path.endswith('.xlsx') else pd.read_csv(self.file_path)
        self.analysisUI = analysis.PossibleAnalysisFilesUI(self)
        self.analysisUI.pack(side=tk.TOP, padx=10, pady=10)

        style = ttk.Style()
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=60,
                        fieldbackground="white")
        style.map("Treeview", background=[("selected", "blue")])

        style.configure("Treeview.Heading",
                        font=("Helvetica", 10, "bold"),
                        background="grey",
                        foreground="black")

        self.tree = ttk.Treeview(self, columns=list(self.data_frame.columns), show="headings")

        self.yscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.xscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)

        self.tree.configure(yscrollcommand=self.yscrollbar.set, xscrollcommand=self.xscrollbar.set)

        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for col in self.data_frame.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=100)

        for i, row in self.data_frame.iterrows():
            values = [self.wrap_text(str(value)) for value in row]
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            self.tree.insert("", "end", values=values, tags=(tag,))

        self.tree.tag_configure('oddrow', background='lightgrey')
        self.tree.tag_configure('evenrow', background='white')

    def item_chosen(self, event):
        self.data_frame.loc[self.data_frame['ITEM'] == int(self.analysisUI.chosen_item), 'MÉDIA BPS'] = self.analysisUI.medians_dict['BPS']
        self.data_frame.loc[self.data_frame['ITEM'] == int(self.analysisUI.chosen_item), 'MÉDIA TCU'] = self.analysisUI.medians_dict['TCU']
        self.data_frame.loc[self.data_frame['ITEM'] == int(self.analysisUI.chosen_item), 'MÉDIA TCE'] = self.analysisUI.medians_dict['TCE']
        self.data_frame.loc[self.data_frame['ITEM'] == int(self.analysisUI.chosen_item), 'MÉDIA AIQ'] = self.analysisUI.medians_dict['AIQ']
        self.data_frame.loc[self.data_frame['ITEM'] == int(self.analysisUI.chosen_item), 'MÉDIA CHAUVENET'] = self.analysisUI.medians_dict['Chauvenet']
        self.data_frame.to_excel(self.file_path, index=False)
        self.refresh_treeview()

    def refresh_treeview(self):
        # Remove all current rows in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert updated rows
        for i, row in self.data_frame.iterrows():
            values = [self.wrap_text(str(value)) for value in row]
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            if(i == 3):
                print(values)
            self.tree.insert("", "end", values=values, tags=(tag,))

        self.tree.tag_configure('oddrow', background='lightgrey')
        self.tree.tag_configure('evenrow', background='white')

    def wrap_text(self, text):
        width = 60 if len(text) < 60 else len(text) / 2
        lines = []
        line = ''
        for word in text.split():
            if len(line) + len(word) <= width:
                line += word + ' '
            else:
                lines.append(line)
                line = word + ' '
        lines.append(line)
        return '\n'.join(lines)

class ControlFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.finish_button = tk.Button(self, text="Concluir", command=self.finish)
        self.finish_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def finish(self):
        self.master.quit()
