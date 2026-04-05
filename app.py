"""
Hospital Triage System - Gradio UI for Hugging Face Spaces
Simple, working interface for patient triage
"""

import gradio as gr
import numpy as np

def calculate_triage_score(heart_rate, oxygen_sat, pain_level):
    """Calculate triage score and determine action"""
    # Simple scoring algorithm
    score = 0
    
    # Heart rate scoring
    if heart_rate < 40 or heart_rate > 130:
        score += 20
    elif heart_rate < 50 or heart_rate > 120:
        score += 15
    elif heart_rate > 100:
        score += 10
    elif heart_rate > 90:
        score += 5
    
    # Oxygen saturation scoring
    if oxygen_sat < 85:
        score += 30
    elif oxygen_sat < 90:
        score += 20
    elif oxygen_sat < 95:
        score += 10
    
    # Pain level scoring
    score += pain_level * 10  # Pain level 1-10, scaled to 10-100
    
    # Normalize to 0-100
    final_score = min(100, score)
    
    # Determine triage action
    if final_score >= 25:
        action = "TREAT_NOW"
        triage_level = "RED"
        explanation = f"Critical condition detected (score: {final_score}). Immediate treatment required."
    elif final_score >= 15:
        action = "MONITOR"
        triage_level = "YELLOW"
        explanation = f"Moderate condition (score: {final_score}). Close monitoring required."
    else:
        action = "WAIT"
        triage_level = "GREEN"
        explanation = f"Stable condition (score: {final_score}). Can wait for treatment."
    
    return final_score, triage_level, action, explanation

def triage_assessment(heart_rate, oxygen_sat, pain_level):
    """Main triage function for Gradio"""
    try:
        # Validate inputs
        if not all([heart_rate, oxygen_sat, pain_level is not None]):
            return "❌ Please fill in all fields", "", "", ""
        
        # Calculate triage
        score, triage_level, action, explanation = calculate_triage_score(
            heart_rate, oxygen_sat, pain_level
        )
        
        # Format result
        result = f"""
🏥 **Triage Assessment Complete**

**Patient Score:** {score}/100
**Triage Level:** {triage_level}
**Recommended Action:** {action}

**Explanation:** {explanation}

---
*This is an AI assessment tool. Always consult with medical professionals for actual patient care.*
        """.strip()
        
        return result, f"Score: {score}/100", triage_level, action
    
    except Exception as e:
        return f"❌ Error: {str(e)}", "", "", ""

# Create Gradio interface
with gr.Blocks(title="🏥 Hospital Triage System", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🏥 Hospital Triage System
    
    **AI-Powered Patient Priority Assessment**
    
    Enter patient vitals below to get triage recommendation.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            heart_rate = gr.Number(
                label="💓 Heart Rate (bpm)",
                minimum=30,
                maximum=200,
                value=85,
                info="Normal range: 60-100 bpm"
            )
            
            oxygen_sat = gr.Number(
                label="🫁 Oxygen Saturation (%)",
                minimum=70,
                maximum=100,
                value=95,
                info="Normal range: 95-100%"
            )
            
            pain_level = gr.Slider(
                label="😫 Pain Level",
                minimum=0,
                maximum=10,
                value=3,
                step=1,
                info="Rate pain from 0 (no pain) to 10 (severe pain)"
            )
    
    with gr.Row():
        assess_btn = gr.Button(
            "🚀 Assess Patient Priority",
            variant="primary",
            size="lg"
        )
    
    with gr.Row():
        with gr.Column(scale=2):
            full_result = gr.Textbox(
                label="📋 Assessment Result",
                lines=12,
                interactive=False,
                show_copy_button=True
            )
        
        with gr.Column(scale=1):
            score_display = gr.Textbox(
                label="📊 Score",
                interactive=False,
                container=True
            )
            
            triage_display = gr.Textbox(
                label="🚨 Triage Level",
                interactive=False,
                container=True
            )
            
            action_display = gr.Textbox(
                label="⚕️ Recommended Action",
                interactive=False,
                container=True
            )
    
    # Example cases
    gr.Markdown("""
    ### 🧪 Example Cases
    
    | Case | Heart Rate | Oxygen | Pain | Result |
    |-------|-------------|---------|-------|---------|
    | Critical | 110 | 88 | 8 | 🚨 TREAT_NOW |
    | Moderate | 85 | 95 | 4 | 👁️ MONITOR |
    | Stable | 70 | 98 | 2 | ⏰ WAIT |
    """)
    
    # Connect the function
    assess_btn.click(
        fn=triage_assessment,
        inputs=[heart_rate, oxygen_sat, pain_level],
        outputs=[full_result, score_display, triage_display, action_display]
    )
    
    # Footer
    gr.Markdown("""
    ---
    **⚠️ Medical Disclaimer:** This is an AI demonstration tool for educational purposes only. 
    Always consult qualified healthcare professionals for actual medical decisions.
    
    **🏆 Built for:** Meta PyTorch OpenEnv Hackathon
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
