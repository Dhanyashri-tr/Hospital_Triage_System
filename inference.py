"""
Inference script for Hospital Triage System
Demo script for testing API
"""

import requests
import json
import time

def test_api():
    """Test the Hospital Triage API"""
    base_url = "http://localhost:7860"
    
    print("🏥 Hospital Triage System - API Test")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    print("\n" + "=" * 50)
    
    # Test prediction endpoint
    test_patients = [
        {
            "patient": {
                "patient_id": "P1001",
                "vitals": {
                    "heart_rate": 85,
                    "oxygen_saturation": 92,
                    "temperature": 37.5,
                    "systolic_bp": 120,
                    "age": 45
                },
                "symptoms": ["chest_pain", "shortness_breath"],
                "waiting_time": 5
            }
        },
        {
            "patient": {
                "patient_id": "P1002",
                "vitals": {
                    "heart_rate": 70,
                    "oxygen_saturation": 98,
                    "temperature": 37.0,
                    "systolic_bp": 110,
                    "age": 25
                },
                "symptoms": ["headache"],
                "waiting_time": 15
            }
        },
        {
            "patient": {
                "patient_id": "P1003",
                "vitals": {
                    "heart_rate": 110,
                    "oxygen_saturation": 88,
                    "temperature": 38.8,
                    "systolic_bp": 145,
                    "age": 75
                },
                "symptoms": ["confusion", "fainting"],
                "waiting_time": 0
            }
        }
    ]
    
    for i, patient_data in enumerate(test_patients, 1):
        print(f"\n🧪 Test Patient {i}: {patient_data['patient']['patient_id']}")
        print("-" * 30)
        
        try:
            response = requests.post(
                f"{base_url}/predict",
                json=patient_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Prediction successful")
                print(f"Patient ID: {result['patient_id']}")
                print(f"Triage Level: {result['triage_level']}")
                print(f"Severity Score: {result['severity_score']}")
                print(f"Recommended Action: {result['recommended_action']}")
                print(f"Priority Score: {result['priority_score']}")
                print(f"Explanation: {result['explanation']}")
            else:
                print(f"❌ Prediction failed: {response.status_code}")
                print(f"Error: {response.text}")
        
        except Exception as e:
            print(f"❌ Prediction error: {e}")
        
        if i < len(test_patients):
            print("⏳ Waiting 2 seconds...")
            time.sleep(2)
    
    print("\n" + "=" * 50)
    print("🎯 API Test Complete!")

if __name__ == "__main__":
    test_api()
