import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

from .fake_wizard import FakeWizard
from state.character_state import CharacterState
from wizard.step_character_display import StepCharacterDisplay
from wizard.wizard import Wizard
import utils.language_helper as lh
import utils.loaded_data as ld
from utils.json_loader import writeLanguageOptions, getSavedCharacterList, loadSavedCharacter

AVAILABLE_LANGUAGES = {lh.getLanguageName(id): id for id in ld.languages}

class StartMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.lang = tk.StringVar(value=lh.getLanguageName(lh.chosenLanguage))
        self.savedCharacterStates = {}

        # Load and set up dynamic parchment background with Canvas
        self.canvas = tk.Canvas(self, bg="#d2b48c")
        self.canvas.pack(fill="both", expand=True)
        image_path = os.path.join("assets", "parchment.png")
        self.pil_image = Image.open(image_path)
        self.update_background()
        self.bind("<Configure>", self.update_background)  # Bind to self instead of master

        # Configure fantasy font (assuming "Chomsky" is installed)
        self.fantasy_font = ("Chomsky", 16)

        # Left navigation frame
        self.nav_frame = tk.Frame(self, bg="#d2b48c", padx=10, pady=10, bd=2, relief="raised")
        self.nav_frame.place(x=10, y=10, height=580, width=200)

        self.showStartMenu()

    def update_background(self, event=None):
        # Resize background image dynamically
        width = self.winfo_width()
        height = self.winfo_height()
        if width <= 0 or height <= 0:
            return
        resized_image = self.pil_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

    def clear_nav_frame(self):
        # Clear all widgets in the navigation frame
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

    def destroyWidgets(self):
        for widget in self.winfo_children():
            if widget != self.canvas and widget != self.nav_frame:
                widget.destroy()

    def addBackButton(self, command=None):
        if command is None:
            command = self.showStartMenu
        tk.Button(self.nav_frame, text=lh.getInfo("button_back"), font=self.fantasy_font, bg="#8b4513",
                  fg="white", padx=10, pady=5, bd=2, command=command).pack(fill="x", pady=5)

    def showStartMenu(self):
        self.destroyWidgets()
        self.clear_nav_frame()

        tk.Label(self, text=lh.getInfo("main_menu"), font=(self.fantasy_font[0], 24), bg="#d2b48c").place(x=220, y=10)
        
        buttons = [
            (lh.getInfo("button_new_character"), self.startWizard),
            (lh.getInfo("button_view_characters"), self.showSavedCharacters),
            (lh.getInfo("button_options"), self.showOptionsMenu),
            (lh.getInfo("button_finish"), self.quitApp)
        ]
        for text, command in buttons:
            tk.Button(self.nav_frame, text=text, font=self.fantasy_font, bg="#8b4513", fg="white",
                      padx=10, pady=5, bd=2, command=command).pack(fill="x", pady=5)

    def showOptionsMenu(self):
        self.destroyWidgets()
        self.clear_nav_frame()

        tk.Label(self, text=lh.getInfo("options_menu"), font=(self.fantasy_font[0], 24), bg="#d2b48c").place(x=220, y=10)

        def save(*args):
            lh.chosenLanguage = AVAILABLE_LANGUAGES.get(self.lang.get())
            writeLanguageOptions(AVAILABLE_LANGUAGES.get(self.lang.get()))
            self.showOptionsMenu()

        langNav = tk.Frame(self, bg="#d2b48c")
        langNav.place(x=220, y=50)
        tk.Label(langNav, text=lh.getInfo("choose_language") + ":", font=self.fantasy_font, bg="#d2b48c").pack(side="left", padx=5)
        self.lang.trace_add("write", save)
        option_menu = tk.OptionMenu(langNav, self.lang, *AVAILABLE_LANGUAGES.keys())
        option_menu.config(bg="#d2b48c", font=self.fantasy_font, bd=2)
        option_menu.pack(side="left", padx=5)

        self.addBackButton()

    def showSavedCharacters(self):
        self.destroyWidgets()
        self.clear_nav_frame()

        tk.Label(self, text=lh.getInfo("saved_characters"), font=(self.fantasy_font[0], 24), bg="#d2b48c").place(x=220, y=10)

        for fileName in getSavedCharacterList():
            data = loadSavedCharacter(fileName)
            self.savedCharacterStates[fileName] = data
            row = tk.Frame(self, bg="#d2b48c")
            row.place(x=220, y=50 + len(self.savedCharacterStates) * 30)
            tk.Button(row, text=fileName.removesuffix(".json").capitalize(), font=self.fantasy_font, bg="#8b4513",
                      fg="white", padx=10, pady=5, bd=2, command=lambda x=fileName: self.showChosenCharacter(x)).pack()

        self.addBackButton()

    def showChosenCharacter(self, chosen):
        self.destroyWidgets()

        print(chosen)
        state = CharacterState(self.savedCharacterStates[chosen])
        fakeWizard = FakeWizard(self.master, self)
        app = StepCharacterDisplay(self.master, state, fakeWizard)
        app.characterSaved = True
        fakeWizard.previousScreen = app

        self.destroy()
        app.pack(side="top", expand=True, fill="both")

    def startWizard(self):
        self.destroyWidgets()

        app = Wizard(self.master)
        self.destroy()
        app.pack(side="top", expand=True, fill="both")

    def quitApp(self):
        self.master.quit()

    def destroy(self):
        self.unbind("<Configure>")
        super().destroy()