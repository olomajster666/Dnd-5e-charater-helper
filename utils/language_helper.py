import utils.json_loader as jl

chosenLanguage = "en"

# to avoid loading one json multiple times
backgrounds = jl.load_json("backgrounds.json")
classes = jl.load_json("classes.json")
proficiencies = jl.load_json("proficiencies.json")
races = jl.load_json("races.json")
spells = jl.load_json("spells.json")

# only for translations
genders = jl.load_json("lang/genders.json")
info = jl.load_json("lang/info.json")
languages = jl.load_json("lang/languages.json")
abilities = jl.load_json("lang/abilities.json")


def getFromDict(d : dict):
    return d.get(chosenLanguage, "en")

def getInfo(key : str):
    return info[key].get(chosenLanguage, "en")

def getGenders():
    return genders.get(chosenLanguage, "en")

def getAbility(key : str):
    return abilities[key].get(chosenLanguage, "en")
