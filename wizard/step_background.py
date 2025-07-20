import tkinter as tk
import utils.language_helper as lh
import utils.loaded_data as ld
from state.character_state import CharacterState
from .has_steps import HasSteps
from .is_step import IsStep
import os  # Added missing import
from PIL import Image, ImageTk

class StepBackground(IsStep):
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

        self.bg_var = tk.StringVar()
        self.background_options = {bg["id"]: bg for bg in ld.backgrounds}

        if self.state.get("background") is not None and self.state.get("background").get("id") in self.background_options.keys():
            self.bg_var.set(self.state.get("background").get("id"))
        else:
            self.bg_var.set("acolyte")

        tk.Label(self, text=lh.getInfo("choose_character_background"), font=(self.fantasy_font[0], 24), bg="#d2b48c").place(x=10, y=10)
        for i, bg in enumerate(self.background_options.values()):
            name = lh.getBackgroundName(bg["id"])
            tk.Radiobutton(self, text=name, variable=self.bg_var, value=bg["id"], font=self.fantasy_font, bg="#d2b48c",
                           activebackground="#d2b48c", selectcolor="#8b4513").place(x=10, y=50 + i * 30)

        nav = tk.Frame(self, bg="#d2b48c")
        nav.place(x=10, y=150)
        tk.Button(nav, text=lh.getInfo("button_back"), font=self.fantasy_font, bg="#8b4513", fg="white", padx=10, pady=5, bd=2,
                  command=self.discard_and_back).pack(side="left", padx=10)
        tk.Button(nav, text=lh.getInfo("button_continue"), font=self.fantasy_font, bg="#8b4513", fg="white", padx=10, pady=5, bd=2,
                  command=lambda: self.save_and_continue()).pack(side="right", padx=10)

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
        bg_id = self.bg_var.get()
        self.state.set("background", {"id": bg_id})
        print(f"Saved Background: {self.state.get('background')}")  # Debug
        super().save_and_continue()