def easy_task(state):
    return state["severity"]


def medium_task(state):
    return state["severity"] + state["waiting_time"] * 0.2


def hard_task(state):
    score = state["severity"] * 2
    score += state["waiting_time"] * 0.3
    score -= state["resources_available"] * 2
    return score