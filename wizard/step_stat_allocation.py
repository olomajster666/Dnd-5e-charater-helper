import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import utils.language_helper as lh
from .has_steps import HasSteps
from .is_step import IsStep

STANDARD_ARRAY = [15, 14, 13, 12, 10, 8]
ABILITIES = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]

class StepStatAllocation(IsStep):
    def __init__(self, master, state, wizard: HasSteps):
        super().__init__(master, wizard)
        self.state = state

        # Load parchment background
        image_path = os.path.join("assets", "parchment.png")
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(pil_image)
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Configure fantasy font
        self.fantasy_font = ("Chomsky", 16)

        # Navigation frame on the left
        self.nav_frame = tk.Frame(self, bg="#d2b48c", padx=10, pady=10, bd=2, relief="raised")
        self.nav_frame.place(x=10, y=10, height=580, width=200)

        # Title
        tk.Label(self, text=lh.getInfo("choose_stat_method"), font=("Chomsky", 24), bg="#d2b48c").place(x=220, y=10)

        # Method selection with radio buttons
        self.method_var = tk.StringVar(value="array")
        method_frame = tk.Frame(self, bg="#d2b48c", bd=1, relief="groove")
        method_frame.place(x=220, y=50, width=300, height=80)
        tk.Radiobutton(method_frame, text=lh.getInfo("stat_option_standard"), variable=self.method_var, value="array",
                       font=self.fantasy_font, bg="#d2b48c", command=self.show_method).pack(anchor="w", padx=10, pady=5)
        tk.Radiobutton(method_frame, text=lh.getInfo("stat_option_manual"), variable=self.method_var, value="manual",
                       font=self.fantasy_font, bg="#d2b48c", command=self.show_method).pack(anchor="w", padx=10, pady=5)

        # Method-specific input frame
        self.method_frame = tk.Frame(self, bg="#d2b48c")
        self.method_frame.place(x=220, y=150, width=450, height=300)
        self.assign_vars = {ability: tk.StringVar() for ability in ABILITIES}
        self.show_method()

        # Navigation buttons
        tk.Button(self.nav_frame, text=lh.getInfo("button_back"), font=self.fantasy_font, bg="#8b4513",
                 fg="white", padx=10, pady=5, bd=2, command=self.discard_and_back).pack(fill="x", pady=5)
        tk.Button(self.nav_frame, text=lh.getInfo("button_continue"), font=self.fantasy_font, bg="#8b4513",
                 fg="white", padx=10, pady=5, bd=2, command=self.save_and_continue).pack(fill="x", pady=5)

    def show_method(self):
        for widget in self.method_frame.winfo_children():
            widget.destroy()

        method = self.method_var.get()

        if method == "array":
            tk.Label(self.method_frame, text=lh.getInfo("option_standard_info"), font=self.fantasy_font,
                    bg="#d2b48c").pack(anchor="w", pady=5)
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

            for i, ability in enumerate(ABILITIES):
                row = tk.Frame(self.method_frame, bg="#d2b48c")
                row.pack(anchor="w", pady=2)
                tk.Label(row, text=lh.getAbility(ability) + ":", font=self.fantasy_font, bg="#d2b48c").pack(side="left", padx=5)
                var = self.assign_vars[ability]
                var.trace_add("write", update_dropdowns)
                dropdown = tk.OptionMenu(row, var, *STANDARD_ARRAY)
                dropdown.config(font=self.fantasy_font, bg="#d2b48c")
                dropdown.pack(side="left")
                self.array_menus[ability] = dropdown

            update_dropdowns()

        elif method == "manual":
            tk.Label(self.method_frame, text=lh.getInfo("option_manual_info"), font=self.fantasy_font,
                    bg="#d2b48c").pack(anchor="w", pady=5)
            for i, ability in enumerate(ABILITIES):
                row = tk.Frame(self.method_frame, bg="#d2b48c")
                row.pack(anchor="w", pady=2)
                tk.Label(row, text=lh.getAbility(ability) + ":", font=self.fantasy_font, bg="#d2b48c").pack(side="left", padx=5)
                entry = tk.Entry(row, textvariable=self.assign_vars[ability], font=self.fantasy_font)
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