import pandas as pd
import tkinter as tk
from tkinter import ttk
import possibleAnalysisFilesui as analysis
import re

class FileViewerFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.root = master
        self.init_ui()

    def init_ui(self):
        self.arquivo_selecionado = None
        self.analise_selecionada = None
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

    def update_values(self, arquivo_selecionado, analise_selecionada, pasta_criada):
        self.arquivo_selecionado = arquivo_selecionado
        self.analise_selecionada = analise_selecionada
        self.pasta_criada = pasta_criada

        self.open_file_viewer(self.arquivo_selecionado, self.analise_selecionada)

    def open_file_viewer(self, arquivo_selecionado, analise_selecionada):
        if arquivo_selecionado:
            if self.frame1 is not None:
                self.frame1.destroy()
            self.frame1 = DataViewerFrame(self, arquivo_selecionado)
            self.grid_frames()
            print(arquivo_selecionado)
        elif analise_selecionada:
            if self.frame1 is not None:
                self.frame1.destroy()
            self.frame1 = DataViewerFrame(self, analise_selecionada)
            self.grid_frames()
            print(analise_selecionada)

class DataViewerFrame(tk.Frame):
    def __init__(self, master, file_path):
        super().__init__(master)
        self.master = master
        self.file_path = file_path
        self.bind("<<ItemChosen>>", self.item_chosen)
        self.bind("<<WrongFileFormat>>", self.wrong_file_format)
        self.bind("<<GetCatmat>>", self.get_catmat)
        self.data_frame = pd.read_excel(self.file_path) if self.file_path.endswith('.xlsx') else pd.read_csv(self.file_path)

        self.data_frame[self.data_frame.columns[3]] = self.data_frame[self.data_frame.columns[3]].astype('str')
        self.data_frame[self.data_frame.columns[3]] = self.data_frame[self.data_frame.columns[3]].map(lambda x: re.sub(r'\.\d+', '', x))

        expectated_columns = ["MÉDIA BPS", "MÉDIA TCU", "MÉDIA TCE", "MÉDIA AIQ", "MÉDIA CHAUVENET",
                              "% MÉDIA BPS", "% MÉDIA TCU", "% MÉDIA TCE", "% MÉDIA AIQ", "% MÉDIA CHAUVENET"]

        if(not (all(column in self.data_frame.columns for column in expectated_columns) and list(self.data_frame.columns[11:21]) == expectated_columns)):
            tk.messagebox.showinfo("Erro", "Selecione um Arquivo de Análise Completa Formatado Corretamente!")
            self.master.root.event_generate("<<PreviousFrame>>")

        drop_columns = ["ABC", "MÉDIA BPS", "MÉDIA TCU", "MÉDIA AIQ", "MÉDIA CHAUVENET",
                        "% MÉDIA BPS", "% MÉDIA TCU", "% MÉDIA AIQ", "% MÉDIA CHAUVENET", self.data_frame.columns[10]]
        self.data_frame_clean = self.data_frame.drop(columns=drop_columns)

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

        self.tree = ttk.Treeview(self, columns=list(self.data_frame_clean.columns), show="headings")

        self.yscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.xscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)

        self.tree.configure(yscrollcommand=self.yscrollbar.set, xscrollcommand=self.xscrollbar.set)

        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree.bind('<Double-1>', self.on_double_click)


        for col in self.data_frame_clean.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=100)
            
        # Insert updated rows
        for i, row in self.data_frame_clean.iterrows():
            values = [value for value in row]
            values[1] = self.wrap_text(str(values[1]))
            if(str(values[9]) != 'nan'):
                tag = 'chosen'
            else:
                tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            self.tree.insert("", "end", values=values, tags=(tag,))

        self.tree.tag_configure('oddrow', background='lightgrey')
        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('chosen', background='lightblue')
    

    def on_double_click(self, event):
        # Obter o item clicado
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if item:
            self.open_popup(item)
    
    def open_popup(self, item):
        values = list(self.tree.item(item, 'values'))
        popup = tk.Toplevel()
        popup.title("Adicionar Observação")

        label = tk.Label(popup, text="Observação Item: " + str(int(values[0])))
        label.pack(pady=10)

        # Obter o valor atual da célula
        current_value = self.tree.item(item, 'values')[11]
        initial_text = 'Adicionar'
        is_placeholder = current_value == initial_text
        if is_placeholder:
            current_value = ''

        text_box = tk.Text(popup, width=50, height=10)
        text_box.pack(pady=10)
        text_box.insert('1.0', current_value)
        text_box.focus()

        def save_comment():
            new_value = text_box.get('1.0', tk.END).strip()
            values = list(self.tree.item(item, 'values'))
            values[11] = new_value if new_value != '' else initial_text

            self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(values[0]), 'OBSERVAÇÕES'] = str(values[11])
            self.data_frame_clean.loc[self.data_frame_clean[self.data_frame_clean.columns[0]] == int(values[0]), 'OBSERVAÇÕES'] = str(values[11])

            popup.destroy()
            self.data_frame.to_excel(self.file_path, index=False)
            self.refresh_treeview()

        save_button = tk.Button(popup, text="Salvar", command=save_comment)
        save_button.pack(pady=10)

        popup.transient(self.tree)
        popup.grab_set()
        self.tree.wait_window(popup)

    def item_chosen(self, event): #Obs.: 'self.data_frame[self.data_frame.columns[1]]' DEVE SER a coluna 'ITEM'
        self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), 'MÉDIA BPS'] = self.analysisUI.medians_dict['BPS']
        self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), 'MÉDIA TCU'] = self.analysisUI.medians_dict['TCU']
        self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), 'MÉDIA TCE'] = self.analysisUI.medians_dict['TCE']
        self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), 'MÉDIA AIQ'] = self.analysisUI.medians_dict['AIQ']
        self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), 'MÉDIA CHAUVENET'] = self.analysisUI.medians_dict['Chauvenet']
        
        if(self.analysisUI.medians_dict['TCE'] == 'nan'):
            self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), '% MÉDIA BPS'] = 'nan'
            self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), '% MÉDIA TCU'] = 'nan'
            self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), '% MÉDIA TCE'] = 'nan'
            self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), '% MÉDIA AIQ'] = 'nan'
            self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), '% MÉDIA CHAUVENET'] = 'nan'
        else:
            unitary_price = self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), self.data_frame.columns[6]]
            unitary_price = unitary_price.iloc[0]
            self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), '% MÉDIA BPS'] = ((unitary_price - self.analysisUI.medians_dict['BPS'])/self.analysisUI.medians_dict['BPS'])*100
            self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), '% MÉDIA TCU'] = ((unitary_price - self.analysisUI.medians_dict['TCU'])/self.analysisUI.medians_dict['TCU'])*100
            self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), '% MÉDIA TCE'] = ((unitary_price - self.analysisUI.medians_dict['TCE'])/self.analysisUI.medians_dict['TCE'])*100
            self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), '% MÉDIA AIQ'] = ((unitary_price - self.analysisUI.medians_dict['AIQ'])/self.analysisUI.medians_dict['BPS'])*100
            self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.chosen_item), '% MÉDIA CHAUVENET'] = ((unitary_price - self.analysisUI.medians_dict['Chauvenet'])/self.analysisUI.medians_dict['Chauvenet'])*100

        #DAQUI PRA BAIXO FAZ PARTE DO DATAFRAME CLEAN
        self.data_frame_clean.loc[self.data_frame_clean[self.data_frame_clean.columns[0]] == int(self.analysisUI.chosen_item), 'MÉDIA TCE'] = self.analysisUI.medians_dict['TCE']

        if(self.analysisUI.medians_dict['TCE'] == 'nan'):
            self.data_frame_clean.loc[self.data_frame_clean[self.data_frame_clean.columns[0]] == int(self.analysisUI.chosen_item), '% MÉDIA TCE'] = 'nan'
        else:
            unitary_price = self.data_frame_clean.loc[self.data_frame_clean[self.data_frame_clean.columns[0]] == int(self.analysisUI.chosen_item), self.data_frame_clean.columns[5]]
            unitary_price = unitary_price.iloc[0]
            self.data_frame_clean.loc[self.data_frame_clean[self.data_frame_clean.columns[0]] == int(self.analysisUI.chosen_item), '% MÉDIA TCE'] = ((unitary_price - self.analysisUI.medians_dict['TCE'])/self.analysisUI.medians_dict['TCE'])*100
        #FINALIZADA PARTE DO DATAFRAME CLEAN

        self.data_frame.to_excel(self.file_path, index=False)
        self.refresh_treeview()

    def refresh_treeview(self):
        # Remove all current rows in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert updated rows
        for i, row in self.data_frame_clean.iterrows():
            values = [value for value in row]
            values[1] = self.wrap_text(str(values[1]))
            if(str(values[9]) != 'nan'):
                tag = 'chosen'
            else:
                tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            self.tree.insert("", "end", values=values, tags=(tag,))

        self.tree.tag_configure('oddrow', background='lightgrey')
        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('chosen', background='lightblue')

    def wrong_file_format(self, event):
        tk.messagebox.showinfo("Erro", "Selecione um Arquivo de Pesquisa Formatado Corretamente!")

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
    
    def get_catmat(self, event):
        respective_catmat = self.data_frame.loc[self.data_frame[self.data_frame.columns[1]] == int(self.analysisUI.item_for_catmat), self.data_frame.columns[3]]
        respective_catmat = respective_catmat.iloc[0]
        self.found_catmat = respective_catmat
        self.analysisUI.event_generate("<<GETCatMat>>")

class ControlFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.back_button = tk.Button(self, text="Voltar", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.finish_button = tk.Button(self, text="Concluir", command=self.finish)
        self.finish_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def finish(self):
        self.master.quit()

    def go_back(self):
        self.master.root.event_generate("<<PreviousFrame>>")
