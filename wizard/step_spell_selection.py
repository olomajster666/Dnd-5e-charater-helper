import tkinter as tk
import utils.language_helper as lh
from .has_steps import HasSteps


class StepSpellSelection(tk.Frame):
    def __init__(self, master, state, wizard : HasSteps):
        super().__init__(master)
        self.master = master
        self.state = state
        self.wizard = wizard

        # Load spell data
        self.spells = lh.spells

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

        # UI Elements
        info : str = lh.getInfo("choose_spells")
        info = info.replace(";", f"{self.max_cantrips}", 1)
        info = info.replace(";", f"{self.max_level_1}", 1)
        tk.Label(self, text=info, font=("Arial", 16)).pack(pady=10)
        self.cantrip_vars = {}
        self.level_1_vars = {}
        self.cantrip_frame = tk.Frame(self)
        self.level_1_frame = tk.Frame(self)
        self.cantrip_frame.pack()
        self.level_1_frame.pack()

        # Filter spells by class and level
        cantrips = [s for s in self.spells if s["level"] == 0 and self.current_class in s["classes"]]
        level_1_spells = [s for s in self.spells if s["level"] == 1 and self.current_class in s["classes"]]
        for spell in cantrips:
            var = tk.BooleanVar()
            self.cantrip_vars[lh.getFromDict(spell["name"])] = var
            cb = tk.Checkbutton(self.cantrip_frame, text=f"{lh.getFromDict(spell['name'])} ({lh.getInfo('level')} 0)", variable=var,
                              command=lambda s=lh.getFromDict(spell["name"]): self.validate_selection(s, "cantrip"))
            cb.pack(anchor="w")
        for spell in level_1_spells:
            var = tk.BooleanVar()
            self.level_1_vars[lh.getFromDict(spell["name"])] = var
            cb = tk.Checkbutton(self.level_1_frame, text=f"{lh.getFromDict(spell['name'])} ({lh.getInfo('level')} 1)", variable=var,
                              command=lambda s=lh.getFromDict(spell["name"]): self.validate_selection(s, "level_1"))
            cb.pack(anchor="w")

        # Navigation
        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text=lh.getInfo("button_back"), command=self.wizard.previous_step).pack(side="left", padx=10)
        tk.Button(nav, text=lh.getInfo("button_continue"), command=self.save_and_continue).pack(side="right", padx=10)

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
            info : str = lh.getInfo("error_wrong_cantrip_amount")
            info = info.replace(";", f"{self.max_cantrips}")
            tk.messagebox.showerror(lh.getInfo("error"), info)
            return
        if len(selected_level_1) != self.max_level_1:
            info: str = lh.getInfo("error_wrong_spell_amount")
            info = info.replace(";", f"{self.max_level_1}")
            tk.messagebox.showerror(lh.getInfo("error"), info)
            return
        self.state.set("spells", selected_cantrips + selected_level_1)
        self.wizard.next_step()