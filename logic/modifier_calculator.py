def calculate_modifier(score):
    if score == 1:
        return "-5"
    elif 2 <= score <= 3:
        return "-4"
    elif 4 <= score <= 5:
        return "-3"
    elif 6 <= score <= 7:
        return "-2"
    elif 8 <= score <= 9:
        return "-1"
    elif 10 <= score <= 11:
        return "+0"
    elif 12 <= score <= 13:
        return "+1"
    elif 14 <= score <= 15:
        return "+2"
    elif 16 <= score <= 17:
        return "+3"
    elif 18 <= score <= 19:
        return "+4"
    elif 20 <= score <= 21:
        return "+5"
    elif 22 <= score <= 23:
        return "+6"
    elif 24 <= score <= 25:
        return "+7"
    elif 26 <= score <= 27:
        return "+8"
    elif 28 <= score <= 29:
        return "+9"
    else:  # 30+
        return "+10"