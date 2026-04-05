"""
Simple Gradio UI for Hospital Triage Environment
Bonus feature for hackathon demonstration
"""

import gradio as gr
import requests
import json
from typing import Dict, Any, Tuple


class TriageUI:
    """Gradio interface for hospital triage environment"""
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.current_episode = None
        self.current_patient = None
    
    def reset_environment(self, difficulty: str) -> Tuple[str, str, str]:
        """Reset environment and return patient info"""
        try:
            response = requests.post(f"{self.api_url}/reset", json={"difficulty": difficulty})
            if response.status_code == 200:
                data = response.json()
                self.current_episode = data["state"]["episode_id"]
                self.current_patient = data["observation"]["patient"]
                
                # Format patient info
                patient = self.current_patient
                vitals = patient["vitals"]
                symptoms = [s.replace("_", " ").title() for s in patient["symptoms"]]
                
                patient_info = f"""
**Patient ID:** {patient['patient_id']}
**Triage Level:** {patient['triage_level']}
**Severity Score:** {patient['severity_score']}/100

**Vitals:**
• Heart Rate: {vitals['heart_rate']} bpm
• Oxygen Saturation: {vitals['oxygen_saturation']}%
• Temperature: {vitals['temperature']}°C
• Blood Pressure: {vitals['systolic_bp']} mmHg
• Age: {vitals['age']} years

**Symptoms:** {', '.join(symptoms) if symptoms else 'None'}
**Waiting Time:** {patient['waiting_time']} minutes
                """.strip()
                
                resources = data["observation"]["available_resources"]
                resource_info = f"""
**Available Resources:**
• ICU Beds: {resources['icu_beds']}
• General Beds: {resources['general_beds']}
• Doctors: {resources['doctors']}
• Nurses: {resources['nurses']}
                """.strip()
                
                return patient_info, resource_info, f"✅ Environment reset - Episode {self.current_episode[:8]}..."
            else:
                return "❌ Error resetting environment", "", "Failed to connect to API"
        except Exception as e:
            return f"❌ Connection Error: {str(e)}", "", "Make sure API server is running"
    
    def take_action(self, action: str) -> Tuple[str, str, str]:
        """Execute action and return results"""
        if not self.current_episode:
            return "❌ Please reset environment first", "", ""
        
        try:
            response = requests.post(f"{self.api_url}/step", json={"action": action})
            if response.status_code == 200:
                data = response.json()
                
                # Format results
                reward = data["reward"]
                explanation = data["info"].get("reward_explanation", "No explanation available")
                performance = data["info"].get("performance", {})
                
                result_info = f"""
**Action Taken:** {action}
**Reward:** {reward:.2f}/1.0
**Episode Done:** {data['done']}

**Explanation:** {explanation}

**Performance:**
• Accuracy: {performance.get('accuracy', 0):.2%}
• Total Decisions: {performance.get('total_decisions', 0)}
• Correct Decisions: {performance.get('correct_decisions', 0)}
                """.strip()
                
                # Get final performance
                perf_response = requests.get(f"{self.api_url}/performance")
                if perf_response.status_code == 200:
                    perf_data = perf_response.json()
                    summary = f"""
**Episode Summary:**
• Total Reward: {perf_data['total_reward']:.2f}
• Accuracy: {perf_data['accuracy']:.2%}
• Difficulty: {perf_data['difficulty']}
• Steps: {perf_data['steps']}
                    """.strip()
                else:
                    summary = "Performance data unavailable"
                
                return result_info, summary, f"✅ Action completed - Reward: {reward:.2f}"
            else:
                return f"❌ Error: {response.text}", "", "Action failed"
        except Exception as e:
            return f"❌ Connection Error: {str(e)}", "", "Make sure API server is running"
    
    def get_environment_info(self) -> str:
        """Get environment information"""
        try:
            response = requests.get(f"{self.api_url}/info")
            if response.status_code == 200:
                info = response.json()
                return f"""
**Environment:** {info['name']}
**Version:** {info['version']}
**Actions:** {', '.join(info['actions'])}
**Difficulty Levels:** {', '.join(info['difficulty_levels'])}
**Reward Range:** {info['reward_range'][0]} - {info['reward_range'][1]}
**Max Steps:** {info['max_episode_steps']}

**Description:** {info['description']}
                """.strip()
            else:
                return "❌ Could not fetch environment info"
        except Exception as e:
            return f"❌ Connection Error: {str(e)}"


