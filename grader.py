def grade_easy(state, action):
    if state["severity"] >= 7 and action == "treat_now":
        return 10
    return 0


def grade_medium(state, action):
    if state["severity"] >= 7 and action == "treat_now":
        return 10
    elif state["resources_available"] == 0 and action == "refer":
        return 8
    return 2


def grade_hard(state, action):
    score = 0

    if state["severity"] >= 8 and action == "treat_now":
        score += 5

    if state["resources_available"] == 0 and action == "refer":
        score += 3

    if state["waiting_time"] > 40 and action == "treat_now":
        score += 2

    return score  # max = 10