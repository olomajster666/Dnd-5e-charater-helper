import tkinter as tk
from utils.json_loader import load_json
from PIL import Image, ImageTk
import os
from logic.modifier_calculator import calculate_modifier
from logic.health_calculator import calculate_health

class StepCharacterDisplay(tk.Frame):
    def __init__(self, master, state):
        super().__init__(master)
        self.master = master
        self.state = state
        self.classes = {cls["id"]: cls for cls in load_json("classes.json")}
        self.races = {race["id"]: race for race in load_json("races.json")}
        self.backgrounds = {bg["id"]: bg for bg in load_json("backgrounds.json")}
        self.proficiencies_data = {prof["id"]: prof for prof in load_json("proficiencies.json")}

        tk.Label(self, text="Podgląd Stworzonej Postaci:", font=("Arial", 16)).pack(pady=10)
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10)
        self.display_text = tk.Text(self, height=20, width=80)
        self.display_text.pack(pady=10)

        self.update_display()
        tk.Button(self, text="Wstecz", command=self.master.previous_step).pack(side="left", padx=10, pady=20)
        tk.Button(self, text="Zakończ", command=self.quit_app).pack(side="right", padx=10, pady=20)

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
        spells = state.get("spells", [])
        if current_class not in {"wizard", "cleric", "bard"}:
            spells = ["Brak zaklęć"]

        # Abilities from classes.json
        abilities = []
        if current_class and current_class in self.classes:
            for feature in self.classes[current_class].get("level_1_features", []):
                abilities.append(f"{feature['name']['pl']}: {feature['description']['pl']}")

        # Get race name in Polish
        race_id = race_data.get("id")
        race_name = self.races.get(race_id, {}).get("name", {}).get("pl", race_data.get("id", "Brak"))

        # Get class and background names in Polish
        class_name = "Brak"
        if isinstance(class_data, dict) and "id" in class_data:
            class_name = self.classes.get(class_data["id"], {}).get("name", {}).get("pl", "Brak")

        # Get background name in Polish
        background_name = "Brak"
        if isinstance(background_data, dict) and "id" in background_data:
            background_name = self.backgrounds.get(background_data["id"], {}).get("name", {}).get("pl", "Brak")

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
        equipment_display = "\n".join([f"  - {item}" for item in equipment]) if equipment else "  - Brak wyposażenia"

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
                skill_name = skill.get("name", {}).get("pl", skill_id)
                display_name = f"* {skill_name} ({total_modifier_str})" if skill_id in proficiency_ids else f"{skill_name} ({total_modifier_str})"
                stat_skills[ability].append(display_name)

        # Display content with bold stats
        display_parts = [
            "Podgląd Postaci:",
            f"Imię i Rasa: {state.get('name', 'Brak')} - {race_name}",
            f"Klasa i Poziom: {class_name} - Poziom 1",
            f"Tło: {background_name}",
            "Statystyki i Modyfikatory:",
            f"  **Siła:** {final_stats.get('strength', 10)} ({modifiers.get('strength', '+0')})" + ("\n" + "\n".join(stat_skills["strength"]) if stat_skills["strength"] else ""),
            f"  **Zręczność:** {final_stats.get('dexterity', 10)} ({modifiers.get('dexterity', '+0')})" + ("\n" + "\n".join(stat_skills["dexterity"]) if stat_skills["dexterity"] else ""),
            f"  **Kondycja:** {final_stats.get('constitution', 10)} ({modifiers.get('constitution', '+0')})",  # No skills for Constitution
            f"  **Inteligencja:** {final_stats.get('intelligence', 10)} ({modifiers.get('intelligence', '+0')})" + ("\n" + "\n".join(stat_skills["intelligence"]) if stat_skills["intelligence"] else ""),
            f"  **Mądrość:** {final_stats.get('wisdom', 10)} ({modifiers.get('wisdom', '+0')})" + ("\n" + "\n".join(stat_skills["wisdom"]) if stat_skills["wisdom"] else ""),
            f"  **Charyzma:** {final_stats.get('charisma', 10)} ({modifiers.get('charisma', '+0')})" + ("\n" + "\n".join(stat_skills["charisma"]) if stat_skills["charisma"] else ""),
            f"Zdrowie: {health}",
            f"Zaklęcia: {', '.join(spells)}",
            "Zdolności:" + ("\n" + "\n".join(abilities) if abilities else "\nBrak zdolności"),
            "Wyposażenie:" + "\n" + equipment_display
        ]
        display = "\n".join(display_parts)
        print("Full display content:", display)

        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, display)

    def quit_app(self):
        self.master.quit()