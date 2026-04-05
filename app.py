import gradio as gr

def triage_assessment(heart_rate, oxygen_level, pain_level):
    """
    AI Hospital Triage System Assessment
    Formula: score = heart_rate/10 + (100 - oxygen) + pain*2
    """
    try:
        # Calculate triage score using exact formula
        score = heart_rate/10 + (100 - oxygen_level) + (pain_level * 2)
        
        # Determine triage decision based on score
        if score >= 25:
            decision = "🚨 TREAT NOW"
            priority = "CRITICAL"
            color = "red"
        elif score >= 15:
            decision = "⚠️ MONITOR"
            priority = "MODERATE"
            color = "orange"
        else:
            decision = "🟢 WAIT"
            priority = "LOW"
            color = "green"
        
        # Format result
        result = f"""
## 🏥 Triage Assessment Complete

### **Decision: {decision}**

**Priority Level:** {priority}
**Triage Score:** {score:.2f}/100

### 📊 Assessment Details
- **Heart Rate:** {heart_rate} bpm
- **Oxygen Level:** {oxygen_level}%
- **Pain Level:** {pain_level}/10

### 📈 Scoring Formula
`score = (heart_rate/10) + (100 - oxygen) + (pain*2)`

### ⚕️ Medical Recommendation
{decision.replace("🚨", "").replace("⚠️", "").replace("🟢", "").strip()} - {priority.lower()} priority case requiring immediate attention.

---
*This AI assessment tool is for demonstration purposes only. Always consult qualified healthcare professionals for actual medical decisions.*
        """
        
        return result
    
    except Exception as e:
        return f"❌ Error in assessment: {str(e)}"

# Create Gradio interface with professional design
with gr.Blocks(
    title="AI Hospital Triage System",
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        max-width: 800px !important;
        margin: auto !important;
    }
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    """
) as demo:
    
    # Header
    gr.HTML("""
    <div class="main-header">
        <h1>🏥 AI Hospital Triage System</h1>
        <p><strong>Meta PyTorch OpenEnv Hackathon Project</strong></p>
        <p>AI-Powered Patient Priority Assessment for Emergency Medical Care</p>
    </div>
    """)
    
    # Main content
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📋 Patient Information")
            gr.Markdown("Enter patient vitals to receive triage assessment.")
            
            # Input fields
            heart_rate = gr.Slider(
                minimum=40,
                maximum=180,
                value=80,
                step=1,
                label="💓 Heart Rate (bpm)",
                info="Normal range: 60-100 bpm"
            )
            
            oxygen_level = gr.Slider(
                minimum=70,
                maximum=100,
                value=95,
                step=1,
                label="🫁 Oxygen Level (%)",
                info="Normal range: 95-100%"
            )
            
            pain_level = gr.Slider(
                minimum=0,
                maximum=10,
                value=3,
                step=1,
                label="😫 Pain Level",
                info="Rate pain from 0 (no pain) to 10 (severe pain)"
            )
            
            # Assessment button
            assess_btn = gr.Button(
                "🚀 Run Triage Assessment",
                variant="primary",
                size="lg"
            )
        
        with gr.Column(scale=1):
            gr.Markdown("### 📊 Assessment Results")
            
            # Output display
            result_output = gr.Markdown(
                value="Click 'Run Triage Assessment' to analyze patient priority.",
                label="Triage Results"
            )
    
    # Information section
    with gr.Accordion("📖 How It Works", open=False):
        gr.Markdown("""
        ### 🎯 Scoring Algorithm
        
        The AI system uses a weighted scoring formula to determine patient priority:
        
        **Formula:** `score = (heart_rate/10) + (100 - oxygen) + (pain*2)`
        
        ### 🚨 Decision Thresholds
        
        | Score Range | Decision | Priority | Action |
        |-------------|----------|----------|--------|
        | **≥ 25** | 🚨 TREAT NOW | Critical | Immediate medical attention required |
        | **≥ 15** | ⚠️ MONITOR | Moderate | Close monitoring, may need treatment |
        | **< 15** | 🟢 WAIT | Low | Can wait for treatment |
        
        ### 🧪 Example Cases
        
        - **Critical Case**: HR=120, O2=85, Pain=8 → Score=39 → 🚨 TREAT NOW
        - **Moderate Case**: HR=85, O2=95, Pain=4 → Score=21.5 → ⚠️ MONITOR  
        - **Stable Case**: HR=70, O2=98, Pain=2 → Score=13 → 🟢 WAIT
        """)
    
    # Connect the function
    assess_btn.click(
        fn=triage_assessment,
        inputs=[heart_rate, oxygen_level, pain_level],
        outputs=[result_output]
    )
    
    # Footer
    gr.Markdown("""
    ---
    
    ### ⚠️ Medical Disclaimer
    This AI-powered triage system is designed for **educational demonstration purposes only** as part of the Meta PyTorch OpenEnv Hackathon. 
    
    **Do not use this tool for actual medical decision-making.** Always consult qualified healthcare professionals for real patient assessment and treatment.
    
    ### 🏆 Project Information
    - **Hackathon**: Meta PyTorch OpenEnv Hackathon
    - **Technology**: Python, Gradio, AI/ML
    - **Purpose**: Demonstrate AI applications in healthcare triage
    - **Status**: Educational Prototype
    """)

# Launch the application
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
