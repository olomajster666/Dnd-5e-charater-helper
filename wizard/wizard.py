import tkinter as tk
from state.character_state import CharacterState
from .step_name_gender import StepNameGender
from .step_race_class import StepRaceClass
from .step_background import StepBackground
from .step_stat_allocation import StepStatAllocation
from .step_proficiencies import StepProficiencies
from .step_spell_selection import StepSpellSelection
from .step_equipment import StepEquipment
from .step_image import StepImage
from .step_character_display import StepCharacterDisplay
from .step_language import StepLanguage

class Wizard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.state = CharacterState()
        self.steps = [
            StepLanguage,
            StepNameGender,
            StepRaceClass,
            StepBackground,
            StepStatAllocation,
            StepProficiencies,
            StepSpellSelection,
            StepEquipment,
            StepImage,
            StepCharacterDisplay,
        ]
        self.current = 0
        self.step_instances = {}
        self.show_step(self.current)

    def show_step(self, index):
        for widget in self.winfo_children():
            widget.destroy()

        if index not in self.step_instances:
            self.step_instances[index] = self.steps[index](self, self.state)
        step = self.step_instances[index]

        step.pack(fill="both", expand=True)

    def next_step(self):
        class_data = self.state.get("class", {})
        current_class = class_data.get("id") if isinstance(class_data, dict) else None
        spellcasting_classes = {"wizard", "cleric", "bard"}

        if self.current < len(self.steps) - 1:
            if self.current == len(self.steps) - 5 and current_class not in spellcasting_classes:  # Before StepSpellSelection
                self.current += 2  # Skip StepSpellSelection
                if self.current >= len(self.steps):  # Ensure we don't exceed the list
                    self.current = len(self.steps) - 1
            else:
                self.current += 1
            self.show_step(self.current)

    def previous_step(self):
        if self.current > 0:
            self.current -= 1
            self.show_step(self.current)