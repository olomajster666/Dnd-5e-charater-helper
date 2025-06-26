class CharacterState:

    __defaultData = {
        "name": "",
        "gender": "",
        "race": None,
        "class": None,
        "background": None,
        "stats": {
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0
        },
        "proficiencies": [],
        "spells": [],
        "equipment": [],
        "level": 1,
        "image": None
    }
    def __init__(self, data : dict = __defaultData):
        self.data = data

    def set(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)

    def update(self, updates: dict):
        self.data.update(updates)