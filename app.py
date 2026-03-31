from fastapi import FastAPI
from env import HospitalEnv

app = FastAPI()
env = HospitalEnv()

@app.get("/")
def home():
    return {"message": "Hospital Triage Env Running"}

@app.get("/reset")
def reset():
    state = env.reset(task="easy")
    return state

@app.get("/step")
def step(action: str = "treat_now"):
    state, reward, done = env.step(action)
    return {
        "state": state,
        "reward": reward,
        "done": done
    }
@app.get("/simulate")
def simulate():
    state = env.reset()
    action = "treat_now"
    next_state, reward, done = env.step(action)

    return {
    "initial_state": state,
    "action_taken": action,
    "next_state": next_state,
    "reward": reward,
    "done": done,
    "reason": explain_decision(state)
}
def smart_agent(state):
    if state["severity"] > 7:
        return "treat_now"
    elif state["waiting_time"] > 30:
        return "treat_now"
    else:
        return "wait"
def explain_decision(state):
    if state["severity"] > 7:
        return "Critical patient - requires immediate treatment"
    elif state["waiting_time"] > 30:
        return "Patient has been waiting too long - prioritize treatment"
    else:
        return "Patient is stable - can safely wait"
