import tkinter as tk
import utils.language_helper as lh
from .has_steps import HasSteps


class StepBackground(tk.Frame):
    def __init__(self, master, state, wizard : HasSteps):
        super().__init__(master)
        self.state = state
        self.wizard = wizard

        self.bg_var = tk.StringVar()
        self.background_options = {bg["id"]: bg for bg in lh.backgrounds}
        self.bg_var.set("acolyte")

        tk.Label(self, text=lh.getInfo("choose_character_background"), font=("Arial", 16)).pack(pady=10)
        for bg in self.background_options.values():
            name = lh.getFromDict(bg["name"])
            tk.Radiobutton(self, text=name, variable=self.bg_var, value=bg["id"]).pack()

        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text=lh.getInfo("button_back"), command=self.wizard.previous_step).pack(side="left", padx=10)
        tk.Button(nav, text=lh.getInfo("button_continue"), command=lambda: self.save_and_continue()).pack(side="right", padx=10)  # Explicit call

    def save_and_continue(self):
        bg_id = self.bg_var.get()
        self.state.set("background", {"id": bg_id})
        print(f"Saved Background: {self.state.get('background')}")  # Debug
        self.wizard.next_step()