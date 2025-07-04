import tkinter as tk
import utils.language_helper as lh
import utils.loaded_data as ld
from state.character_state import CharacterState
from .has_steps import HasSteps
from .is_step import IsStep


class StepEquipment(IsStep):
    def __init__(self, master, state : CharacterState, wizard : HasSteps):
        super().__init__(master, wizard)
        self.state = state

        # Load class and background data
        self.classes = {cls["id"]: cls for cls in ld.classes}
        self.backgrounds = {bg["id"]: bg for bg in ld.backgrounds}
        class_data = self.state.get("class", {})
        background_data = self.state.get("background", {})
        self.current_class = class_data.get("id") if isinstance(class_data, dict) else None
        self.current_background = background_data.get("id") if isinstance(background_data, dict) else None

        if not self.current_class or self.current_class not in self.classes:
            tk.Label(self, text=lh.getInfo("error_class_not_chosen")).pack(pady=10)
            return

        self.equipment_options = self.classes[self.current_class]["starting_equipment_options"]
        self.selected_options = [tk.IntVar(value=0) for options in self.equipment_options]  # Pre-select first option
        self.background_equipment = self.backgrounds.get(self.current_background, {}).get("equipment", []) if self.current_background else []

        # UI Elements
        tk.Label(self, text=lh.getInfo("background_equipment"), font=("Arial", 14)).pack(pady=5)
        if self.background_equipment:
            for item in self.background_equipment:
                tk.Label(self, text=lh.getItemCountAndName(item), fg="gray").pack()
        else:
            tk.Label(self, text=lh.getInfo("background_equipment_missing"), fg="gray").pack()

        tk.Label(self, text=lh.getInfo("choose_equipment_for_class") + " " + lh.getClassName(self.current_class), font=("Arial", 16)).pack(pady=10)

        for i, options in enumerate(self.equipment_options):
            frame = tk.Frame(self)
            frame.pack(pady=5)
            tk.Label(frame, text=lh.getInfo("choose_option") + " " + str(i + 1) + ":").pack(side="left")
            var = self.selected_options[i]
            for j, option in enumerate(options):
                text : str = ""
                bl = True
                for x in option:
                    if(not (x in self.state.get("equipment"))):
                        bl = False
                    if(len(text) < 1):
                        text += lh.getItemCountAndName(x)
                    else:
                        text += ", " + lh.getItemCountAndName(x)
                if(bl):
                    var.set(j)
                tk.Radiobutton(frame, text=text, variable=var, value=j).pack(side="left", padx=5)

        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text=lh.getInfo("button_back"), command=self.discard_and_back).pack(side="left", padx=10)
        tk.Button(nav, text=lh.getInfo("button_continue"), command=self.save_and_continue).pack(side="right", padx=10)

    def save_and_continue(self):
        # The commented code doesn't work anymore, but there is no need to fix it, because radio buttons
        # cannot be deselected, so there is no need to check if an option was not selected

        #selected_equipment = [var.get() for var in self.selected_options]
        #if any(not option for option in selected_equipment):
        #    tk.messagebox.showerror(lh.getInfo("error"), lh.getInfo("error_not_all_options_selected"))
        #    return

        all_equipment = self.background_equipment.copy()
        for i, option in enumerate(self.equipment_options):
            for item in option[self.selected_options[i].get()]:
                all_equipment.append(item)
        self.state.set("equipment", all_equipment)
        print("Character equipment:")
        print(all_equipment)
        super().save_and_continue()