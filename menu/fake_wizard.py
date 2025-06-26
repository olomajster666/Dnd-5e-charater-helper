import tkinter

import menu.start_menu
import wizard.has_steps


class FakeWizard(wizard.has_steps.HasSteps):

    def __init__(self, master, previousScreen : tkinter.Frame):
        self.master = master
        self.previousScreen = previousScreen

    def next_step(self):
        pass

    def previous_step(self):
        app = menu.start_menu.StartMenu(self.master)
        app.showSavedCharacters()
        self.previousScreen.destroy()
        app.pack(side="top", expand=True, fill="both")