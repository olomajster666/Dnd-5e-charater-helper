import tkinter as tk
from tkinter import messagebox

class StepNameGender(tk.Frame):
    def __init__(self, master, state):
        super().__init__(master)
        self.master = master
        self.state = state

        tk.Label(self, text="Imię postaci", font=("Arial", 16)).pack(pady=10)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Płeć postaci", font=("Arial", 16)).pack(pady=10)
        self.gender_var = tk.StringVar(value="Nieokreślona")
        genders = ["Mężczyzna", "Kobieta", "Nieokreślona"]
        for g in genders:
            tk.Radiobutton(self, text=g, variable=self.gender_var, value=g).pack()

        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text="Dalej", command=self.save_and_continue).pack()

    def save_and_continue(self):
        name = self.name_entry.get().strip()
        if name == "":
            messagebox.showerror("Błąd", "Proszę podać imię postaci przed kontynuowaniem.")
            return
        
        self.state.set("name", name)
        self.state.set("gender", self.gender_var.get())
        self.master.next_step()