import utils.json_loader as jl

chosenLanguage = jl.loadLanguageOptions()

# to avoid loading one json multiple times
backgrounds = jl.load_json("backgrounds.json")
classes = jl.load_json("classes.json")
proficiencies = jl.load_json("proficiencies.json")
races = jl.load_json("races.json")
spells = jl.load_json("spells.json")
genders = jl.load_json("genders.json")

# only for translations
gender_names = jl.load_json("lang/gender_names.json")
info = jl.load_json("lang/info.json")
languages = jl.load_json("lang/languages.json")
abilities = jl.load_json("lang/abilities.json")
items = jl.load_json("lang/items.json")
spell_names = jl.load_json("lang/spell_names.json")


def getFromDict(d : dict):
    if(not d.keys().__contains__("en")):
        raise KeyError
    return d.get(chosenLanguage, d.get("en"))

def getInfo(key : str):
    return info[key].get(chosenLanguage, info[key].get("en"))

def getGender(id : str):
    return gender_names.get(id).get(chosenLanguage, gender_names.get(id).get("en"))

def getAbility(key : str):
    return abilities[key].get(chosenLanguage, abilities[key].get("en"))

def getItem(key : str):
    return items[key].get(chosenLanguage, items[key].get("en"))

def getItemCountAndName(item : dict):
    if(item['count'] < 1):
        return ""

    text : str = ""
    if(item['count'] > 1):
        text += str(item['count']) + "x "

    return text + getItem(item['id'])

def getSpellName(id : str):
    return spell_names[id].get("name").get(chosenLanguage, spell_names[id].get("en"))

def getSpellDescription(id : str):
    return spell_names[id].get("description").get(chosenLanguage, spell_names[id].get("en"))
