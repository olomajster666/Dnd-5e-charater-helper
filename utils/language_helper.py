import utils.json_loader as jl


chosenLanguage = jl.loadLanguageOptions()

# only for translations
gender_names = jl.load_json("lang/gender_names.json")
info = jl.load_json("lang/info.json")
language_names = jl.load_json("lang/language_names.json")
abilities = jl.load_json("lang/abilities.json")
items = jl.load_json("lang/items.json")
spell_names = jl.load_json("lang/spell_names.json")
background_names = jl.load_json("lang/background_names.json")
features = jl.load_json("lang/features.json")


def getTranslation(d : dict):
    if(not d.keys().__contains__("en")):
        raise KeyError
    return d.get(chosenLanguage, d.get("en"))

def getDescription(d : dict):
    return getTranslation(d.get("description"))

def getName(d : dict):
    return getTranslation(d.get("name"))

def getLanguageName(id : str):
    return language_names.get(id, "Unknown")

def getInfo(key : str):
    return getTranslation(info[key])

def getGender(id : str):
    return getTranslation(gender_names[id])

def getAbility(key : str):
    return getTranslation(abilities[key])

def getItem(key : str):
    return getTranslation(items[key])

def getItemCountAndName(item : dict):
    if(item['count'] < 1):
        return ""

    text : str = ""
    if(item['count'] > 1):
        text += str(item['count']) + "x "

    return text + getItem(item['id'])

def getSpellName(id : str):
    return getName(spell_names[id])

def getSpellDescription(id : str):
    return getDescription(spell_names[id])

def getBackgroundName(id : str):
    return getName(background_names[id])

def getBackgroundDescription(id : str):
    return getDescription(background_names[id])

def getFeatureName(id : str):
    return getName(features[id])

def getFeatureDescription(id : str):
    return getDescription(features[id])
