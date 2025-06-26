import tkinter as tk

from wizard.wizard import Wizard
import utils.language_helper as lh
from utils.json_loader import writeLanguageOptions, getSavedCharacterList, loadSavedCharacter


class StartMenu(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.lang = tk.StringVar(value=lh.chosenLanguage)
        self.savedCharacterStates = {}

        self.showStartMenu()


    def destroyWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def addBackButton(self, command = None):
        if(command == None):
            command = self.showStartMenu

        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text=lh.getInfo("button_back"), command=command).pack()

    def showStartMenu(self):
        self.destroyWidgets()

        tk.Label(self, text=lh.getInfo("main_menu"), font=("Arial", 16)).pack(pady=10)

        nav = tk.Frame(self)
        nav.pack(side="top", pady=20)
        tk.Button(nav, text=lh.getInfo("button_new_character"), command=self.startWizard).pack(pady=5)
        tk.Button(nav, text=lh.getInfo("button_view_characters"), command=self.showSavedCharacters).pack(pady=12)
        tk.Button(nav, text=lh.getInfo("button_options"), command=self.showOptionsMenu).pack(pady=5)
        tk.Button(nav, text=lh.getInfo("button_finish"), command=self.quitApp).pack(pady=20)


    def showOptionsMenu(self):
        self.destroyWidgets()

        tk.Label(self, text=lh.getInfo("options_menu"), font=("Arial", 16)).pack(pady=10)

        def save(*args):
            lh.chosenLanguage = self.lang.get()
            writeLanguageOptions(self.lang.get())
            self.showOptionsMenu()


        langNav = tk.Frame(self)
        langNav.pack(side="top", pady=20)

        tk.Label(langNav, text=lh.getInfo("choose_language") + ":").pack(side="left", padx=5)

        self.lang.trace_add("write", save)
        tk.OptionMenu(langNav, self.lang, *lh.languages).pack(side="left", padx=5)

        self.addBackButton()

    def showSavedCharacters(self):
        self.destroyWidgets()

        tk.Label(self, text=lh.getInfo("saved_characters"), font=("Arial", 16)).pack(pady=10)

        for fileName in getSavedCharacterList():
            data = loadSavedCharacter(fileName)
            self.savedCharacterStates[fileName] = data
            row = tk.Frame(self)
            row.pack(side="top", pady=20)
            tk.Button(row, text=fileName.removesuffix(".json").capitalize(), command=lambda: self.showChosenCharacter(fileName)).pack(pady=5)

        self.addBackButton()


    def showChosenCharacter(self, chosen):
        self.destroyWidgets()

        print(self.savedCharacterStates[chosen])

        self.addBackButton(self.showSavedCharacters)

    def startWizard(self):
        self.destroyWidgets()

        app = Wizard(self.master)
        self.destroy()
        app.pack(side="top", expand=True, fill="both")

    def quitApp(self):
        self.master.quit()
