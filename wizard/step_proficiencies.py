import tkinter as tk
import utils.language_helper as lh
from state.character_state import CharacterState
from .has_steps import HasSteps
from .is_step import IsStep


class StepProficiencies(IsStep):
    def __init__(self, master, state : CharacterState, wizard : HasSteps):
        super().__init__(master, wizard)
        self.state = state

        # Load data
        self.proficiencies = lh.proficiencies
        self.classes = {cls["id"]: cls for cls in lh.classes}
        self.backgrounds = {bg["id"]: bg for bg in lh.backgrounds}
        self.races = {race["id"]: race for race in lh.races}

        # Get current selections with manual fallback
        class_data = self.state.get("class") or {}
        self.current_class = class_data.get("id") if isinstance(class_data, dict) else None
        background_data = self.state.get("background") or {}
        self.current_background = background_data.get("id") if isinstance(background_data, dict) else None
        race_data = self.state.get("race") or {}
        self.current_race = race_data.get("id") if isinstance(race_data, dict) else None

        # Debug print to console
        print(f"Debug - StepProficiencies Init:")
        print(f"  Class: {self.current_class} (Type: {type(self.current_class)})")
        print(f"  Background: {self.current_background} (Type: {type(self.current_background)})")
        print(f"  Race: {self.current_race} (Type: {type(self.current_race)})")
        print(f"  State content: {self.state.data}")  # Full state dump

        # Determine proficiencies
        self.default_profs, self.available_choices = self.get_proficiencies()
        print(f"  Default profs: {self.default_profs}")
        print(f"  Available choices: {self.available_choices}")

        # UI Elements
        tk.Label(self, text=lh.getInfo("default_skills"), font=("Arial", 16)).pack(pady=10)
        default_frame = tk.Frame(self)
        default_frame.pack()
        for prof_id in self.default_profs:
            prof = next(p for p in self.proficiencies if p["id"] == prof_id)
            tk.Label(default_frame, text=lh.getFromDict(prof["name"]), fg="gray").pack(anchor="w")

        tk.Label(self, text=lh.getInfo("choose_skills"), font=("Arial", 16)).pack(pady=10)
        self.skill_vars = {prof["id"]: tk.BooleanVar() for prof in self.available_choices}
        self.skill_frame = tk.Frame(self)
        self.skill_frame.pack()

        if not self.available_choices:
            tk.Label(self.skill_frame, text=lh.getInfo("no_skills_to_choose")).pack()
        else:
            self.update_skill_checkboxes()

        # Navigation
        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text=lh.getInfo("button_back"), command=self.discard_and_back).pack(side="left", padx=10)
        tk.Button(nav, text=lh.getInfo("button_continue"), command=self.save_and_continue).pack(side="right", padx=10)

    def get_proficiencies(self):
        default_profs = set()
        available_choices = []

        # Class proficiencies
        if self.current_class and self.current_class in self.classes:
            default_profs.update(self.classes[self.current_class].get("skill_proficiencies", []))

        # Background proficiencies
        if self.current_background and self.current_background in self.backgrounds:
            default_profs.update(self.backgrounds[self.current_background].get("skill_proficiencies", []))

        # Race proficiencies (e.g., Keen Senses for Elf)
        if self.current_race and self.current_race in self.races and "traits" in self.races[self.current_race]:
            for trait in self.races[self.current_race]["traits"]:
                if "description" in trait and isinstance(trait["description"], dict):
                    desc_pl = trait["description"].get("pl", "").lower()
                    if "biegłość" in desc_pl and "percepcja" in desc_pl:
                        default_profs.add("perception")

        # Available choices: all skills minus default, no arbitrary limit
        all_skills = [prof["id"] for prof in self.proficiencies if prof["type"] == "skill"]
        available_choices = [prof for prof in self.proficiencies if prof["type"] == "skill" and prof["id"] not in default_profs]
        return list(default_profs), available_choices  # Remove the [:4] limit

    def update_skill_checkboxes(self):
        for widget in self.skill_frame.winfo_children():
            widget.destroy()
        selected_count = sum(var.get() for var in self.skill_vars.values())
        for prof in self.available_choices:
            cb = tk.Checkbutton(self.skill_frame, text=lh.getFromDict(prof["name"]), variable=self.skill_vars[prof["id"]],
                              command=lambda p=prof["id"]: self.validate_selection(p))
            cb.pack(anchor="w")
        self.validate_selection()  # Initial validation
        for id in self.skill_vars.keys():
            if (id in self.state.get("proficiencies", [])):
                self.skill_vars.get(id).set(True)
                self.state.get("proficiencies").remove(id)

    def validate_selection(self, changed=None):
        selected = [prof for prof, var in self.skill_vars.items() if var.get()]
        if len(selected) > 3:  # Changed from 2 to 3
            for prof in selected[3:]:
                self.skill_vars[prof].set(False)
        for var in self.skill_vars.values():
            var.set(False) if len(selected) >= 3 and changed not in selected else None  # Changed from 2 to 3

    def save_and_continue(self):
        selected_profs = [prof for prof, var in self.skill_vars.items() if var.get()]
        if len(selected_profs) > 3:  # Changed from 2 to 3
            tk.messagebox.showerror(lh.getInfo("error"), lh.getInfo("error_too_many_skills_chosen"))
            return

        current_profs = self.state.get("proficiencies", [])
        all_profs = list(set(current_profs + list(self.default_profs) + selected_profs))  # Combine default and chosen
        self.state.set("proficiencies", all_profs)
        super().save_and_continue()