import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk

class FileViewerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Viewer App")
        self.geometry("800x600")

        self.frame1 = FileSelectionFrame(self)
        self.frame1.pack(fill="both", expand=True)

class FileSelectionFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.file_path_label = tk.Label(self, text="Nenhum arquivo selecionado")
        self.file_path_label.pack(pady=10)

        self.browse_button = tk.Button(self, text="Selecionar arquivo", command=self.open_file)
        self.browse_button.pack(pady=5)

        self.open_button = tk.Button(self, text="Abrir", command=self.open_file_viewer)
        self.open_button.pack(pady=5)

        self.master = master

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")])
        self.file_path_label.config(text=file_path)
        self.file_path = file_path

    def open_file_viewer(self):
        if hasattr(self, 'file_path'):
            self.master.frame2 = FileViewerFrame(self.master, self.file_path)
            self.master.frame2.pack(fill="both", expand=True)
            self.pack_forget()

class FileViewerFrame(tk.Frame):
    def __init__(self, master, file_path):
        super().__init__(master)

        self.master = master
        self.file_path = file_path

        # Ler o arquivo para um DataFrame
        self.data_frame = pd.read_excel(self.file_path) if self.file_path.endswith('.xlsx') else pd.read_csv(self.file_path)

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

        self.back_button = tk.Button(self, text="Voltar", command=self.back_to_file_selection)
        self.back_button.pack(pady=5)

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

    def back_to_file_selection(self):
        self.master.frame1.pack(fill="both", expand=True)
        self.pack_forget()

if __name__ == "__main__":
    app = FileViewerApp()
    app.mainloop()

