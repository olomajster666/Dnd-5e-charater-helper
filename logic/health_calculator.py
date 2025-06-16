from utils.json_loader import load_json
from .modifier_calculator import calculate_modifier

def calculate_health(class_id, con_score, classes=None):
    if classes is None:
        classes = {cls["id"]: cls for cls in load_json("classes.json")}
    class_data = classes.get(class_id, {"hit_die": 6})
    con_modifier = int(calculate_modifier(con_score).replace("+", ""))  # Convert to int for calculation
    return class_data["hit_die"] + con_modifier
