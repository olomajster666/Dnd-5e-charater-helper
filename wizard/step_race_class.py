import tkinter as tk
import utils.language_helper as lh
import utils.loaded_data as ld
from state.character_state import CharacterState
from .has_steps import HasSteps
from .is_step import IsStep


class StepRaceClass(IsStep):
    def __init__(self, master, state : CharacterState, wizard : HasSteps):
        super().__init__(master, wizard)
        self.state = state

        # Load data
        self.race_options = {race["id"]: race for race in ld.races}
        self.class_options = {cls["id"]: cls for cls in ld.classes}

        self.race_var = tk.StringVar()
        self.class_var = tk.StringVar()
        if(self.state.get("race") != None and self.state.get("race").get("id") in self.race_options.keys()):
            self.race_var.set(self.state.get("race").get("id"))
        else:
            self.race_var.set("human")

        if(self.state.get("class") != None and self.state.get("class").get("id") in self.class_options.keys()):
            self.class_var.set(self.state.get("class").get("id"))
        else:
            self.class_var.set("fighter")

        tk.Label(self, text=lh.getInfo("choose_race"), font=("Arial", 16)).pack(pady=10)
        for race in self.race_options.values():
            name = lh.getFromDict(race["name"])
            tk.Radiobutton(self, text=name, variable=self.race_var, value=race["id"]).pack()

        tk.Label(self, text=lh.getInfo("choose_class"), font=("Arial", 16)).pack(pady=10)
        for cls in self.class_options.values():
            name = lh.getFromDict(cls["name"])
            tk.Radiobutton(self, text=name, variable=self.class_var, value=cls["id"]).pack()

        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text=lh.getInfo("button_back"), command=self.discard_and_back).pack(side="left", padx=10)
        tk.Button(nav, text=lh.getInfo("button_continue"), command=self.save_and_continue).pack(side="right", padx=10)

    def save_and_continue(self):
        race_id = self.race_var.get()
        class_id = self.class_var.get()
        self.state.set("race", {"id": race_id})
        self.state.set("class", {"id": class_id})
        print(f"Saved Race: {self.state.get('race')}, Class: {self.state.get('class')}")  # Debug
        super().save_and_continue()