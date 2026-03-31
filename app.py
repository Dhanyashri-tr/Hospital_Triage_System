import gradio as gr
from env import HospitalEnv

env = HospitalEnv()

def simulate(severity, waiting_time, age, resources, condition):
    state = {
        "severity": severity,
        "waiting_time": waiting_time,
        "age": age,
        "resources_available": resources,
        "condition": condition
    }

    action = smart_agent(state)
    next_state, reward, done = env.step(action)

    return f"""
Action: {action}
Reward: {reward}
Decision: {explain_decision(state)}
"""

def smart_agent(state):
    if state["severity"] > 7:
        return "treat_now"
    elif state["waiting_time"] > 30:
        return "treat_now"
    else:
        return "wait"

def explain_decision(state):
    if state["severity"] > 7:
        return "Critical patient → immediate treatment"
    elif state["waiting_time"] > 30:
        return "Waited too long → prioritize"
    else:
        return "Stable → can wait"

interface = gr.Interface(
    fn=simulate,
    inputs=[
        gr.Slider(0, 10, label="Severity"),
        gr.Slider(0, 60, label="Waiting Time (minutes)"),
        gr.Slider(0, 100, label="Age"),
        gr.Slider(0, 5, label="Resources Available"),
        gr.Textbox(label="Condition (fever/injury/etc)")
    ],
    outputs="text",
    title="🏥 Hospital Triage AI System"
)

interface.launch()