import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk

class FileViewerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Viewer App")
        self.geometry("600x400")
        
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
        
        self.data_frame = pd.read_excel(self.file_path) if self.file_path.endswith('.xlsx') else pd.read_csv(self.file_path)
        
        self.tree = ttk.Treeview(self, columns=list(self.data_frame.columns), show="headings", style="Custom.Treeview")
        for col in self.data_frame.columns:
            self.tree.heading(col, text=col)
        
        for index, row in self.data_frame.iterrows():
            self.tree.insert("", "end", values=list(row))
        
        self.tree.pack(expand=True, fill="both")
        
        ttk.Style().configure("Custom.Treeview.Heading", background="grey", foreground="black")
        
        yscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        yscrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=yscrollbar.set)
        
        xscrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        xscrollbar.pack(side='bottom', fill='x')
        self.tree.configure(xscrollcommand=xscrollbar.set)
        
        self.back_button = tk.Button(self, text="Voltar", command=self.back_to_file_selection)
        self.back_button.pack(pady=5)
    
    def back_to_file_selection(self):
        self.master.frame1.pack(fill="both", expand=True)
        self.pack_forget()


if __name__ == "__main__":
    app = FileViewerApp()
    app.mainloop()