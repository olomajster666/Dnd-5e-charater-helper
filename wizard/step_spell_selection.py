import tkinter as tk
from PIL import Image, ImageTk
import os
import utils.language_helper as lh
from .has_steps import HasSteps
from .is_step import IsStep
from tkinter import messagebox

class StepSpellSelection(IsStep):
    def __init__(self, master, state, wizard: HasSteps):
        super().__init__(master, wizard)
        self.state = state
        self.max_cantrips = 3  # Static limit for level 0 spells
        self.max_level1 = 2    # Static limit for level 1 spells

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

        # Create scrollable canvas for content
        self.canvas = tk.Canvas(self, bg="#d2b48c", highlightthickness=0)
        self.canvas.place(x=220, y=10, width=560, height=580)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.place(x=760, y=10, height=580)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Scrollable frame
        self.scrollable_frame = tk.Frame(self.canvas, bg="#d2b48c")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Main title with selection limits
        tk.Label(self.scrollable_frame, text="Wybierz zaklęcia (3 poziomu 0 i 2 poziomu 1)", font=("Chomsky", 24), bg="#d2b48c").pack(anchor="w", pady=10)

        # Load data
        self.spells = lh.spells
        class_data = self.state.get("class") or {}
        self.current_class = class_data.get("id") if isinstance(class_data, dict) else None
        self.spell_vars = {}
        self.spell_levels = {}  # Track spell levels for validation

        # Spell selection
        if self.current_class in {"wizard", "cleric", "bard"}:
            available_spells = [
                spell for spell in self.spells
                if spell.get("level", 0) <= 1 and self.current_class in spell.get("classes", [])
            ]
            if not available_spells:
                tk.Label(self.scrollable_frame, text=lh.getInfo("no_spells_available"), font=self.fantasy_font, bg="#d2b48c").pack(anchor="w", pady=5)
            else:
                # Group spells by level
                cantrips = [spell for spell in available_spells if spell.get("level", 0) == 0]
                level1_spells = [spell for spell in available_spells if spell.get("level", 0) == 1]

                # Cantrips (Level 0) header and frame
                if cantrips:
                    tk.Label(self.scrollable_frame, text="Zaklęcia poziomu 0 (3 dostępne)", font=("Chomsky", 18), bg="#d2b48c").pack(anchor="w", pady=5)
                    cantrip_frame = tk.Frame(self.scrollable_frame, bg="#d2b48c")
                    cantrip_frame.pack(anchor="w", pady=5)
                    for spell in cantrips:
                        spell_id = spell.get("id", spell.get("name", {}).get("en", "unknown_spell"))
                        if not spell_id:
                            print(f"Warning: Spell {spell.get('name', 'unknown')} has no valid ID, skipping.")
                            continue
                        self.spell_vars[spell_id] = tk.BooleanVar()
                        self.spell_levels[spell_id] = 0
                        tk.Checkbutton(cantrip_frame, text=lh.getFromDict(spell.get("name", {"en": spell_id})),
                                      variable=self.spell_vars[spell_id], font=self.fantasy_font, bg="#d2b48c",
                                      command=self.validate_selection).pack(anchor="w", pady=5)

                # Level 1 Spells header and frame
                if level1_spells:
                    tk.Label(self.scrollable_frame, text="Zaklęcia poziomu 1 (2 dostępne)", font=("Chomsky", 18), bg="#d2b48c").pack(anchor="w", pady=5)
                    level1_frame = tk.Frame(self.scrollable_frame, bg="#d2b48c")
                    level1_frame.pack(anchor="w", pady=5)
                    for spell in level1_spells:
                        spell_id = spell.get("id", spell.get("name", {}).get("en", "unknown_spell"))
                        if not spell_id:
                            print(f"Warning: Spell {spell.get('name', 'unknown')} has no valid ID, skipping.")
                            continue
                        self.spell_vars[spell_id] = tk.BooleanVar()
                        self.spell_levels[spell_id] = 1
                        tk.Checkbutton(level1_frame, text=lh.getFromDict(spell.get("name", {"en": spell_id})),
                                      variable=self.spell_vars[spell_id], font=self.fantasy_font, bg="#d2b48c",
                                      command=self.validate_selection).pack(anchor="w", pady=5)
        else:
            tk.Label(self.scrollable_frame, text=lh.getInfo("no_spells"), font=self.fantasy_font, bg="#d2b48c").pack(anchor="w", pady=5)

        # Update scroll region
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Navigation buttons
        tk.Button(self.nav_frame, text=lh.getInfo("button_back"), font=self.fantasy_font, bg="#8b4513",
                 fg="white", padx=10, pady=5, bd=2, command=self.discard_and_back).pack(fill="x", pady=5)
        tk.Button(self.nav_frame, text=lh.getInfo("button_continue"), font=self.fantasy_font, bg="#8b4513",
                 fg="white", padx=10, pady=5, bd=2, command=self.save_and_continue).pack(fill="x", pady=5)

    def validate_selection(self):
        selected_cantrips = sum(1 for spell_id, var in self.spell_vars.items() if var.get() and self.spell_levels.get(spell_id, 0) == 0)
        selected_level1 = sum(1 for spell_id, var in self.spell_vars.items() if var.get() and self.spell_levels.get(spell_id, 0) == 1)

        if selected_cantrips > self.max_cantrips:
            for spell_id, var in self.spell_vars.items():
                if var.get() and self.spell_levels.get(spell_id, 0) == 0:
                    var.set(False)
                    selected_cantrips -= 1
                    if selected_cantrips <= self.max_cantrips:
                        break
        if selected_level1 > self.max_level1:
            for spell_id, var in self.spell_vars.items():
                if var.get() and self.spell_levels.get(spell_id, 0) == 1:
                    var.set(False)
                    selected_level1 -= 1
                    if selected_level1 <= self.max_level1:
                        break

    def save_and_continue(self):
        selected_cantrips = sum(1 for spell_id, var in self.spell_vars.items() if var.get() and self.spell_levels.get(spell_id, 0) == 0)
        selected_level1 = sum(1 for spell_id, var in self.spell_vars.items() if var.get() and self.spell_levels.get(spell_id, 0) == 1)
        if selected_cantrips > self.max_cantrips or selected_level1 > self.max_level1:
            messagebox.showerror(lh.getInfo("error"), f"Cannot select more than {self.max_cantrips} cantrips and {self.max_level1} level 1 spells.")
            return
        selected_spells = [spell_id for spell_id, var in self.spell_vars.items() if var.get()]
        self.state.set("spells", selected_spells)
        super().save_and_continue()