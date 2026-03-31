import gradio as gr
from env import HospitalEnv

env = HospitalEnv()

def simulate(name, severity, waiting_time, age, resources, condition):
    state = env.reset()

    # override values
    state["severity"] = severity
    state["waiting_time"] = waiting_time
    state["age"] = age
    state["resources_available"] = resources
    state["condition"] = condition
    priority_score = (
    state["severity"] * 2 +
    state["waiting_time"] * 0.5 +
    (10 if state["condition"] in ["cardiac", "stroke"] else 0)
    )
    priority_score = round(priority_score, 2)
    if state["condition"] == "cardiac":
         emoji = "❤️"
    elif state["condition"] == "stroke":
         emoji = "🧠"
    else:
         emoji = "🩺"
    action = smart_agent(state)
    next_state, reward, done = env.step(action)

    return f"""
    <h2>👤 Patient: {name}</h2>
    <h2>Patient Summary</h2>

    <ul>
    <li><b>Severity:</b> {state["severity"]}</li>
    <li><b>Waiting Time:</b> {state["waiting_time"]} minutes</li>
    <li><b>Age:</b> {state["age"]}</li>
    <li><b>Condition:</b> {emoji} {state["condition"]}</li>
    </ul>

    <h3 style="color:purple;"> Priority Score: {priority_score}</h3>

    <h3 style="color:{'red' if action=='treat_now' else 'green'};">
    Decision: {action.upper()}
    </h3>

    <p><b>Reward:</b> {reward}</p>

    <p><b>Reason:</b> {explain_decision(state)}</p>
    """

def smart_agent(state):
    if state["severity"] >= 9:
        return "treat_now"
    
    elif state["condition"] in ["cardiac", "stroke", "accident"]:
        return "treat_now"
    
    elif state["age"] > 65 and state["severity"] > 5:
        return "treat_now"
    
    elif state["resources_available"] == 0:
        return "wait"
    
    elif state["waiting_time"] > 30:
        return "treat_now"
    
    else:
        return "wait"

def explain_decision(state):
    if state["severity"] >= 9:
        return "Critical severity → immediate treatment required"
    
    elif state["condition"] in ["cardiac", "stroke", "accident"]:
        return "Life-threatening condition → prioritized treatment"
    
    elif state["age"] > 65 and state["severity"] > 5:
        return "Elderly patient with moderate risk → prioritized"
    
    elif state["resources_available"] == 0:
        return "No resources available → patient must wait"
    
    elif state["waiting_time"] > 30:
        return "Patient waited too long → prioritized"
    
    else:
        return "Stable condition → safe to wait"

interface = gr.Interface(
    fn=simulate,
    inputs=[
        gr.Textbox(label="Patient Name"),
        gr.Slider(0, 10, label="Severity"),
        gr.Slider(0, 60, label="Waiting Time (minutes)"),
        gr.Slider(0, 100, label="Age"),
        gr.Slider(0, 5, label="Resources Available"),
        gr.Textbox(label="Condition (fever/injury/etc)")
    ],
    outputs=gr.HTML(),
    title="🏥 Hospital Triage AI System",
    description="AI-powered patient prioritization system with explainable decisions"
)

interface.launch()