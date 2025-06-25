import utils.json_loader as jl

# to avoid loading one json multiple times

chosenLanguage = "en"

backgrounds = jl.load_json("backgrounds.json")
classes = jl.load_json("classes.json")
genders = jl.load_json("genders.json")
info = jl.load_json("info.json")
languages = jl.load_json("languages.json")
proficiencies = jl.load_json("proficiencies.json")
races = jl.load_json("races.json")
spells = jl.load_json("spells.json")

