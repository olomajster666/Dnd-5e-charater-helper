import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import utils.language_helper as lh
from state.character_state import CharacterState
from .has_steps import HasSteps
from .is_step import IsStep
import os

class StepImage(IsStep):
    def __init__(self, master, state: CharacterState, wizard: HasSteps):
        super().__init__(master, wizard)
        self.state = state
        self.image_path = tk.StringVar()

        # Load and set up dynamic parchment background with Canvas
        self.canvas = tk.Canvas(self, bg="#d2b48c")
        self.canvas.pack(fill="both", expand=True)
        image_path = os.path.join("assets", "parchment.png")
        self.pil_image = Image.open(image_path)
        self.update_background()
        self.bind("<Configure>", self.update_background)

        # Configure fantasy font
        self.fantasy_font = ("Chomsky", 16)

        if(self.state.get("image_path") != None):
            self.image_path.set(self.state.get("image_path"))

        tk.Label(self.canvas, text=lh.getInfo("add_character_image"), font=self.fantasy_font, bg="#d2b48c").pack(pady=10)
        tk.Button(self.canvas, text=lh.getInfo("choose_image"), font=self.fantasy_font, bg="#8b4513", fg="white", padx=10, pady=5, bd=2,
                  command=self.load_image).pack(pady=5)
        self.image_label = tk.Label(self.canvas, bg="#d2b48c")
        self.image_label.pack(pady=10)

        # Navigation
        self.nav = tk.Frame(self.canvas, bg="#d2b48c")
        self.nav.pack(side="bottom", pady=20)
        tk.Button(self.nav, text=lh.getInfo("button_back"), font=self.fantasy_font, bg="#8b4513", fg="white", padx=10, pady=5, bd=2,
                  command=self.discard_and_back).pack(side="left", padx=10)
        tk.Button(self.nav, text=lh.getInfo("button_skip"), font=self.fantasy_font, bg="#8b4513", fg="white", padx=10, pady=5, bd=2,
                  command=self.skip_and_continue).pack(side="right", padx=10)
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

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if path:
            self.image_path.set(path)
            img = Image.open(path).resize((200, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference!

    def skip_and_continue(self):
        self.state.set("image_path", None)
        super().save_and_continue()

    def save_and_continue(self):
        image_path = self.image_path.get() if self.image_path.get() else None
        self.state.set("image_path", image_path)
        super().save_and_continue()