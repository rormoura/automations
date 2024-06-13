import tkinter as tk
from mainFrame import App
from fileViewer import FileViewerFrame
import os

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicativo de Pesquisa de Preços")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "tce-icon.ico")

        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Erro ao definir o ícone: {e}")

        self.root.geometry("800x600")

        self.arquivo_selecionado = None
        self.analise_selecionada = None
        self.pasta_criada = None

        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)

        self.app = App(self.frame1)
        self.app.root.bind("<<NextFrame>>", self.switch_to_frame2)

        self.file_viewer_frame = FileViewerFrame(self.frame2)
        self.file_viewer_frame.root.bind("<<PreviousFrame>>", self.switch_to_frame1)
        self.file_viewer_frame.pack(fill="both", expand=True)

        # self.frame_navegacao = tk.Frame(self.frame2)
        # self.frame_navegacao.pack(pady=20)

        # self.btn_voltar = tk.Button(self.frame_navegacao, text="Voltar ao Frame 1", command=self.switch_to_frame1)
        # self.btn_voltar.pack(side=tk.LEFT, padx=10)

        self.frame1.pack(fill="both", expand=True)
        self.frame2.pack_forget()

    def switch_to_frame1(self, event=None):
        self.frame2.pack_forget()
        self.app.arquivo_selecionado = None
        self.app.analise_selecionada = None
        self.app.pasta_criada = None
        self.app.btn_buscar_arquivo.config(state='normal')
        self.app.entrada_nome_pasta.config(state='disabled')
        self.app.btn_criar_pasta.config(state='disabled')
        self.app.btn_continuar.config(state='normal')
        self.app.btn_cancelar_continuar.destroy()
        self.frame1.pack(fill="both", expand=True)

    def switch_to_frame2(self, event=None):
        arquivo_selecionado = self.app.arquivo_selecionado
        analise_selecionada = self.app.analise_selecionada
        pasta_criada = self.app.pasta_criada
        print(arquivo_selecionado,analise_selecionada,pasta_criada)

        self.frame1.pack_forget()
        self.frame2.pack(fill="both", expand=True)
        self.file_viewer_frame.update_values(arquivo_selecionado, analise_selecionada, pasta_criada)

if __name__ == "__main__":
    root = tk.Tk()
    main_app = MainApp(root)
    root.mainloop()