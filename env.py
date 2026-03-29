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

    def step(self, action):
        s = self.state_data
        reward = 0

        # EASY TASK
        if self.task == "easy":
            if action == "treat_now" and s["severity"] >= 7:
                reward = 10
            else:
                reward = -5

        # MEDIUM TASK
        elif self.task == "medium":
            if action == "treat_now" and s["severity"] >= 7:
                reward = 10
            elif action == "refer" and s["resources_available"] == 0:
                reward = 6
            else:
                reward = -5

        # HARD TASK (BEST FOR JUDGES)
        elif self.task == "hard":
            if action == "treat_now":
                if s["severity"] >= 8:
                    reward = 10
                elif s["severity"] >= 5:
                    reward = 5
                else:
                    reward = -6

            elif action == "delay":
                if s["severity"] < 4:
                    reward = 6
                else:
                    reward = -8

            elif action == "refer":
                if s["resources_available"] == 0:
                    reward = 7
                else:
                    reward = -3

            # penalty for long wait
            if s["waiting_time"] > 40:
                reward -= 3

        done = True
        return s, reward, done