def create_ui():
    """Create Gradio interface"""
    ui = TriageUI()
    
    with gr.Blocks(title="Hospital Triage Environment", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🏥 Hospital Triage Environment")
        gr.Markdown("### OpenEnv-Compatible AI Triage Decision System")
        
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("## 🎮 Environment Controls")
                
                with gr.Row():
                    difficulty = gr.Dropdown(
                        choices=["easy", "medium", "hard"],
                        value="medium",
                        label="Difficulty Level"
                    )
                    reset_btn = gr.Button("🔄 Reset Environment", variant="primary")
                
                gr.Markdown("## 🤖 Decision Making")
                
                with gr.Row():
                    treat_btn = gr.Button("🚨 TREAT_NOW", variant="stop", size="lg")
                    monitor_btn = gr.Button("👁️ MONITOR", variant="secondary", size="lg")
                    wait_btn = gr.Button("⏰ WAIT", variant="secondary", size="lg")
                
                status = gr.Textbox(label="Status", interactive=False)
            
            with gr.Column(scale=3):
                gr.Markdown("## 📊 Patient Information")
                patient_info = gr.Textbox(
                    label="Current Patient",
                    lines=12,
                    interactive=False,
                    value="Reset environment to see patient data..."
                )
                
                gr.Markdown("## 🏥 Resource Status")
                resource_info = gr.Textbox(
                    label="Available Resources",
                    lines=6,
                    interactive=False,
                    value="Reset environment to see resources..."
                )
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("## 📈 Action Results")
                action_results = gr.Textbox(
                    label="Results",
                    lines=10,
                    interactive=False
                )
            
            with gr.Column():
                gr.Markdown("## 📋 Performance Summary")
                performance_summary = gr.Textbox(
                    label="Performance",
                    lines=10,
                    interactive=False
                )
        
        with gr.Row():
            gr.Markdown("## ℹ️ Environment Information")
            env_info = gr.Textbox(
                label="Environment Details",
                lines=8,
                interactive=False,
                value="Loading..."
            )
        
        # Event handlers
        reset_btn.click(
            fn=ui.reset_environment,
            inputs=[difficulty],
            outputs=[patient_info, resource_info, status]
        )
        
        treat_btn.click(
            fn=ui.take_action,
            inputs=[gr.Textbox(value="TREAT_NOW", visible=False)],
            outputs=[action_results, performance_summary, status]
        )
        
        monitor_btn.click(
            fn=ui.take_action,
            inputs=[gr.Textbox(value="MONITOR", visible=False)],
            outputs=[action_results, performance_summary, status]
        )
        
        wait_btn.click(
            fn=ui.take_action,
            inputs=[gr.Textbox(value="WAIT", visible=False)],
            outputs=[action_results, performance_summary, status]
        )
        
        # Load environment info on start
        demo.load(
            fn=ui.get_environment_info,
            outputs=[env_info]
        )
        
        gr.Markdown("""
        ## 🎯 How to Use
        1. **Select Difficulty** - Choose easy, medium, or hard
        2. **Reset Environment** - Initialize new patient case
        3. **Review Patient** - Check vitals, symptoms, and severity
        4. **Make Decision** - Choose TREAT_NOW, MONITOR, or WAIT
        5. **View Results** - See reward and performance metrics
        
        ## 🏆 Scoring
        - **Correct critical decision** → +1.0 reward
        - **Correct moderate decision** → +0.8 reward  
        - **Correct low priority** → +0.6 reward
        - **Slightly incorrect** → +0.5 reward
        - **Dangerous wrong decision** → +0.0 reward
        """)
    
    return demo


if __name__ == "__main__":
    demo = create_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
