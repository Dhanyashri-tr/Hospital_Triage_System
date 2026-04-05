def calculate_priority(heart_rate, oxygen, temperature, pain_level):
    score = 0

    # Heart rate rules
    if heart_rate > 120 or heart_rate < 50:
        score += 10
    elif heart_rate > 100:
        score += 5

    # Oxygen rules
    if oxygen < 90:
        score += 15
    elif oxygen < 95:
        score += 8

    # Temperature rules
    if temperature > 39:
        score += 10
    elif temperature > 37.5:
        score += 5

    # Pain level
    score += pain_level

    return score


def choose_action(priority_score):
    if priority_score >= 25:
        return "🚨 TREAT NOW (Critical Condition)"
    elif priority_score >= 15:
        return "⚠️ MONITOR (Needs Observation)"
    else:
        return "🕒 WAIT (Stable Condition)"


def triage_system(heart_rate, oxygen, temperature, pain_level):
    score = calculate_priority(heart_rate, oxygen, temperature, pain_level)
    decision = choose_action(score)

    # Explanation (IMPORTANT for hackathon scoring)
    explanation = []

    if oxygen < 90:
        explanation.append("Low oxygen level detected")
    if heart_rate > 120 or heart_rate < 50:
        explanation.append("Abnormal heart rate")
    if temperature > 39:
        explanation.append("High fever detected")
    if pain_level >= 7:
        explanation.append("Severe pain reported")

    if not explanation:
        explanation.append("Vitals are within acceptable range")

    return score, decision, ", ".join(explanation)