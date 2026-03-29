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
