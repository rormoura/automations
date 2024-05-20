import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk
import possibleAnalysisFilesui as analysis

class FileViewerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Viewer App")
        self.geometry("800x600")

        self.frame1 = FileSelectionFrame(self)
        self.frame1.pack(fill="x")

        self.frame2 = None

        self.frame3 = ControlFrame(self)
        self.frame3.pack(side=tk.BOTTOM, fill="x")

class FileSelectionFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.browse_button = tk.Button(self, text="Selecionar arquivo", command=self.open_file)
        self.browse_button.grid(row=0, column=0, padx=10, pady=10)

        self.open_button = tk.Button(self, text="Abrir", command=self.open_file_viewer)
        self.open_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.file_path_label = tk.Label(self, text="Nenhum arquivo selecionado")
        self.file_path_label.grid(row=0, column=2, padx=10, pady=10)

        self.file_path = None

        self.browse_button.grid_columnconfigure(0, weight=1)
        self.open_button.grid_columnconfigure(1, weight=1)
        self.file_path_label.grid_columnconfigure(2, weight=1)

        self.line_canvas = tk.Canvas(self, height=2, bg="black")
        self.line_canvas.grid(row=1, column=0, sticky="ew", columnspan = 3)

        self.grid_columnconfigure(0, weight=1)


    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")])
        if file_path:
            self.file_path_label.config(text=file_path)
            self.file_path = file_path

    def open_file_viewer(self):
        if self.file_path:
            if self.master.frame2:
                self.master.frame2.destroy()
            self.master.frame2 = FileViewerFrame(self.master, self.file_path)
            self.master.frame2.pack(fill="both", expand=True)

class FileViewerFrame(tk.Frame):
    def __init__(self, master, file_path):
        super().__init__(master)

        self.master = master
        self.file_path = file_path

        # Ler o arquivo para um DataFrame
        self.data_frame = pd.read_excel(self.file_path) if self.file_path.endswith('.xlsx') else pd.read_csv(self.file_path)
        self.analysisUI = analysis.PossibleAnalysisFilesUI(self)
        self.analysisUI.pack( padx=10, pady=10)
        # Configurar estilos para Treeview
        style = ttk.Style()
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=60,  # Aumente a altura da linha para permitir múltiplas linhas de texto
                        fieldbackground="white")
        style.map("Treeview", background=[("selected", "blue")])

        style.configure("Treeview.Heading",
                        font=("Helvetica", 10, "bold"),
                        background="grey",
                        foreground="black")

        # Configurar Treeview com Scrollbars
        self.tree = ttk.Treeview(self, columns=list(self.data_frame.columns), show="headings")

        self.yscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.xscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)

        self.tree.configure(yscrollcommand=self.yscrollbar.set, xscrollcommand=self.xscrollbar.set)

        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adicionar cabeçalhos às colunas
        for col in self.data_frame.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=100)

        # Adicionar linhas de dados com cores alternadas e texto em múltiplas linhas
        for i, row in self.data_frame.iterrows():
            values = [self.wrap_text(str(value)) for value in row]
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            self.tree.insert("", "end", values=values, tags=(tag,))

        self.tree.tag_configure('oddrow', background='lightgrey')
        self.tree.tag_configure('evenrow', background='white')
        
    def wrap_text(self, text):
        """
        Quebra o texto em múltiplas linhas, quebrando apenas nos espaços.
        """
        width = 0
        if (len(text) < 60):
            width = 60
        else:
            width = len(text)/2
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

        self.back_button = tk.Button(self, text="Voltar", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.finish_button = tk.Button(self, text="Concluir", command=self.finish)
        self.finish_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def go_back(self):
        # Implementar a funcionalidade do botão Voltar
        if self.master.frame2:
            self.master.frame2.destroy()
            self.master.frame2 = None

    def finish(self):
        # Implementar a funcionalidade do botão Concluir
        self.master.quit()
    

if __name__ == "__main__":
    app = FileViewerApp()
    app.mainloop()
