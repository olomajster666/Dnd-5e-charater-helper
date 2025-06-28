import tkinter as tk
import utils.language_helper as lh
import utils.loaded_data as ld
from PIL import Image, ImageTk
import os
from logic.modifier_calculator import calculate_modifier
from logic.health_calculator import calculate_health
import menu.start_menu
from utils.json_loader import saveCharacter
from tkinter import messagebox

from .has_steps import HasSteps
from .is_step import IsStep


class StepCharacterDisplay(IsStep):
    def __init__(self, master, state, wizard : HasSteps):
        super().__init__(master, wizard)
        self.state = state

        self.classes = {cls["id"]: cls for cls in ld.classes}
        self.races = {race["id"]: race for race in ld.races}
        self.backgrounds = {bg["id"]: bg for bg in ld.backgrounds}
        self.proficiencies_data = {prof["id"]: prof for prof in ld.proficiencies}

        tk.Label(self, text=lh.getInfo("created_character_display"), font=("Arial", 16)).pack(pady=10)
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10)
        self.display_text = tk.Text(self, height=20, width=80)
        self.display_text.pack(pady=10)

        self.update_display()
        tk.Button(self, text=lh.getInfo("button_back"), command=self.discard_and_back).pack(side="left", padx=10, pady=20)
        tk.Button(self, text=lh.getInfo("main_menu"), command=self.backToMenu).pack(side="right", padx=10, pady=20)
        tk.Button(self, text=lh.getInfo("button_save_character"), command=self.saveCharacterToFile).pack(side="right", padx=10, pady=20)

        self.characterSaved = False

    def update_display(self):
        state = self.state.data
        class_data = state.get("class", {})
        current_class = class_data.get("id") if isinstance(class_data, dict) else None
        background_data = state.get("background", {})
        stats = state.get("stats", {})
        race_data = state.get("race", {})
        racial_bonuses = self.races.get(race_data.get("id"), {}).get("ability_bonuses", {})

        # Apply racial bonuses to stats
        final_stats = {}
        for stat, value in stats.items():
            bonus = racial_bonuses.get(stat, 0)
            final_stats[stat] = value + bonus

        # Calculate modifiers based on final stats with racial bonuses
        modifiers = {stat: calculate_modifier(score) for stat, score in final_stats.items()}

        # Health calculation
        con_score = final_stats.get("constitution", 10)
        health = calculate_health(current_class, con_score, self.classes)

        # Spells (if applicable)
        if current_class not in {"wizard", "cleric", "bard"}:
            spells = ["no_spells"]
        else:
            spells = state.get("spells", [])

        # Abilities from classes.json
        abilities = []
        if current_class and current_class in self.classes:
            for feature in self.classes[current_class].get("level_1_features", []):
                abilities.append(f"{lh.getFeatureName(feature)}: {lh.getFeatureDescription(feature)}")

        # Get race name
        race_id = race_data.get("id")
        race_name = lh.getRaceName(race_id)

        # Get class and background names
        class_name = "None"
        if isinstance(class_data, dict) and "id" in class_data:
            class_name = lh.getClassName(class_data["id"])

        # Get background name
        background_name = "None"
        if isinstance(background_data, dict) and "id" in background_data:
            background_name = lh.getBackgroundName(background_data["id"])

        # Image handling
        image_path = state.get("image_path")
        if image_path and os.path.exists(image_path):
            img = Image.open(image_path).resize((200, 200), Image.Resampling.LANCZOS)
        else:
            img = Image.open(os.path.join("assets", "blank_character.png")).resize((200, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference!

        # Equipment
        equipment = state.get("equipment", [])
        equipment_display = "\n".join([f"  - {lh.getItemCountAndName(item)}" for item in equipment]) if equipment else "  - " + lh.getInfo("no_equipment")

        # Proficiencies
        proficiencies = state.get("proficiencies", [])
        proficiency_ids = proficiencies  # Use strings directly as proficiency IDs
        skill_proficiencies = {prof["id"]: prof for prof in self.proficiencies_data.values() if prof["type"] == "skill"}

        # Map skills to stats and calculate modifiers
        stat_skills = {
            "strength": [],
            "dexterity": [],
            "intelligence": [],
            "wisdom": [],
            "charisma": []
        }
        for skill_id, skill in skill_proficiencies.items():
            ability = skill.get("ability")
            if ability in stat_skills:
                base_modifier = modifiers.get(ability, "+0")
                base_value = int(base_modifier.replace("+", ""))
                proficiency_bonus = 2 if skill_id in proficiency_ids else 0
                total_modifier = base_value + proficiency_bonus
                total_modifier_str = f"+{total_modifier}" if total_modifier >= 0 else str(total_modifier)
                skill_name = lh.getProficiency(skill.get("id", "None"))
                display_name = f"* {skill_name} ({total_modifier_str})" if skill_id in proficiency_ids else f"{skill_name} ({total_modifier_str})"
                stat_skills[ability].append(display_name)

        # Display content with bold stats
        display_parts = [
            lh.getInfo("character_display"),
            f"{lh.getInfo('name_and_race')} {state.get('name', 'None')} - {race_name}",
            f"{lh.getInfo('class_and_level')} {class_name} - {lh.getInfo('level')} 1",
            f"{lh.getInfo('background')} {background_name}",
            lh.getInfo("stats_and_modifiers"),
            f"  **{lh.getAbility('strength')}:** {final_stats.get('strength', 10)} ({modifiers.get('strength', '+0')})" + ("\n" + "\n".join(stat_skills["strength"]) if stat_skills["strength"] else ""),
            f"  **{lh.getAbility('dexterity')}:** {final_stats.get('dexterity', 10)} ({modifiers.get('dexterity', '+0')})" + ("\n" + "\n".join(stat_skills["dexterity"]) if stat_skills["dexterity"] else ""),
            f"  **{lh.getAbility('constitution')}:** {final_stats.get('constitution', 10)} ({modifiers.get('constitution', '+0')})",  # No skills for Constitution
            f"  **{lh.getAbility('intelligence')}:** {final_stats.get('intelligence', 10)} ({modifiers.get('intelligence', '+0')})" + ("\n" + "\n".join(stat_skills["intelligence"]) if stat_skills["intelligence"] else ""),
            f"  **{lh.getAbility('wisdom')}:** {final_stats.get('wisdom', 10)} ({modifiers.get('wisdom', '+0')})" + ("\n" + "\n".join(stat_skills["wisdom"]) if stat_skills["wisdom"] else ""),
            f"  **{lh.getAbility('charisma')}:** {final_stats.get('charisma', 10)} ({modifiers.get('charisma', '+0')})" + ("\n" + "\n".join(stat_skills["charisma"]) if stat_skills["charisma"] else ""),
            f"{lh.getInfo('health')}: {health}",
            f"{lh.getInfo('spells')}: {', '.join(self.getTranslatedSpells(spells))}",
            f"{lh.getInfo('abilities')}:" + ("\n" + "\n".join(abilities) if abilities else "\n" + lh.getInfo("no_abilities")),
            f"{lh.getInfo('equipment')}:" + "\n" + equipment_display
        ]
        display = "\n".join(display_parts)
        print("Full display content:", display)

        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, display)


    def getTranslatedSpells(self, spells : list):
        tr = []
        for spell in spells:
            if(spell == "no_spells"):
                tr.append(lh.getInfo("no_spells"))
                return tr
            tr.append(lh.getSpellName(spell))

        return tr

    def backToMenu(self):
        if(self.characterSaved or messagebox.askquestion(lh.getInfo("warning"), lh.getInfo("u_sure")) == "yes"):
            app = menu.start_menu.StartMenu(self.master)
            self.destroy()
            app.pack(side="top", expand=True, fill="both")


    def saveCharacterToFile(self):
        if(saveCharacter(self.state)):
            messagebox.showinfo(lh.getInfo("success"), lh.getInfo("character_save_success"))
            self.characterSaved = True
        else:
            messagebox.showerror(lh.getInfo("error"), lh.getInfo("character_save_failure"))