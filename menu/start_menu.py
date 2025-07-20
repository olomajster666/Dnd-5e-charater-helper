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

AVAILABLE_LANGUAGES = {lh.getLanguageName(id) : id for id in ld.languages}

class StartMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.lang = tk.StringVar(value=lh.getLanguageName(lh.chosenLanguage))
        self.savedCharacterStates = {}

        # Load parchment background with PIL
        image_path = os.path.join("assets", "parchment.png")
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize to match window size
        self.bg_image = ImageTk.PhotoImage(pil_image)
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Configure fantasy font (assuming "Chomsky" is installed)
        self.fantasy_font = ("Chomsky", 16)  # Adjust size as needed

        # Left navigation frame
        self.nav_frame = tk.Frame(self, bg="#d2b48c", padx=10, pady=10, bd=2, relief="raised")  # Updated to match parchment
        self.nav_frame.place(x=10, y=10, height=580, width=200)  # Fixed position and size

        self.showStartMenu()

    def destroyWidgets(self):
        for widget in self.winfo_children():
            if widget != self.bg_label and widget != self.nav_frame:
                widget.destroy()

    def addBackButton(self, command=None):
        if command is None:
            command = self.showStartMenu
        tk.Button(self.nav_frame, text=lh.getInfo("button_back"), font=self.fantasy_font, bg="#8b4513",
                  fg="white", padx=10, pady=5, bd=2, command=command).pack(fill="x", pady=5)

    def showStartMenu(self):
        self.destroyWidgets()

        tk.Label(self, text=lh.getInfo("main_menu"), font=(self.fantasy_font[0], 24), bg="#d2b48c").place(x=220, y=10)  # Updated to match parchment
        
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

        tk.Label(self, text=lh.getInfo("options_menu"), font=(self.fantasy_font[0], 24), bg="#d2b48c").place(x=220, y=10)  # Updated to match parchment

        def save(*args):
            lh.chosenLanguage = AVAILABLE_LANGUAGES.get(self.lang.get())
            writeLanguageOptions(AVAILABLE_LANGUAGES.get(self.lang.get()))
            self.showOptionsMenu()

        langNav = tk.Frame(self, bg="#d2b48c")  # Updated to match parchment
        langNav.place(x=220, y=50)
        tk.Label(langNav, text=lh.getInfo("choose_language") + ":", font=self.fantasy_font).pack(side="left", padx=5)
        self.lang.trace_add("write", save)
        tk.OptionMenu(langNav, self.lang, *AVAILABLE_LANGUAGES.keys()).pack(side="left", padx=5)

        self.addBackButton()

    def showSavedCharacters(self):
        self.destroyWidgets()

        tk.Label(self, text=lh.getInfo("saved_characters"), font=(self.fantasy_font[0], 24), bg="#d2b48c").place(x=220, y=10)  # Updated to match parchment

        for fileName in getSavedCharacterList():
            data = loadSavedCharacter(fileName)
            self.savedCharacterStates[fileName] = data
            row = tk.Frame(self, bg="#d2b48c")  # Updated to match parchment
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