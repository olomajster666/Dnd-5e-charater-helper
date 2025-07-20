import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import utils.language_helper as lh
from .has_steps import HasSteps
from .is_step import IsStep


class StepImage(IsStep):
    def __init__(self, master, state, wizard : HasSteps):
        super().__init__(master, wizard)
        self.state = state
        self.image_path = tk.StringVar()

        tk.Label(self, text=lh.getInfo("add_character_image"), font=("Arial", 16)).pack(pady=10)
        tk.Button(self, text=lh.getInfo("choose_image"), command=self.load_image).pack(pady=5)
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10)

        tk.Button(self, text=lh.getInfo("button_skip"), command=self.skip_and_continue).pack(side="left", padx=10, pady=20)
        tk.Button(self, text=lh.getInfo("button_continue"), command=self.save_and_continue).pack(side="right", padx=10, pady=20)

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