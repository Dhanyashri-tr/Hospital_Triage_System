import gradio as gr

def triage(heart_rate, oxygen, pain):
    score = heart_rate/10 + (100 - oxygen) + pain*2

    if score >= 25:
        return f"🚨 TREAT NOW (Score: {score:.2f})"
    elif score >= 15:
        return f"⚠️ MONITOR (Score: {score:.2f})"
    else:
        return f"🟢 WAIT (Score: {score:.2f})"

with gr.Blocks() as demo:
    gr.Markdown("# 🏥 AI Hospital Triage System")

    hr = gr.Slider(40, 180, label="Heart Rate")
    oxy = gr.Slider(70, 100, label="Oxygen Level")
    pain = gr.Slider(0, 10, label="Pain Level")

    output = gr.Textbox(label="Decision")

    btn = gr.Button("Analyze")
    btn.click(triage, inputs=[hr, oxy, pain], outputs=output)

demo.launch()