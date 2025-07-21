import tkinter as tk
from tkinter import messagebox
import utils.language_helper as lh
from .has_steps import HasSteps
from .is_step import IsStep
import os
from PIL import Image, ImageTk

STANDARD_ARRAY = [15, 14, 13, 12, 10, 8]
ABILITIES = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]

class StepStatAllocation(IsStep):
    def __init__(self, master, state, wizard: HasSteps):
        super().__init__(master, wizard)
        self.state = state

        # Load and set up dynamic parchment background with Canvas
        self.canvas = tk.Canvas(self, bg="#d2b48c")
        self.canvas.pack(fill="both", expand=True)
        image_path = os.path.join("assets", "parchment.png")
        self.pil_image = Image.open(image_path)
        self.update_background()
        self.bind("<Configure>", self.update_background)

        # Configure fantasy font
        self.fantasy_font = ("Chomsky", 16)

        self.method_var = tk.StringVar(value="array")
        self.assign_vars = {ability: tk.StringVar() for ability in ABILITIES}
        self.method_var.set("array")

        tk.Label(self, text=lh.getInfo("choose_stat_method"), font=(self.fantasy_font[0], 24), bg="#d2b48c").place(x=10, y=10)

        tk.Radiobutton(self, text=lh.getInfo("stat_option_standard"), variable=self.method_var, value="array", command=self.show_method,
                       font=self.fantasy_font, bg="#d2b48c", activebackground="#d2b48c", selectcolor="#8b4513").place(x=10, y=50)
        tk.Radiobutton(self, text=lh.getInfo("stat_option_manual"), variable=self.method_var, value="manual", command=self.show_method,
                       font=self.fantasy_font, bg="#d2b48c", activebackground="#d2b48c", selectcolor="#8b4513").place(x=10, y=80)

        self.method_frame = tk.Frame(self, bg="#d2b48c")
        self.method_frame.place(x=10, y=110)

        self.show_method()

        # Navigation
        nav = tk.Frame(self, bg="#d2b48c")
        nav.place(x=10, y=450)  # Adjusted y position to fit below method_frame
        tk.Button(nav, text=lh.getInfo("button_back"), font=self.fantasy_font, bg="#8b4513", fg="white", padx=10, pady=5, bd=2,
                  command=self.discard_and_back).pack(side="left", padx=10)
        tk.Button(nav, text=lh.getInfo("button_continue"), font=self.fantasy_font, bg="#8b4513", fg="white", padx=10, pady=5, bd=2,
                  command=self.save_and_continue).pack(side="right", padx=10)

    def update_background(self, event=None):
        width = self.winfo_width()
        height = self.winfo_height()
        if width <= 0 or height <= 0:
            return
        resized_image = self.pil_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

    def show_method(self):
        for widget in self.method_frame.winfo_children():
            widget.destroy()

        method = self.method_var.get()

        if method == "array":
            tk.Label(self.method_frame, text=lh.getInfo("option_standard_info"), font=self.fantasy_font, bg="#d2b48c").pack(pady=5)

            self.array_menus = {}

            def update_dropdowns(*args):
                selected_values = [var.get() for var in self.assign_vars.values() if var.get()]
                for ability, menu in self.array_menus.items():
                    current_val = self.assign_vars[ability].get()
                    menu['menu'].delete(0, 'end')
                    for val in STANDARD_ARRAY:
                        state = "normal" if (val not in selected_values or str(val) == current_val) else "disabled"
                        menu['menu'].add_command(
                            label=val,
                            command=lambda v=val, a=ability: self.assign_vars[a].set(str(v))
                        )

            for ability in ABILITIES:
                row = tk.Frame(self.method_frame, bg="#d2b48c")
                row.pack(pady=2)
                tk.Label(row, text=lh.getAbility(ability) + ":", font=self.fantasy_font, bg="#d2b48c").pack(side="left", padx=5)
                var = self.assign_vars[ability]
                var.trace_add("write", update_dropdowns)
                dropdown = tk.OptionMenu(row, var, *STANDARD_ARRAY)
                dropdown.config(font=self.fantasy_font, bg="#f5e8c7", activebackground="#f5e8c7")
                dropdown.pack(side="left")
                self.array_menus[ability] = dropdown

            update_dropdowns()  # Initial call

        elif method == "manual":
            tk.Label(self.method_frame, text=lh.getInfo("option_manual_info"), font=self.fantasy_font, bg="#d2b48c").pack(pady=5)
            for ability in ABILITIES:
                row = tk.Frame(self.method_frame, bg="#d2b48c")
                row.pack(pady=2)
                tk.Label(row, text=lh.getAbility(ability) + ":", font=self.fantasy_font, bg="#d2b48c").pack(side="left", padx=5)
                entry = tk.Entry(row, textvariable=self.assign_vars[ability], font=self.fantasy_font, bg="#f5e8c7")
                entry.pack(side="left")

    def save_and_continue(self):
        stats = {}
        method = self.method_var.get()

        try:
            for ability in ABILITIES:
                val = int(self.assign_vars[ability].get())
                if val < 1 or val > 20:
                    raise ValueError
                stats[ability] = val
        except ValueError:
            messagebox.showerror(lh.getInfo("error"), lh.getInfo("error_option_manual"))
            return
        if method == "array":
            values = list(stats.values())
            if sorted(values) != sorted(STANDARD_ARRAY):
                messagebox.showerror(lh.getInfo("error"), lh.getInfo("error_option_standard"))
                return

        self.state.set("stat_method", method)
        self.state.set("stats", stats)
        super().save_and_continue()

    def destroy(self):
        self.unbind("<Configure>")
        super().destroy()