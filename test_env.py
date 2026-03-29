from env import HospitalEnv

env = HospitalEnv()

for task in ["easy", "medium", "hard"]:
    print(f"\n--- Testing {task.upper()} ---")
    state = env.reset(task=task)
    print("State:", state)

    action = "treat_now"
    _, reward, _ = env.step(action)
    print("Reward:", reward)