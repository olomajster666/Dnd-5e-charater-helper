import tkinter as tk
from tkinter import messagebox

STANDARD_ARRAY = [15, 14, 13, 12, 10, 8]
ABILITIES = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]

class StepStatAllocation(tk.Frame):
    def __init__(self, master, state):
        super().__init__(master)
        self.master = master
        self.state = state

        self.method_var = tk.StringVar(value="array")
        self.assign_vars = {ability: tk.StringVar() for ability in ABILITIES}
        self.method_var.set("array")

        tk.Label(self, text="Wybierz metodę rozdzielania statystyk", font=("Arial", 16)).pack(pady=10)

        tk.Radiobutton(self, text="Standardowa pula (15, 14, 13, ...)", variable=self.method_var, value="array", command=self.show_method).pack(anchor="w")
        tk.Radiobutton(self, text="Rzut kośćmi (wpisz ręcznie)", variable=self.method_var, value="manual", command=self.show_method).pack(anchor="w")

        self.method_frame = tk.Frame(self)
        self.method_frame.pack(pady=10)

        self.show_method()

        # Navigation
        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text="Wstecz", command=self.master.previous_step).pack(side="left", padx=10)
        tk.Button(nav, text="Dalej", command=self.save_and_continue).pack(side="right", padx=10)

    def show_method(self):
        for widget in self.method_frame.winfo_children():
            widget.destroy()

        method = self.method_var.get()

        if method == "array":
            tk.Label(self.method_frame, text="Przypisz każdą wartość do cechy (każda wartość tylko raz)").pack()

            self.array_menus = {}

            def update_dropdowns(*args):
                selected_values = [var.get() for var in self.assign_vars.values() if var.get()]
                for ability, menu in self.array_menus.items():
                    current_val = self.assign_vars[ability].get()
                    menu['menu'].delete(0, 'end')
                    for val in STANDARD_ARRAY:
                        state = "normal" if (val not in selected_values or str(val) == current_val) else "disabled"
                        menu['menu'].add_command(
                            label=val,
                            command=lambda v=val, a=ability: self.assign_vars[a].set(str(v))
                        )

            for ability in ABILITIES:
                row = tk.Frame(self.method_frame)
                row.pack(pady=2)
                tk.Label(row, text=ability.capitalize() + ":").pack(side="left", padx=5)
                var = self.assign_vars[ability]
                var.trace_add("write", update_dropdowns)
                dropdown = tk.OptionMenu(row, var, *STANDARD_ARRAY)
                dropdown.pack(side="left")
                self.array_menus[ability] = dropdown

            update_dropdowns()  # Initial call

        elif method == "manual":
            tk.Label(self.method_frame, text="Wprowadź wyniki rzutów (3k6 lub 4k6 drop lowest)").pack()
            for ability in ABILITIES:
                row = tk.Frame(self.method_frame)
                row.pack(pady=2)
                tk.Label(row, text=ability.capitalize() + ":").pack(side="left", padx=5)
                entry = tk.Entry(row, textvariable=self.assign_vars[ability])
                entry.pack(side="left")

    def save_and_continue(self):
        stats = {}
        method = self.method_var.get()

        try:
            for ability in ABILITIES:
                val = int(self.assign_vars[ability].get())
                if val < 1 or val > 20:
                    raise ValueError
                stats[ability] = val
        except ValueError:
            messagebox.showerror("Błąd", "Upewnij się, że wszystkie wartości są liczbami całkowitymi między 1 a 20.")
            return
        if method == "array":
            values = list(stats.values())
            if sorted(values) != sorted(STANDARD_ARRAY):
                messagebox.showerror("Błąd", "Musisz przypisać każdą wartość tylko raz.")
                return

        self.state.set("stat_method", method)
        self.state.set("stats", stats)
        self.master.next_step()
