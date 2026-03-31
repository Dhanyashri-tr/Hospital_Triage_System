import random

class HospitalEnv:
    def __init__(self):
        self.state_data = None
        self.task = "easy"

    def reset(self, task="easy"):
        self.task = task

        self.state_data = {
            "severity": random.randint(1, 10),
            "waiting_time": random.randint(1, 60),
            "age": random.randint(1, 90),
            "resources_available": random.choice([0, 1]),
            "condition": random.choice(["cardiac", "injury", "fever"])
        }
        return self.state_data

    def state(self):
        return self.state_data

    def step(self, action, priority_score):

        s = self.state_data  # current state

        # Reward logic
        if priority_score >= 25 and action == "TREAT_NOW":
            reward = 10

        elif 15 <= priority_score < 25 and action == "MONITOR":
            reward = 5

        elif priority_score < 15 and action == "WAIT":
            reward = 2

        else:
            reward = -5

        # penalty for long wait
        if s["waiting_time"] > 40:
            reward -= 3

        done = True

        return s, reward, done

