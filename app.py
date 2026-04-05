"""
Hospital Triage System - Gradio UI for Hugging Face Spaces
Clean, working interface with exact triage logic
"""

import gradio as gr

def calculate_triage_score(heart_rate, oxygen_sat, pain_level):
    """Calculate triage score using exact formula: score = heart_rate/10 + (100 - oxygen) + pain*2"""
    
    # Exact scoring formula as specified
    score = (heart_rate / 10) + (100 - oxygen_sat) + (pain_level * 2)
    
    # Determine triage action based on score thresholds
    if score >= 25:
        action = "TREAT NOW"
        triage_level = "RED"
        explanation = f"Critical condition detected (score: {score:.1f}). Immediate treatment required."
    elif score >= 15:
        action = "MONITOR"
        triage_level = "YELLOW"
        explanation = f"Moderate condition (score: {score:.1f}). Close monitoring required."
    else:
        action = "WAIT"
        triage_level = "GREEN"
        explanation = f"Stable condition (score: {score:.1f}). Can wait for treatment."
    
    return score, triage_level, action, explanation

def triage_assessment(heart_rate, oxygen_sat, pain_level):
    """Main triage function for Gradio"""
    try:
        # Validate inputs
        if heart_rate is None or oxygen_sat is None or pain_level is None:
            return "❌ Please fill in all fields", "", "", ""
        
        # Calculate triage using exact formula
        score, triage_level, action, explanation = calculate_triage_score(
            heart_rate, oxygen_sat, pain_level
        )
        
        # Format result
        result = f"""
🏥 **Triage Assessment Complete**

**Patient Score:** {score:.1f}
**Triage Level:** {triage_level}
**Recommended Action:** {action}

**Explanation:** {explanation}

**Formula Used:** score = (heart_rate/10) + (100 - oxygen) + (pain*2)

---
*This is an AI assessment tool. Always consult with medical professionals for actual patient care.*
        """.strip()
        
        return result, f"{score:.1f}", triage_level, action
    
    except Exception as e:
        return f"❌ Error: {str(e)}", "", "", ""

# Create Gradio interface
with gr.Blocks(title="🏥 Hospital Triage System", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🏥 Hospital Triage System
    
    **AI-Powered Patient Priority Assessment**
    
    Enter patient vitals below to get triage recommendation using the scoring formula:
    **score = (heart_rate/10) + (100 - oxygen) + (pain*2)**
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
                lines=14,
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
    
    # Scoring explanation
    gr.Markdown("""
    ### 📊 Scoring Logic
    
    **Formula:** `score = (heart_rate/10) + (100 - oxygen) + (pain*2)`
    
    **Decision Thresholds:**
    - **Score ≥ 25**: 🚨 **TREAT NOW** (Critical - RED)
    - **Score ≥ 15**: 👁️ **MONITOR** (Moderate - YELLOW)
    - **Score < 15**: ⏰ **WAIT** (Stable - GREEN)
    
    ### 🧪 Example Cases
    
    | Case | Heart Rate | Oxygen | Pain | Score | Result |
    |-------|-------------|---------|-------|-------|--------|
    | Critical | 110 | 88 | 8 | 110/10 + 12 + 16 = 39 | 🚨 TREAT NOW |
    | Moderate | 85 | 95 | 4 | 8.5 + 5 + 8 = 21.5 | 👁️ MONITOR |
    | Stable | 70 | 98 | 2 | 7 + 2 + 4 = 13 | ⏰ WAIT |
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
