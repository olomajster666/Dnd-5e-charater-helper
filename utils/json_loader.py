import json
import os


def load_json(filename):
    path = os.path.join("data", filename)
    print(path)
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
    return load_json("saved_characters/" + fileName)

def getSavedCharacterList():
    return [f for f in os.listdir(os.path.join("data", "saved_characters")) if os.path.isfile(os.path.join("data", f"saved_characters/{f}")) and f.__contains__(".json")]
