import tkinter as tk
from tkinter import messagebox
import menu.start_menu
import utils.language_helper as lh
import utils.loaded_data as ld
from state.character_state import CharacterState
from .has_steps import HasSteps
from .is_step import IsStep
import os
from PIL import Image, ImageTk

class StepNameGender(IsStep):
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

        # UI Elements
        tk.Label(self, text=lh.getInfo("choose_character_name"), font=(self.fantasy_font[0], 24), bg="#d2b48c").place(x=10, y=10)
        self.name_entry = tk.Entry(self, font=self.fantasy_font, bg="#f5e8c7")
        self.name_entry.insert(0, self.state.get("name", ""))
        self.name_entry.place(x=10, y=50)

        tk.Label(self, text=lh.getInfo("choose_character_gender"), font=(self.fantasy_font[0], 24), bg="#d2b48c").place(x=10, y=100)
        self.gender_var = tk.StringVar()
        if state.get("gender", "") in ld.genders:
            self.gender_var.set(state.get("gender"))
        else:
            self.gender_var.set(ld.genders[-1])
        for i, g in enumerate(ld.genders):
            tk.Radiobutton(self, text=lh.getGender(g), variable=self.gender_var, value=g, font=self.fantasy_font, bg="#d2b48c",
                           activebackground="#d2b48c", selectcolor="#8b4513").place(x=10, y=150 + i * 30)

        nav = tk.Frame(self, bg="#d2b48c")
        nav.place(x=10, y=250)
        tk.Button(nav, text=lh.getInfo("main_menu"), font=self.fantasy_font, bg="#8b4513", fg="white", padx=10, pady=5, bd=2,
                  command=self.backToMenu).pack(side="left", padx=10)
        tk.Button(nav, text=lh.getInfo("button_continue"), font=self.fantasy_font, bg="#8b4513", fg="white", padx=10, pady=5, bd=2,
                  command=self.save_and_continue).pack(side="left", padx=10)

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