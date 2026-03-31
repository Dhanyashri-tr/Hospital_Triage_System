import gradio as gr
from env import HospitalEnv

env = HospitalEnv()

def simulate(severity, waiting_time, age, resources, condition):
    state = env.reset()

    # override values
    state["severity"] = severity
    state["waiting_time"] = waiting_time
    state["age"] = age
    state["resources_available"] = resources
    state["condition"] = condition

    action = smart_agent(state)
    next_state, reward, done = env.step(action)

    return f"""
  Patient Summary:
- Severity: {state["severity"]}
- Waiting Time: {state["waiting_time"]} minutes
- Age: {state["age"]}
- Condition: {state["condition"]}

    Decision: {action}
    Reward: {reward}

    Reason:
{explain_decision(state)}
"""

def smart_agent(state):
    if state["severity"] > 8:
        return "treat_now"
    
    elif state["condition"] in ["cardiac", "accident", "stroke"]:
        return "treat_now"
    
    elif state["age"] > 65 and state["severity"] > 5:
        return "treat_now"
    
    elif state["waiting_time"] > 30:
        return "treat_now"
    
    else:
        return "wait"

def explain_decision(state):
    if state["severity"] > 8:
        return "Critical condition → immediate treatment required"
    
    elif state["condition"] in ["cardiac", "accident", "stroke"]:
        return "High-risk condition → prioritized treatment"
    
    elif state["age"] > 65 and state["severity"] > 5:
        return "Elderly patient with risk → prioritized"
    
    elif state["waiting_time"] > 30:
        return "Long waiting time → prioritized"
    
    else:
        return "Stable condition → safe to wait"

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