import tkinter as tk
import utils.language_helper as lh

class StepEquipment(tk.Frame):
    def __init__(self, master, state):
        super().__init__(master)
        self.master = master
        self.state = state

        # Load class and background data
        self.classes = {cls["id"]: cls for cls in lh.classes}
        self.backgrounds = {bg["id"]: bg for bg in lh.backgrounds}
        class_data = self.state.get("class", {})
        background_data = self.state.get("background", {})
        self.current_class = class_data.get("id") if isinstance(class_data, dict) else None
        self.current_background = background_data.get("id") if isinstance(background_data, dict) else None

        if not self.current_class or self.current_class not in self.classes:
            tk.Label(self, text=lh.getInfo("error_class_not_chosen")).pack(pady=10)
            return

        self.equipment_options = lh.getFromDict(self.classes[self.current_class]["starting_equipment_options"])
        self.selected_options = [tk.StringVar(value=options[0]) for options in self.equipment_options]  # Pre-select first option
        self.background_equipment = lh.getFromDict(self.backgrounds.get(self.current_background, {}).get("equipment", {"en": []})) if self.current_background else []

        # UI Elements
        tk.Label(self, text=lh.getInfo("background_equipment"), font=("Arial", 14)).pack(pady=5)
        if self.background_equipment:
            for item in self.background_equipment:
                tk.Label(self, text=item, fg="gray").pack(anchor="w")
        else:
            tk.Label(self, text=lh.getInfo("background_equipment_missing"), fg="gray").pack(anchor="w")

        tk.Label(self, text=lh.getInfo("choose_equipment_for_class") + " " + lh.getFromDict(self.classes[self.current_class]['name']), font=("Arial", 16)).pack(pady=10)

        for i, options in enumerate(self.equipment_options):
            frame = tk.Frame(self)
            frame.pack(pady=5)
            tk.Label(frame, text=lh.getInfo("choose_option") + " " + str(i + 1) + ":").pack(side="left")
            var = self.selected_options[i]
            for option in options:
                tk.Radiobutton(frame, text=option, variable=var, value=option).pack(side="left", padx=5)

        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text=lh.getInfo("button_back"), command=self.master.previous_step).pack(side="left", padx=10)
        tk.Button(nav, text=lh.getInfo("button_continue"), command=self.save_and_continue).pack(side="right", padx=10)

    def save_and_continue(self):
        selected_equipment = [var.get() for var in self.selected_options]
        if any(not option for option in selected_equipment):
            tk.messagebox.showerror(lh.getInfo("error"), lh.getInfo("error_not_all_options_selected"))
            return
        all_equipment = self.background_equipment + selected_equipment
        self.state.set("equipment", all_equipment)
        self.master.next_step()