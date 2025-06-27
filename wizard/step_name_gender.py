import tkinter as tk

import menu.start_menu
import utils.language_helper as lh
from tkinter import messagebox

from .has_steps import HasSteps


class StepNameGender(tk.Frame):
    def __init__(self, master, state, wizard : HasSteps):
        super().__init__(master)
        self.state = state
        self.wizard = wizard

        self.quitToMenuVar = tk.BooleanVar()

        tk.Label(self, text=lh.getInfo("choose_character_name"), font=("Arial", 16)).pack(pady=10)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text=lh.getInfo("choose_character_gender"), font=("Arial", 16)).pack(pady=10)
        self.gender_var = tk.StringVar(value=lh.getGenders()[-1])
        for g in lh.getGenders():
            tk.Radiobutton(self, text=g, variable=self.gender_var, value=g).pack()

        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text=lh.getInfo("main_menu"), command=self.backToMenu).pack(side="left", padx=10)
        tk.Button(nav, text=lh.getInfo("button_continue"), command=self.save_and_continue).pack(side="left", padx=10)

    def save_and_continue(self):
        name = self.name_entry.get().strip()
        if name == "":
            messagebox.showerror(lh.getInfo("error"), lh.getInfo("error_character_name_wrong"))
            return
        
        self.state.set("name", name)
        self.state.set("gender", self.gender_var.get())
        self.wizard.next_step()

    def backToMenu(self):
        result = messagebox.askquestion(lh.getInfo("warning"), lh.getInfo("u_sure"))

        if(result == 'yes' or result == True):
            app = menu.start_menu.StartMenu(self.master)
            self.destroy()
            app.pack(side="top", expand=True, fill="both")