import tkinter as tk
from state.character_state import CharacterState
from .has_steps import HasSteps
from .step_name_gender import StepNameGender
from .step_race_class import StepRaceClass
from .step_background import StepBackground
from .step_stat_allocation import StepStatAllocation
from .step_proficiencies import StepProficiencies
from .step_spell_selection import StepSpellSelection
from .step_equipment import StepEquipment
from .step_image import StepImage
from .step_character_display import StepCharacterDisplay


SPELLCASTING_CLASSES = {"wizard", "cleric", "bard"}

class Wizard(tk.Frame, HasSteps):
    def __init__(self, master):
        super().__init__(master)
        self.state = CharacterState()
        self.steps = [
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
        # sprawdzam czy moge pushowac
        #self.step_instances = {}
        self.show_step(self.current)

    def show_step(self, index):
        #for widget in self.winfo_children():
        #    widget.destroy()

        #if index not in self.step_instances:
        #    self.step_instances[index] = self.steps[index](self, self.state, self)
        step = self.steps[index](self, self.state, self)

        step.pack(fill="both", expand=True)

    def next_step(self):
        if self.current < len(self.steps) - 1:
            if self.current == len(self.steps) - 5 and self.shouldSkipSpellSelection():  # Before StepSpellSelection
                self.current += 2  # Skip StepSpellSelection
                if self.current >= len(self.steps):  # Ensure we don't exceed the list
                    self.current = len(self.steps) - 1
            else:
                self.current += 1
            self.show_step(self.current)

    def previous_step(self):
        if self.current > 0:
            if(self.current == len(self.steps) - 3 and self.shouldSkipSpellSelection()):
                self.current -= 2
            else:
                self.current -= 1

            self.current = 0 if self.current < 0 else self.current
            self.show_step(self.current)

    def shouldSkipSpellSelection(self):
        class_data = self.state.get("class", {})
        current_class = class_data.get("id") if isinstance(class_data, dict) else None
        return current_class not in SPELLCASTING_CLASSES