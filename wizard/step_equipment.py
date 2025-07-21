import tkinter as tk
import tkinter.messagebox
import utils.language_helper as lh
import utils.loaded_data as ld
from state.character_state import CharacterState
from .has_steps import HasSteps
from .is_step import IsStep
import os
from PIL import Image, ImageTk

class StepEquipment(IsStep):
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
        self.small_font = ("Chomsky", 14)

        # Load class and background data
        self.classes = {cls["id"]: cls for cls in ld.classes}
        self.backgrounds = {bg["id"]: bg for bg in ld.backgrounds}
        class_data = self.state.get("class", {})
        background_data = self.state.get("background", {})
        self.current_class = class_data.get("id") if isinstance(class_data, dict) else None
        self.current_background = background_data.get("id") if isinstance(background_data, dict) else None

        if not self.current_class or self.current_class not in self.classes:
            tk.Label(self.canvas, text=lh.getInfo("error_class_not_chosen"), font=self.small_font, bg="#d2b48c").pack(pady=10)
            return

        self.equipment_options = self.classes[self.current_class]["starting_equipment_options"]
        self.selected_options = [tk.IntVar(value=0) for options in self.equipment_options]  # Pre-select first option
        self.background_equipment = self.backgrounds.get(self.current_background, {}).get("equipment", []) if self.current_background else []

        # UI Elements on canvas
        tk.Label(self.canvas, text=lh.getInfo("background_equipment"), font=self.small_font, bg="#d2b48c").pack(pady=5)
        if self.background_equipment:
            for item in self.background_equipment:
                tk.Label(self.canvas, text=lh.getItemCountAndName(item), font=self.small_font, fg="#8b4513", bg="#d2b48c").pack()
        else:
            tk.Label(self.canvas, text=lh.getInfo("background_equipment_missing"), font=self.small_font, fg="#8b4513", bg="#d2b48c").pack()

        tk.Label(self.canvas, text=lh.getInfo("choose_equipment_for_class") + " " + lh.getClassName(self.current_class), font=self.fantasy_font, bg="#d2b48c").pack(pady=10)

        for i, options in enumerate(self.equipment_options):
            frame = tk.Frame(self.canvas, bg="#d2b48c")
            frame.pack(pady=5)
            tk.Label(frame, text=lh.getInfo("choose_option") + " " + str(i + 1) + ":", font=self.small_font, bg="#d2b48c").pack(side="left")
            var = self.selected_options[i]
            for j, option in enumerate(options):
                text = ""
                bl = True
                for x in option:
                    if not (x in self.state.get("equipment", [])):
                        bl = False
                    if len(text) < 1:
                        text += lh.getItemCountAndName(x)
                    else:
                        text += ", " + lh.getItemCountAndName(x)
                if bl:
                    var.set(j)
                tk.Radiobutton(frame, text=text, variable=var, value=j, font=self.small_font, bg="#d2b48c", activebackground="#d2b48c", selectcolor="#8b4513").pack(side="left", padx=5)

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

    def save_and_continue(self):
        all_equipment = self.background_equipment.copy()
        for i, option in enumerate(self.equipment_options):
            for item in option[self.selected_options[i].get()]:
                all_equipment.append(item)
        self.state.set("equipment", all_equipment)
        print("Character equipment:")
        print(all_equipment)
        super().save_and_continue()