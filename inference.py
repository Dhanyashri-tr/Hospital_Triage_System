from env import HospitalEnv
from grader import grade_easy, grade_medium, grade_hard

def smart_agent(state):
    if state["severity"] >= 8:
        return "treat_now"
    elif state["resources_available"] == 0:
        return "refer"
    elif state["severity"] < 4:
        return "delay"
    else:
        return "treat_now"

env = HospitalEnv()

scores = {}

for task in ["easy", "medium", "hard"]:
    total_score = 0

    for _ in range(10):
        state = env.reset(task=task)
        action = smart_agent(state)

        if task == "easy":
            score = grade_easy(state, action)
        elif task == "medium":
            score = grade_medium(state, action)
        else:
            score = grade_hard(state, action)

        total_score += score

    scores[task] = total_score

print("Scores:", scores)
print("Final Score:", sum(scores.values()))