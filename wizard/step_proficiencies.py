import tkinter as tk
from PIL import Image, ImageTk
import os
import utils.language_helper as lh
from .has_steps import HasSteps
from .is_step import IsStep

class StepProficiencies(IsStep):
    def __init__(self, master, state, wizard: HasSteps):
        super().__init__(master, wizard)
        self.state = state

        # Load parchment background
        image_path = os.path.join("assets", "parchment.png")
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(pil_image)
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Configure fantasy font
        self.fantasy_font = ("Chomsky", 16)

        # Navigation frame on the left
        self.nav_frame = tk.Frame(self, bg="#d2b48c", padx=10, pady=10, bd=2, relief="raised")
        self.nav_frame.place(x=10, y=10, height=580, width=200)

        # Load data
        self.proficiencies = lh.proficiencies
        self.classes = {cls["id"]: cls for cls in lh.classes}
        self.backgrounds = {bg["id"]: bg for bg in lh.backgrounds}
        self.races = {race["id"]: race for race in lh.races}

        # Get current selections
        class_data = self.state.get("class") or {}
        self.current_class = class_data.get("id") if isinstance(class_data, dict) else None
        background_data = self.state.get("background") or {}
        self.current_background = background_data.get("id") if isinstance(background_data, dict) else None
        race_data = self.state.get("race") or {}
        self.current_race = race_data.get("id") if isinstance(race_data, dict) else None

        # Determine proficiencies
        self.default_profs, self.available_choices = self.get_proficiencies()

        # Create scrollable canvas for content
        self.canvas = tk.Canvas(self, bg="#d2b48c", highlightthickness=0)
        self.canvas.place(x=220, y=10, width=560, height=580)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.place(x=760, y=10, height=580)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Scrollable frame
        self.scrollable_frame = tk.Frame(self.canvas, bg="#d2b48c")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Default proficiencies display
        tk.Label(self.scrollable_frame, text=lh.getInfo("default_skills"), font=("Chomsky", 24), bg="#d2b48c").pack(anchor="w", pady=10)
        default_frame = tk.Frame(self.scrollable_frame, bg="#d2b48c")
        default_frame.pack(anchor="w", pady=5)
        for prof_id in self.default_profs:
            prof = next(p for p in self.proficiencies if p["id"] == prof_id)
            tk.Label(default_frame, text=lh.getFromDict(prof["name"]), font=self.fantasy_font,
                    bg="#d2b48c", fg="gray").pack(anchor="w", pady=5)

        # Skill selection
        tk.Label(self.scrollable_frame, text=lh.getInfo("choose_skills"), font=("Chomsky", 24), bg="#d2b48c").pack(anchor="w", pady=10)
        self.skill_frame = tk.Frame(self.scrollable_frame, bg="#d2b48c")
        self.skill_frame.pack(anchor="w", pady=5)
        self.skill_vars = {prof["id"]: tk.BooleanVar() for prof in self.available_choices}
        if not self.available_choices:
            tk.Label(self.skill_frame, text=lh.getInfo("no_skills_to_choose"), font=self.fantasy_font,
                    bg="#d2b48c").pack(anchor="w", pady=5)
        else:
            self.update_skill_checkboxes()

        # Update scroll region
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Navigation buttons
        tk.Button(self.nav_frame, text=lh.getInfo("button_back"), font=self.fantasy_font, bg="#8b4513",
                 fg="white", padx=10, pady=5, bd=2, command=self.discard_and_back).pack(fill="x", pady=5)
        tk.Button(self.nav_frame, text=lh.getInfo("button_continue"), font=self.fantasy_font, bg="#8b4513",
                 fg="white", padx=10, pady=5, bd=2, command=self.save_and_continue).pack(fill="x", pady=5)

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

        # Available choices: all skills minus default
        all_skills = [prof["id"] for prof in self.proficiencies if prof["type"] == "skill"]
        available_choices = [prof for prof in self.proficiencies if prof["type"] == "skill" and prof["id"] not in default_profs]
        return list(default_profs), available_choices

    def update_skill_checkboxes(self):
        for widget in self.skill_frame.winfo_children():
            widget.destroy()
        selected_count = sum(var.get() for var in self.skill_vars.values())
        for prof in self.available_choices:
            cb = tk.Checkbutton(self.skill_frame, text=lh.getFromDict(prof["name"]), variable=self.skill_vars[prof["id"]],
                               font=self.fantasy_font, bg="#d2b48c",
                               command=lambda p=prof["id"]: self.validate_selection(p))
            cb.pack(anchor="w", pady=5)
        self.validate_selection()

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
            tk.messagebox.showerror(lh.getInfo("error"), lh.getInfo("error_too_many_skills_chosen"))
            return
        current_profs = self.state.get("proficiencies", [])
        all_profs = list(set(current_profs + list(self.default_profs) + selected_profs))
        self.state.set("proficiencies", all_profs)
        super().save_and_continue()