import customtkinter as ctk
from functools import partial

from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from apiRequests.apiOpenData import obter_itens
from utilities.apiOpenData import unitFilter, cleanData, uniqueItems

class MultiSelectMenu(ctk.CTkToplevel):
    def __init__(self, master, values, variable, **kwargs):
        super().__init__(master, **kwargs)
        self.withdraw()
        self.overrideredirect(True)
        self.values = values
        self.variable = variable
        self.check_vars = {value: ctk.BooleanVar() for value in self.values}

        for value in self.values:
            chk = ctk.CTkCheckBox(self, text=value, variable=self.check_vars[value], command=self.update_value)
            chk.pack(anchor='w', padx=10, pady=2)

        self.bind("<FocusOut>", self.hide_menu)

    def show_menu(self, x, y):
        self.geometry(f"+{x}+{y}")
        self.deiconify()
        self.focus_force()

    def hide_menu(self, event):
        self.withdraw()

    def update_value(self):
        selected_values = [value for value, var in self.check_vars.items() if var.get()]
        self.variable.set(", ".join(selected_values))

    def get_selected_values(self):
        return [value for value, var in self.check_vars.items() if var.get()]

class MultiSelectButton(ctk.CTkButton):
    def __init__(self, master=None, values=None, **kwargs):
        self.var = ctk.StringVar(value="Selecionar Unidades")
        super().__init__(master, text="Selecionar Unidades", command=self.show_menu, **kwargs)

        self.values = values if values else ()
        self.menu = MultiSelectMenu(master, self.values, self.var)
        self.configure(width=100, height=30)

    def show_menu(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.menu.show_menu(x, y)

    def get_selected_values(self):
        return self.menu.get_selected_values()

def show_selected_values(df):
    selected_values = multi_select_button.get_selected_values()
    dfCompleto, df_reduzido = unitFilter(df, selected_values)
    print(dfCompleto)

def confirm_entry_value():
    entry_value = entry.get()
    print(f"Valor digitado: {entry_value}")

def validate_numeric_entry(new_value):
    if new_value.isdigit() or new_value == "":
        return True
    return False

# Exemplo de uso

root = ctk.CTk()
ctk.set_appearance_mode("System")
root.title("MultiSelect Menu")
root.geometry("400x400")

catmat = ("299605",)
df = cleanData(obter_itens(catmat))
items = uniqueItems(df)

# Adiciona um título e uma entrada acima do MultiSelectButton
label = ctk.CTkLabel(root, text="CATMAT:")
label.pack(anchor='center', pady=5)

# Cria um frame para a entry e o botão confirmar
entry_frame = ctk.CTkFrame(root, fg_color="transparent")  # Define a cor de fundo como transparente
entry_frame.pack(anchor='center', pady=5)

vcmd = (root.register(validate_numeric_entry), '%P')
entry = ctk.CTkEntry(entry_frame, width=100, validate="key", validatecommand=vcmd)
entry.pack(side='left', padx=5)

confirm_button = ctk.CTkButton(entry_frame, text="Confirmar",text_color="black", width=70, command=confirm_entry_value)
confirm_button.pack(side='left', padx=5)

# Adiciona o MultiSelectButton e o botão Concluir
multi_select_button = MultiSelectButton(
    root,
    fg_color="darkgrey",
    hover_color="grey",
    text_color="black",
    values=items,
)
multi_select_button.pack(pady=20, padx=5)

show_values_button = ctk.CTkButton(
    root,
    text="Concluir",
    text_color="black",
    command=partial(show_selected_values, df)
)
show_values_button.pack(side='bottom', pady=10)

root.mainloop()