import tkinter as tk
import tkinter.messagebox
import utils.language_helper as lh
import utils.loaded_data as ld
from state.character_state import CharacterState
from .has_steps import HasSteps
from .is_step import IsStep
import os
from PIL import Image, ImageTk

class StepSpellSelection(IsStep):
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

        # Load spell data
        self.spells = ld.spells

        # Get class and stats from state
        class_data = self.state.get("class") or {}
        self.current_class = class_data.get("id") if isinstance(class_data, dict) else None
        stats = self.state.get("stats", {})

        # Determine max spells for level 1 Wizard
        self.max_cantrips = 3 if self.current_class == "wizard" else self.get_max_cantrips(stats)
        self.max_level_1 = 2 if self.current_class == "wizard" else self.get_max_spells(stats, 1)
        self.selected_cantrips = []
        self.selected_level_1 = []

        # Debug print
        print(f"Debug - StepSpellSelection Init:")
        print(f"  Class: {self.current_class}")
        print(f"  Max Cantrips: {self.max_cantrips}")
        print(f"  Max Level 1 Spells: {self.max_level_1}")
        print(f"  State content: {self.state.data}")

        # UI Elements on canvas
        info = lh.getInfo("choose_spells")
        info = info.replace(";", f"{self.max_cantrips}", 1)
        info = info.replace(";", f"{self.max_level_1}", 1)
        tk.Label(self.canvas, text=info, font=self.fantasy_font, bg="#d2b48c").pack(pady=10)
        self.cantrip_vars = {}
        self.level_1_vars = {}
        self.cantrip_frame = tk.Frame(self.canvas, bg="#d2b48c")
        self.level_1_frame = tk.Frame(self.canvas, bg="#d2b48c")
        self.cantrip_frame.pack()
        self.level_1_frame.pack()

        # Filter spells by class and level
        cantrips = [s for s in self.spells if s["level"] == 0 and self.current_class in s["classes"]]
        level_1_spells = [s for s in self.spells if s["level"] == 1 and self.current_class in s["classes"]]
        for spell in cantrips:
            var = tk.BooleanVar()
            self.cantrip_vars[spell["id"]] = var
            cb = tk.Checkbutton(self.cantrip_frame, text=f"{lh.getSpellName(spell['id'])} ({lh.getInfo('level')} 0)", variable=var,
                              font=self.fantasy_font, bg="#d2b48c", activebackground="#d2b48c", selectcolor="#8b4513",
                              command=lambda s=spell["id"]: self.validate_selection(s, "cantrip"))
            cb.pack(anchor="w")
        for spell in level_1_spells:
            var = tk.BooleanVar()
            self.level_1_vars[spell["id"]] = var
            cb = tk.Checkbutton(self.level_1_frame, text=f"{lh.getSpellName(spell['id'])} ({lh.getInfo('level')} 1)", variable=var,
                              font=self.fantasy_font, bg="#d2b48c", activebackground="#d2b48c", selectcolor="#8b4513",
                              command=lambda s=spell["id"]: self.validate_selection(s, "level_1"))
            cb.pack(anchor="w")

        for spell in self.state.get("spells", []):
            if(spell in self.cantrip_vars.keys()):
                self.cantrip_vars[spell].set(True)
            elif(spell in self.level_1_vars.keys()):
                self.level_1_vars[spell].set(True)
            else:
                print("Character has unknown spell: " + spell)

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

    def get_max_cantrips(self, stats):
        return 3  # Default for level 1, adjust based on class progression later

    def get_max_spells(self, stats, level):
        return 2 if level == 1 else 0  # Default for level 1 Wizard, adjust later

    def validate_selection(self, spell_name, spell_type):
        if spell_type == "cantrip":
            selected = [name for name, var in self.cantrip_vars.items() if var.get()]
            if len(selected) > self.max_cantrips:
                for name in selected[self.max_cantrips:]:
                    self.cantrip_vars[name].set(False)
        elif spell_type == "level_1":
            selected = [name for name, var in self.level_1_vars.items() if var.get()]
            if len(selected) > self.max_level_1:
                for name in selected[self.max_level_1:]:
                    self.level_1_vars[name].set(False)

    def save_and_continue(self):
        selected_cantrips = [name for name, var in self.cantrip_vars.items() if var.get()]
        selected_level_1 = [name for name, var in self.level_1_vars.items() if var.get()]
        if len(selected_cantrips) != self.max_cantrips:
            info = lh.getInfo("error_wrong_cantrip_amount")
            info = info.replace(";", f"{self.max_cantrips}")
            tk.messagebox.showerror(lh.getInfo("error"), info)
            return
        if len(selected_level_1) != self.max_level_1:
            info = lh.getInfo("error_wrong_spell_amount")
            info = info.replace(";", f"{self.max_level_1}")
            tk.messagebox.showerror(lh.getInfo("error"), info)
            return
        self.state.set("spells", selected_cantrips + selected_level_1)
        print("Selected spells:")
        print(self.state.get("spells"))
        super().save_and_continue()