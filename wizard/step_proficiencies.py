import tkinter as tk
import tkinter.messagebox
import utils.language_helper as lh
import utils.loaded_data as ld
from state.character_state import CharacterState
from .has_steps import HasSteps
from .is_step import IsStep
import os
from PIL import Image, ImageTk

class StepProficiencies(IsStep):
    def __init__(self, master, state: CharacterState, wizard: HasSteps):
        super().__init__(master, wizard)
        self.state = state

        # Load and set up dynamic parchment background with Canvas
        self.canvas = tk.Canvas(self, bg="#d2b48c")
        self.canvas.pack(fill="both", expand=True)
        image_path = os.path.join("assets", "parchment.png")
        self.pil_image = Image.open(image_path)
        self.update_background()
        self.bind("<Configure>", self.update_background)

        # Configure fantasy font
        self.fantasy_font = ("Chomsky", 16)

        # Load data
        self.proficiencies = ld.proficiencies
        self.classes = {cls["id"]: cls for cls in ld.classes}
        self.backgrounds = {bg["id"]: bg for bg in ld.backgrounds}
        self.races = {race["id"]: race for race in ld.races}

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
        print(f"  State content: {self.state.data}")

        # Determine proficiencies
        self.default_profs, self.available_choices = self.get_proficiencies()
        print(f"  Default profs: {self.default_profs}")
        print(f"  Available choices: {self.available_choices}")

        # UI Elements on canvas
        tk.Label(self.canvas, text=lh.getInfo("default_skills"), font=(self.fantasy_font[0], 16), bg="#d2b48c").pack(pady=10)
        default_frame = tk.Frame(self.canvas, bg="#d2b48c")
        default_frame.pack()
        for prof_id in self.default_profs:
            prof = next(p for p in self.proficiencies if p["id"] == prof_id)
            tk.Label(default_frame, text=lh.getProficiency(prof["id"]), font=self.fantasy_font, fg="#8b4513", bg="#d2b48c").pack(anchor="w")

        tk.Label(self.canvas, text=lh.getInfo("choose_skills"), font=(self.fantasy_font[0], 16), bg="#d2b48c").pack(pady=10)
        self.skill_vars = {prof["id"]: tk.BooleanVar() for prof in self.available_choices}
        self.skill_frame = tk.Frame(self.canvas, bg="#d2b48c")
        self.skill_frame.pack()

        if not self.available_choices:
            tk.Label(self.skill_frame, text=lh.getInfo("no_skills_to_choose"), font=self.fantasy_font, bg="#d2b48c").pack()
        else:
            self.update_skill_checkboxes()

        # Navigation
        self.nav = tk.Frame(self.canvas, bg="#d2b48c")
        self.nav.pack(side="bottom", pady=20)
        tk.Button(self.nav, text=lh.getInfo("button_back"), font=self.fantasy_font, bg="#8b4513", fg="white", padx=10, pady=5, bd=2,
                  command=self.discard_and_back).pack(side="left", padx=10)
        tk.Button(self.nav, text=lh.getInfo("button_continue"), font=self.fantasy_font, bg="#8b4513", fg="white", padx=10, pady=5, bd=2,
                  command=self.save_and_continue).pack(side="right", padx=10)

    def update_background(self, event=None):
        width = self.winfo_width()
        height = self.winfo_height()
        if width <= 0 or height <= 0:
            return
        resized_image = self.pil_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

    def get_proficiencies(self):
        default_profs = set()
        available_choices = []

        # Class proficiencies
        if self.current_class and self.current_class in self.classes:
            default_profs.update(self.classes[self.current_class].get("skill_proficiencies", []))

        # Background proficiencies
        if self.current_background and self.current_background in self.backgrounds:
            default_profs.update(self.backgrounds[self.current_background].get("skill_proficiencies", []))

        # Race proficiencies
        if self.current_race and self.current_race in self.races and "traits" in self.races[self.current_race]:
            for trait in self.races[self.current_race]["traits"]:
                if "description" in trait and isinstance(trait["description"], dict):
                    desc_pl = trait["description"].get("pl", "").lower()
                    if "biegłość" in desc_pl and "percepcja" in desc_pl:
                        default_profs.add("perception")

        # Available choices: all skills minus default, no arbitrary limit
        all_skills = [prof["id"] for prof in self.proficiencies if prof["type"] == "skill"]
        available_choices = [prof for prof in self.proficiencies if prof["type"] == "skill" and prof["id"] not in default_profs]
        return list(default_profs), available_choices

    def update_skill_checkboxes(self):
        for widget in self.skill_frame.winfo_children():
            widget.destroy()
        selected_count = sum(var.get() for var in self.skill_vars.values())
        if not self.available_choices:
            tk.Label(self.skill_frame, text=lh.getInfo("no_skills_to_choose"), font=self.fantasy_font, bg="#d2b48c").pack()
        else:
            num_choices = len(self.available_choices)
            num_columns = 3
            num_rows = (num_choices + num_columns - 1) // num_columns  # Ceiling division
            for i, prof in enumerate(self.available_choices):
                row = i // num_columns
                col = i % num_columns
                cb = tk.Checkbutton(self.skill_frame, text=lh.getProficiency(prof["id"]), variable=self.skill_vars[prof["id"]],
                                    font=self.fantasy_font, bg="#d2b48c", activebackground="#d2b48c", selectcolor="#8b4513",
                                    command=lambda p=prof["id"]: self.validate_selection(p))
                cb.grid(row=row, column=col, padx=5, pady=2, sticky="w")
            self.validate_selection()  # Initial validation
            for id in self.skill_vars.keys():
                if (id in self.state.get("proficiencies", [])):
                    self.skill_vars.get(id).set(True)
                    self.state.get("proficiencies").remove(id)

    def validate_selection(self, changed=None):
        selected = [prof for prof, var in self.skill_vars.items() if var.get()]
        if len(selected) > 3:
            for prof in selected[3:]:
                self.skill_vars[prof].set(False)
        for var in self.skill_vars.values():
            var.set(False) if len(selected) >= 3 and changed not in selected else None

    def save_and_continue(self):
        selected_profs = [prof for prof, var in self.skill_vars.items() if var.get()]
        if len(selected_profs) > 3:
            tkinter.messagebox.showerror(lh.getInfo("error"), lh.getInfo("error_too_many_skills_chosen"))
            return

        current_profs = self.state.get("proficiencies", [])
        all_profs = list(set(current_profs + list(self.default_profs) + selected_profs))
        self.state.set("proficiencies", all_profs)
        super().save_and_continue()

    def destroy(self):
        self.unbind("<Configure>")
        super().destroy()