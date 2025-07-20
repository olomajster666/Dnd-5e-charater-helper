import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import menu.start_menu
import utils.language_helper as lh
from .has_steps import HasSteps
from .is_step import IsStep

class StepNameGender(IsStep):
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

        # Title and input for name
        tk.Label(self, text=lh.getInfo("choose_character_name"), font=("Chomsky", 24), bg="#d2b48c").place(x=220, y=10)
        self.name_entry = tk.Entry(self, font=self.fantasy_font)
        self.name_entry.place(x=220, y=50, width=200)

        # Gender selection
        tk.Label(self, text=lh.getInfo("choose_character_gender"), font=("Chomsky", 24), bg="#d2b48c").place(x=220, y=90)
        self.gender_var = tk.StringVar(value=lh.getGenders()[-1])
        content_frame = tk.Frame(self, bg="#d2b48c")
        content_frame.place(x=220, y=130)
        for i, g in enumerate(lh.getGenders()):
            tk.Radiobutton(content_frame, text=g, variable=self.gender_var, value=g,
                          font=self.fantasy_font, bg="#d2b48c").pack(anchor="w", pady=5)

        # Navigation buttons
        tk.Button(self.nav_frame, text=lh.getInfo("main_menu"), font=self.fantasy_font, bg="#8b4513",
                 fg="white", padx=10, pady=5, bd=2, command=self.backToMenu).pack(fill="x", pady=5)
        tk.Button(self.nav_frame, text=lh.getInfo("button_continue"), font=self.fantasy_font, bg="#8b4513",
                 fg="white", padx=10, pady=5, bd=2, command=self.save_and_continue).pack(fill="x", pady=5)

    def save_and_continue(self):
        name = self.name_entry.get().strip()
        if name == "":
            messagebox.showerror(lh.getInfo("error"), lh.getInfo("error_character_name_wrong"))
            return
        self.state.set("name", name)
        self.state.set("gender", self.gender_var.get())
        super().save_and_continue()

    def backToMenu(self):
        result = messagebox.askquestion(lh.getInfo("warning"), lh.getInfo("u_sure"))
        if result == 'yes' or result == True:
            app = menu.start_menu.StartMenu(self.master)
            self.destroy()
            app.pack(side="top", expand=True, fill="both")