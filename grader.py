def grade_easy(action, score):
    if score >= 20 and action == "TREAT_NOW":
        return 1.0
    elif action == "MONITOR":
        return 0.5
    return 0.0


def grade_medium(action, score):
    if score >= 20 and action == "TREAT_NOW":
        return 1.0
    elif 10 <= score < 20 and action == "MONITOR":
        return 0.7
    elif action == "WAIT":
        return 0.3
    return 0.0

def grade_hard(action, score):
    if score >= 25 and action == "TREAT_NOW":
        return 1.0
    elif 15 <= score < 25 and action == "MONITOR":
        return 0.7
    elif score < 15 and action == "WAIT":
        return 0.5
    else:
        return 0.0