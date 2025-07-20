import tkinter as tk
from PIL import Image, ImageTk
import os
import utils.language_helper as lh
from .has_steps import HasSteps
from .is_step import IsStep

class StepRaceClass(IsStep):
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
        self.race_options = {race["id"]: race for race in lh.races}
        self.class_options = {cls["id"]: cls for cls in lh.classes}
        self.race_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.race_var.set("human")
        self.class_var.set("fighter")

        # Race selection
        tk.Label(self, text=lh.getInfo("choose_race"), font=("Chomsky", 24), bg="#d2b48c").place(x=220, y=10)
        race_frame = tk.Frame(self, bg="#d2b48c")
        race_frame.place(x=220, y=50)
        for race in self.race_options.values():
            name = lh.getFromDict(race["name"])
            tk.Radiobutton(race_frame, text=name, variable=self.race_var, value=race["id"],
                          font=self.fantasy_font, bg="#d2b48c").pack(anchor="w", pady=5)

        # Class selection
        tk.Label(self, text=lh.getInfo("choose_class"), font=("Chomsky", 24), bg="#d2b48c").place(x=220, y=200)
        class_frame = tk.Frame(self, bg="#d2b48c")
        class_frame.place(x=220, y=240)
        for cls in self.class_options.values():
            name = lh.getFromDict(cls["name"])
            tk.Radiobutton(class_frame, text=name, variable=self.class_var, value=cls["id"],
                          font=self.fantasy_font, bg="#d2b48c").pack(anchor="w", pady=5)

        # Navigation buttons
        tk.Button(self.nav_frame, text=lh.getInfo("button_back"), font=self.fantasy_font, bg="#8b4513",
                 fg="white", padx=10, pady=5, bd=2, command=self.discard_and_back).pack(fill="x", pady=5)
        tk.Button(self.nav_frame, text=lh.getInfo("button_continue"), font=self.fantasy_font, bg="#8b4513",
                 fg="white", padx=10, pady=5, bd=2, command=self.save_and_continue).pack(fill="x", pady=5)

    def save_and_continue(self):
        race_id = self.race_var.get()
        class_id = self.class_var.get()
        self.state.set("race", {"id": race_id})
        self.state.set("class", {"id": class_id})
        print(f"Saved Race: {self.state.get('race')}, Class: {self.state.get('class')}")
        super().save_and_continue()