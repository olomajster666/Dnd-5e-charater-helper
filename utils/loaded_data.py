import utils.json_loader as jl

# to avoid loading one json multiple times
backgrounds = jl.load_json("backgrounds.json")
classes = jl.load_json("classes.json")
proficiencies = jl.load_json("proficiencies.json")
races = jl.load_json("races.json")
spells = jl.load_json("spells.json")
genders = jl.load_json("genders.json")
languages = jl.load_json("languages.json")