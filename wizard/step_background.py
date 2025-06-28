import tkinter as tk
import utils.language_helper as lh
import utils.loaded_data as ld
from state.character_state import CharacterState
from .has_steps import HasSteps
from .is_step import IsStep


class StepBackground(IsStep):
    def __init__(self, master, state : CharacterState, wizard : HasSteps):
        super().__init__(master, wizard)
        self.state = state

        self.bg_var = tk.StringVar()
        self.background_options = {bg["id"]: bg for bg in ld.backgrounds}

        if(self.state.get("background") != None and self.state.get("background").get("id") in self.background_options.keys()):
            self.bg_var.set(self.state.get("background").get("id"))
        else:
            self.bg_var.set("acolyte")

        tk.Label(self, text=lh.getInfo("choose_character_background"), font=("Arial", 16)).pack(pady=10)
        for bg in self.background_options.values():
            name = lh.getFromDict(bg["name"])
            tk.Radiobutton(self, text=name, variable=self.bg_var, value=bg["id"]).pack()

        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text=lh.getInfo("button_back"), command=self.discard_and_back).pack(side="left", padx=10)
        tk.Button(nav, text=lh.getInfo("button_continue"), command=lambda: self.save_and_continue()).pack(side="right", padx=10)  # Explicit call

    def save_and_continue(self):
        bg_id = self.bg_var.get()
        self.state.set("background", {"id": bg_id})
        print(f"Saved Background: {self.state.get('background')}")  # Debug
        super().save_and_continue()