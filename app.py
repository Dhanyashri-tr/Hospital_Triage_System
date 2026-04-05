import gradio as gr
from inference import triage_system


def predict(heart_rate, oxygen, temperature, pain_level):
    score, decision, explanation = triage_system(
        heart_rate, oxygen, temperature, pain_level
    )

    return (
        f"{score}",
        decision,
        explanation
    )


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏥 AI Hospital Triage System")
    gr.Markdown("### Smart patient prioritization using vital signs")

    with gr.Row():
        heart_rate = gr.Number(label="Heart Rate (bpm)", value=80)
        oxygen = gr.Number(label="Oxygen Level (%)", value=98)
        temperature = gr.Number(label="Temperature (°C)", value=36.5)
        pain_level = gr.Slider(1, 10, value=3, label="Pain Level")

    analyze_btn = gr.Button("🔍 Analyze Patient")

    score_output = gr.Textbox(label="Priority Score")
    decision_output = gr.Textbox(label="Decision")
    explanation_output = gr.Textbox(label="AI Explanation")

    analyze_btn.click(
        fn=predict,
        inputs=[heart_rate, oxygen, temperature, pain_level],
        outputs=[score_output, decision_output, explanation_output]
    )

    gr.Markdown("### 🚦 Decision Levels")
    gr.Markdown("""
    - 🚨 **TREAT NOW** → Immediate emergency care  
    - ⚠️ **MONITOR** → Needs observation  
    - 🕒 **WAIT** → Stable condition  
    """)

demo.launch()