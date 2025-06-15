def get_final_stat(state, ability):
    base = state.get("stats").get(ability, 0)
    bonuses = state.get("race", {}).get("ability_bonuses", {}).get(ability, 0)
    return base + bonuses