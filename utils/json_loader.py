import json
import os

def load_json(filename):
    path = os.path.join("data", filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)
