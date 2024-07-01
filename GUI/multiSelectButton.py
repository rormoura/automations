import tkinter as tk

class MultiSelectMenu(tk.Frame):
    def __init__(self, master, values, variable, **kwargs):
        super().__init__(master, **kwargs)
        self.values = values
        self.variable = variable
        self.check_vars = {value: tk.BooleanVar() for value in self.values}

        for i, value in enumerate(self.values):
            chk = tk.Checkbutton(self, text=value, variable=self.check_vars[value], command=self.update_value)
            chk.grid(row=i, column=0, sticky='w', padx=10, pady=2)

        self.bind("<FocusOut>", self.hide_menu)

    def create_checkbuttons(self):
        for widget in self.winfo_children():
            widget.destroy()
        for i, value in enumerate(self.values):
            chk = tk.Checkbutton(self, text=value, variable=self.check_vars[value], command=self.update_value)
            chk.grid(row=i, column=0, sticky='w', padx=10, pady=2),

    def show_menu(self, x, y):
        self.place(x=x, y=y)
        self.lift()
        self.focus_force()

    def hide_menu(self, event=None):
        self.place_forget()

    def update_value(self):
        selected_values = [value for value, var in self.check_vars.items() if var.get()]
        self.variable.set(", ".join(selected_values))

    def get_selected_values(self):
        return [value for value, var in self.check_vars.items() if var.get()]
    
    def update_values(self, new_values):
        self.values = new_values
        self.check_vars = {value: tk.BooleanVar() for value in self.values}
        self.create_checkbuttons()

class MultiSelectButton(tk.Button):
    def __init__(self, master=None, values=None, **kwargs):
        self.var = tk.StringVar(value="Selecionar Unidades")
        super().__init__(master, text="Selecionar Unidades", command=self.show_menu, **kwargs)

        self.values = values if values else ()
        self.menu = MultiSelectMenu(master, self.values, self.var)
        self.configure(width=15, height=2)

    def show_menu(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.menu.show_menu(x, y)

    def get_selected_values(self):
        return self.menu.get_selected_values()
    
    def update_values(self, new_values):
        self.menu.update_values(new_values)