import utils.json_loader as jl


chosenLanguage = jl.loadLanguageOptions()

# only for translations
gender_names = jl.load_json("lang/gender_names.json")
info = jl.load_json("lang/info.json")
language_names = jl.load_json("lang/language_names.json")
abilities = jl.load_json("lang/abilities.json")
items = jl.load_json("lang/items.json")
spell_names = jl.load_json("lang/spell_names.json")


def getFromDict(d : dict):
    if(not d.keys().__contains__("en")):
        raise KeyError
    return d.get(chosenLanguage, d.get("en"))

def getLanguageName(id : str):
    return language_names.get(id, "Unknown")

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
