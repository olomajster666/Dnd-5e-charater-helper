import tkinter as tk
from PIL import Image, ImageTk
import os
import utils.language_helper as lh
from. import has_steps
from. import is_step

class StepBackground(is_step.IsStep):
    def __init__(self, master, state, wizard: has_steps.HasSteps):
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

        # Title
        tk.Label(self, text=lh.getInfo("choose_character_background"), font=("Chomsky", 24), bg="#d2b48c").place(x=220, y=10)

        # Background selection
        self.bg_var = tk.StringVar()
        self.background_options = {bg["id"]: bg for bg in lh.backgrounds}
        self.bg_var.set("acolyte")

        content_frame = tk.Frame(self, bg="#d2b48c")
        content_frame.place(x=220, y=50)
        for bg in self.background_options.values():
            name = lh.getFromDict(bg["name"])
            tk.Radiobutton(content_frame, text=name, variable=self.bg_var, value=bg["id"],
                          font=self.fantasy_font, bg="#d2b48c").pack(anchor="w", pady=5)

        # Navigation buttons
        tk.Button(self.nav_frame, text=lh.getInfo("button_back"), font=self.fantasy_font, bg="#8b4513",
                 fg="white", padx=10, pady=5, bd=2, command=self.discard_and_back).pack(fill="x", pady=5)
        tk.Button(self.nav_frame, text=lh.getInfo("button_continue"), font=self.fantasy_font, bg="#8b4513",
                 fg="white", padx=10, pady=5, bd=2, command=self.save_and_continue).pack(fill="x", pady=5)

    def save_and_continue(self):
        bg_id = self.bg_var.get()
        self.state.set("background", {"id": bg_id})
        print(f"Saved Background: {self.state.get('background')}")
        super().save_and_continue()