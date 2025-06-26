import tkinter as tk

from wizard.wizard import Wizard
import utils.language_helper as lh
from utils.json_loader import writeLanguageOptions


class StartMenu(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.lang = tk.StringVar(value=lh.chosenLanguage)

        self.showStartMenu()


    def destroyWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()


    def showStartMenu(self):
        self.destroyWidgets()

        tk.Label(self, text=lh.getInfo("main_menu"), font=("Arial", 16)).pack(pady=10)

        nav = tk.Frame(self)
        nav.pack(side="top", pady=20)
        tk.Button(nav, text=lh.getInfo("button_new_character"), command=self.startWizard).pack(pady=5)
        tk.Button(nav, text=lh.getInfo("button_options"), command=self.showOptionsMenu).pack(pady=5)


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

        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text=lh.getInfo("button_back"), command=self.showStartMenu).pack()



    def startWizard(self):
        self.destroyWidgets()

        app = Wizard(self.master)
        self.destroy()
        app.pack(side="top", expand=True, fill="both")
