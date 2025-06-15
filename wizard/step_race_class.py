import tkinter as tk
from utils.json_loader import load_json

class StepRaceClass(tk.Frame):
    def __init__(self, master, state):
        super().__init__(master)
        self.master = master
        self.state = state

        # Load data
        self.race_options = {race["id"]: race for race in load_json("races.json")}
        self.class_options = {cls["id"]: cls for cls in load_json("classes.json")}

        self.race_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.race_var.set("human")
        self.class_var.set("fighter")

        tk.Label(self, text="Wybierz rasę", font=("Arial", 16)).pack(pady=10)
        for race in self.race_options.values():
            name = race["name"]["pl"]
            tk.Radiobutton(self, text=name, variable=self.race_var, value=race["id"]).pack()

        tk.Label(self, text="Wybierz klasę", font=("Arial", 16)).pack(pady=10)
        for cls in self.class_options.values():
            name = cls["name"]["pl"]
            tk.Radiobutton(self, text=name, variable=self.class_var, value=cls["id"]).pack()

        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=20)
        tk.Button(nav, text="Wstecz", command=self.master.previous_step).pack(side="left", padx=10)
        tk.Button(nav, text="Dalej", command=self.save_and_continue).pack(side="right", padx=10)

    def save_and_continue(self):
        race_id = self.race_var.get()
        class_id = self.class_var.get()
        self.state.set("race", {"id": race_id})
        self.state.set("class", {"id": class_id})
        print(f"Saved Race: {self.state.get('race')}, Class: {self.state.get('class')}")  # Debug
        self.master.next_step()