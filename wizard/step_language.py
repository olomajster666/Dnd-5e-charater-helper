import tkinter as tk
import utils.language_helper as lh

class StepLanguage(tk.Frame):

    def __init__(self, master, state):
        super().__init__(master)
        self.master = master
        self.state = state

        tk.Label(self, text="Choose language", font=("Arial", 16)).pack(pady=10)
        self.lang_var = tk.StringVar(value="en")
        for lang in lh.languages:
            tk.Radiobutton(self, text=lang, variable=self.lang_var, value=lang).pack()

        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text="Start", command=self.save_and_continue).pack()


    def save_and_continue(self):
        lh.chosenLanguage = self.lang_var.get()
        self.master.next_step()