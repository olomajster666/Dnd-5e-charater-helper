import json
import os

from state.character_state import CharacterState


def load_json(filename):
    path = os.path.join("data", filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def writeLanguageOptions(chosenLanguage: str = "en"):
    path = os.path.join("data", "options/language.txt")
    with open(path, "w") as f:
        f.write(chosenLanguage)


def loadLanguageOptions():
    path = os.path.join("data", "options/language.txt")
    try:
        with open(path) as f:
            return f.read()

    except:
        writeLanguageOptions()
        return loadLanguageOptions()


def loadSavedCharacter(fileName : str):
    try:
        json = load_json("saved_characters/" + fileName)
        return json
    except:
        print(f"An error occurred while reading saved character from the following JSON file: {fileName}")
        return {}

def getSavedCharacterList():
    return [f for f in os.listdir(os.path.join("data", "saved_characters")) if os.path.isfile(os.path.join("data", f"saved_characters/{f}")) and f.__contains__(".json")]


def saveCharacter(state : CharacterState):
    try:
        fileName = state.get("name", "no name") + ".json"
        number = 1
        existingCharacters = getSavedCharacterList()
        while(fileName in existingCharacters):
            fileName = f"{state.get('name', 'no name')} ({number}).json"
            number += 1

        path = os.path.join("data", "saved_characters/" + fileName)
        with open(path, "w", encoding="utf-8") as f:
            print(path)
            json.dump(state.data, f)
            return True

    except:
        print("Failed to save character")
        return False
