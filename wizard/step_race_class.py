import tkinter as tk
import utils.language_helper as lh
import utils.loaded_data as ld
from state.character_state import CharacterState
from .has_steps import HasSteps
from .is_step import IsStep
import os  # Added missing import
from PIL import Image, ImageTk

class StepRaceClass(IsStep):
    def __init__(self, master, state: CharacterState, wizard: HasSteps):
        super().__init__(master, wizard)
        self.state = state

        # Load and set up dynamic parchment background with Canvas
        self.canvas = tk.Canvas(self, bg="#d2b48c")
        self.canvas.pack(fill="both", expand=True)
        image_path = os.path.join("assets", "parchment.png")
        self.pil_image = Image.open(image_path)
        self.update_background()
        self.master.bind("<Configure>", lambda e: self.update_background())

        # Configure fantasy font
        self.fantasy_font = ("Chomsky", 16)

        # Load data
        self.race_options = {race["id"]: race for race in ld.races}
        self.class_options = {cls["id"]: cls for cls in ld.classes}

        self.race_var = tk.StringVar()
        self.class_var = tk.StringVar()
        if self.state.get("race") is not None and self.state.get("race").get("id") in self.race_options.keys():
            self.race_var.set(self.state.get("race").get("id"))
        else:
            self.race_var.set("human")

        if self.state.get("class") is not None and self.state.get("class").get("id") in self.class_options.keys():
            self.class_var.set(self.state.get("class").get("id"))
        else:
            self.class_var.set("fighter")

        tk.Label(self, text=lh.getInfo("choose_race"), font=(self.fantasy_font[0], 24), bg="#d2b48c").place(x=10, y=10)
        for i, race in enumerate(self.race_options.values()):
            name = lh.getRaceName(race["id"])
            tk.Radiobutton(self, text=name, variable=self.race_var, value=race["id"], font=self.fantasy_font, bg="#d2b48c",
                           activebackground="#d2b48c", selectcolor="#8b4513").place(x=10, y=50 + i * 30)

        tk.Label(self, text=lh.getInfo("choose_class"), font=(self.fantasy_font[0], 24), bg="#d2b48c").place(x=10, y=150)
        for i, cls in enumerate(self.class_options.values()):
            name = lh.getClassName(cls["id"])
            tk.Radiobutton(self, text=name, variable=self.class_var, value=cls["id"], font=self.fantasy_font, bg="#d2b48c",
                           activebackground="#d2b48c", selectcolor="#8b4513").place(x=10, y=190 + i * 30)

        nav = tk.Frame(self, bg="#d2b48c")
        nav.place(x=10, y=350)
        tk.Button(nav, text=lh.getInfo("button_back"), font=self.fantasy_font, bg="#8b4513", fg="white", padx=10, pady=5, bd=2,
                  command=self.discard_and_back).pack(side="left", padx=10)
        tk.Button(nav, text=lh.getInfo("button_continue"), font=self.fantasy_font, bg="#8b4513", fg="white", padx=10, pady=5, bd=2,
                  command=self.save_and_continue).pack(side="right", padx=10)

    def update_background(self):
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        if width <= 0 or height <= 0:
            return
        resized_image = self.pil_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

    def save_and_continue(self):
        race_id = self.race_var.get()
        class_id = self.class_var.get()
        self.state.set("race", {"id": race_id})
        self.state.set("class", {"id": class_id})
        print(f"Saved Race: {self.state.get('race')}, Class: {self.state.get('class')}")  # Debug
        super().save_and_continue()