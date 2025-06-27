import tkinter

from .has_steps import HasSteps


class IsStep(tkinter.Frame):

    def __init__(self, master, wizard : HasSteps):
        super().__init__(master)
        self.wizard = wizard


    def save_and_continue(self):
        self.destroy()
        self.wizard.next_step()

    def discard_and_back(self):
        self.destroy()
        self.wizard.previous_step()