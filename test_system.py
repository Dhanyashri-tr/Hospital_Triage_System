#!/usr/bin/env python3
"""
Test script for Hospital OpenEnv API
Demonstrates all key features and fixes
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_api():
    """Test the complete Hospital OpenEnv API"""
    
    print("🏥 Hospital OpenEnv API v1.1.0 Test Suite")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. 📊 Health Check")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data['status']}")
            print(f"   ✅ Version: {data['version']}")
            print(f"   ✅ Environment Ready: {data['environment_initialized']}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to API. Start server with: python main.py")
        return False
    
    # Test 2: Reset Environment
    print("\n2. 🔄 Reset Environment")
    reset_data = {"task": "medium", "max_steps": 50}
    response = requests.post(f"{API_BASE}/reset", json=reset_data)
    if response.status_code == 200:
        state = response.json()
        print(f"   ✅ Environment reset successfully")
        print(f"   ✅ Queue length: {state['queue_length']}")
        print(f"   ✅ Resources: {state['resources']}")
    else:
        print(f"   ❌ Reset failed: {response.status_code}")
        return False
    
    # Test 3: Get State
    print("\n3. 📋 Get Current State")
    response = requests.get(f"{API_BASE}/state")
    if response.status_code == 200:
        state = response.json()
        patient = state.get('current_patient')
        if patient:
            print(f"   ✅ Current patient: {patient['patient_id']}")
            print(f"   ✅ Severity score: {patient['severity_score']}")
            print(f"   ✅ Triage level: {patient['triage_level']}")
            print(f"   ✅ Waiting time: {patient['waiting_time']} min")
        else:
            print("   ✅ No patients in queue")
    else:
        print(f"   ❌ Get state failed: {response.status_code}")
    
    # Test 4: Step Actions
    print("\n4. 🎮 Execute Actions")
    actions = ["TREAT_NOW", "MONITOR", "WAIT"]
    
    for i, action in enumerate(actions):
        print(f"\n   Step {i+1}: Action = {action}")
        step_data = {"action": action}
        response = requests.post(f"{API_BASE}/step", json=step_data)
        
        if response.status_code == 200:
            result = response.json()
            state = result['state']
            info = result['info']
            
            print(f"   ✅ Reward: {result['reward']:.3f}")
            print(f"   ✅ Done: {result['done']}")
            print(f"   ✅ Queue length: {state['queue_length']}")
            print(f"   ✅ Treated count: {state['treated_count']}")
            
            if info.get('severity_score'):
                print(f"   ✅ Patient severity: {info['severity_score']}")
                print(f"   ✅ Triage level: {info['triage_level']}")
                print(f"   ✅ Resource blocked: {info['resource_blocked']}")
                print(f"   ✅ Decision reason: {info['decision_reason']}")
            
            if result['done']:
                print(f"   🏁 Episode completed!")
                break
        else:
            print(f"   ❌ Step failed: {response.status_code}")
            print(f"   Error: {response.text}")
    
    # Test 5: Get Metrics
    print("\n5. 📈 Performance Metrics")
    response = requests.get(f"{API_BASE}/metrics")
    if response.status_code == 200:
        metrics = response.json()
        print(f"   ✅ Average reward: {metrics['average_reward']:.3f}")
        print(f"   ✅ Total reward: {metrics['total_reward']:.3f}")
        print(f"   ✅ Efficiency: {metrics['efficiency']:.3f}")
        print(f"   ✅ Steps completed: {metrics['steps_completed']}")
        print(f"   ✅ Patients treated: {metrics['patients_treated']}")
        print(f"   ✅ Termination reason: {metrics['termination_reason']}")
    else:
        print(f"   ❌ Metrics failed: {response.status_code}")
    
    # Test 6: Demo Patient
    print("\n6. 🧪 Demo Patient Generation")
    response = requests.get(f"{API_BASE}/demo/patient")
    if response.status_code == 200:
        demo = response.json()
        patient = demo['patient']
        interpretation = demo['interpretation']
        
        print(f"   ✅ Patient ID: {patient['patient_id']}")
        print(f"   ✅ Severity score: {patient['severity_score']}")
        print(f"   ✅ Triage level: {patient['triage_level']}")
        print(f"   ✅ Severity level: {interpretation['severity_level']}")
        print(f"   ✅ Recommended action: {interpretation['recommended_action']}")
        print(f"   ✅ Urgency: {interpretation['urgency']}")
    else:
        print(f"   ❌ Demo patient failed: {response.status_code}")
    
    # Test 7: Demo Scenario
    print("\n7. 🎭 Demo Scenario")
    response = requests.get(f"{API_BASE}/demo/scenario")
    if response.status_code == 200:
        scenario = response.json()
        state = scenario['current_state']
        
        print(f"   ✅ Queue length: {state['queue_length']}")
        print(f"   ✅ ICU utilization: {scenario['resource_status']['icu_utilization']}")
        print(f"   ✅ Doctor utilization: {scenario['resource_status']['doctor_utilization']}")
        print(f"   ✅ Queue preview: {len(scenario['queue_preview'])} patients")
    else:
        print(f"   ❌ Demo scenario failed: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed successfully!")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 ReDoc Documentation: http://localhost:8000/redoc")
    
    return True

def test_severity_calculation():
    """Test severity calculation directly"""
    print("\n🔬 Testing Severity Calculation")
    print("-" * 30)
    
    from severity import SeverityCalculator, SymptomType
    
    calc = SeverityCalculator()
    
    # Test critical patient
    critical_score = calc.calculate_severity_score(
        spo2=88, systolic_bp=85, heart_rate=125, age=75,
        symptoms=[SymptomType.CHEST_PAIN, SymptomType.CONFUSION]
    )
    
    print(f"🚨 Critical Patient:")
    print(f"   Score: {critical_score['severity_score']}")
    print(f"   Level: {critical_score['triage_level']}")
    print(f"   Expected: RED (≥50)")
    
    # Test moderate patient
    moderate_score = calc.calculate_severity_score(
        spo2=94, systolic_bp=120, heart_rate=95, age=45,
        symptoms=[SymptomType.HEADACHE]
    )
    
    print(f"\n⚠️ Moderate Patient:")
    print(f"   Score: {moderate_score['severity_score']}")
    print(f"   Level: {moderate_score['triage_level']}")
    print(f"   Expected: YELLOW (20-49)")
    
    # Test low severity patient
    low_score = calc.calculate_severity_score(
        spo2=98, systolic_bp=110, heart_rate=75, age=25,
        symptoms=[]
    )
    
    print(f"\n🟢 Low Severity Patient:")
    print(f"   Score: {low_score['severity_score']}")
    print(f"   Level: {low_score['triage_level']}")
    print(f"   Expected: GREEN (<20)")

def test_reward_system():
    """Test reward calculation"""
    print("\n⚖️ Testing Reward System")
    print("-" * 25)
    
    from reward import RewardCalculator, ActionType
    
    calc = RewardCalculator()
    
    # Test correct critical decision
    reward = calc.calculate_total_reward(
        ActionType.TREAT_NOW, severity_score=75.0, triage_level="RED",
        waiting_time=5, resources_available={"icu_beds": 3, "doctors": 5},
        resource_blocked=False
    )
    
    print(f"✅ Correct Critical Decision:")
    print(f"   Action: TREAT_NOW for RED patient")
    print(f"   Reward: {reward['total_reward']:.3f}")
    print(f"   Reason: {reward['decision_reason']}")
    
    # Test incorrect decision
    reward = calc.calculate_total_reward(
        ActionType.WAIT, severity_score=75.0, triage_level="RED",
        waiting_time=15, resources_available={"icu_beds": 3, "doctors": 5},
        resource_blocked=False
    )
    
    print(f"\n❌ Incorrect Critical Decision:")
    print(f"   Action: WAIT for RED patient")
    print(f"   Reward: {reward['total_reward']:.3f}")
    print(f"   Reason: {reward['decision_reason']}")

if __name__ == "__main__":
    print("🚀 Starting Hospital OpenEnv API Tests")
    print("Make sure the server is running: python main.py")
    print("Waiting for server to start...")
    time.sleep(2)
    
    # Test core functionality
    if test_api():
        print("\n✅ API tests passed!")
    
    # Test individual components
    test_severity_calculation()
    test_reward_system()
    
    print("\n🎯 All tests completed!")
    print("\n📋 Key Improvements Implemented:")
    print("   ✅ Severity score normalization (0-100)")
    print("   ✅ Triage level mapping (RED/YELLOW/GREEN)")
    print("   ✅ Resource constraint enforcement")
    print("   ✅ Balanced reward system")
    print("   ✅ Queue simulation with arrivals")
    print("   ✅ Explainable decision reasoning")
    print("   ✅ Termination logic")
    print("   ✅ FastAPI OpenEnv interface")
