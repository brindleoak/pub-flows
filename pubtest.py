from typing import NamedTuple
import random
from rapidfuzz import fuzz
import re

class Flow(NamedTuple):
    code: str
    desc: str
    short: str

flows = [
    Flow("PUB-001", "Notification of Change of Supplier", "Change Supply"),
    Flow("PUB-002", "Notification to New Supplier of Site Information", "Site info"),
    Flow("PUB-004", "Comms Hub Information (Optional)", "Comms hub info"),
    Flow("PUB-005", "Metering Service MTD Updates to Registration", "MS MTD update"),
    Flow("PUB-006", "Notification of Metering Service MTD Update to Registration", "MTD Update"),
    Flow("PUB-007", "Change of Energisation Status Outcome", "MS Energisation Status"),
    Flow("PUB-008", "Registration Service Notification of Change of Energisation Status", "Energisation Status"),
    Flow("PUB-009", "Notification of LDSO Disconnection / CSS De-Registration", "Disconnection"),
    Flow("PUB-013", "MDS Defaults Applied", "x"),
    Flow("PUB-014", "Rejected Consumption Data Submission", "x"),
    Flow("PUB-015", "Request Historic Consumption Replay (ADV Sites only)", "x"),
    Flow("PUB-016", "HH Consumption History Replay  (ADV Sites only)", "x"),
    Flow("PUB-018", "Notification of Registration Data Item Changes", "x"),
    Flow("PUB-019", "Maintain MPAN Relationships", "x"),
    Flow("PUB-020", "Maintain MPAN Relationships Outcome", "x"),
    Flow("PUB-021", "UTC Settlement Period Consumption Data", "x"),
    Flow("PUB-022", "LSS Period Data", "x"),
    Flow("PUB-023", "LSS Totals Data", "x"),
    Flow("PUB-024", "Supplier Advisory Notification to DS", "x"),
    Flow("PUB-025", "Supplier Updates to Registration", "x"),
    Flow("PUB-026", "Registration Service Notification of Supplier Data Chg", "x"),
    Flow("PUB-027", "Consumption Amendment Request", "x"),
    Flow("PUB-028", "Consumption Amendment Request Response", "x"),
    Flow("PUB-031", "Supplier Service Provider Appointment Request", "x"),
    Flow("PUB-032", "Supplier Service Provider Appointment Request Response", "x"),
    Flow("PUB-033", "Registration Service Request for Service Appointment", "x"),
    Flow("PUB-034", "Service Provider Appointment Request Response", "x"),
    Flow("PUB-035", "Registration Service Appointment Status Notification", "x"),
    Flow("PUB-036", "Registration Service Notification of Service Appointment & Supporting Info", "x"),
    Flow("PUB-037", "Registration Service Notification of Service De-Appointment", "x"),
    Flow("PUB-038", "Customer Direct Contract Advisory", "x"),
    Flow("PUB-039", "Customer Direct Contract Advisory Response", "x"),
    Flow("PUB-040", "Notification of Annual Consumption", "x"),
    Flow("PUB-041", "Smart / Advanced Readings", "x"),
    Flow("PUB-043", "Registration Service Notification of Change of Connection Type", "x"),
    Flow("PUB-044", "Registration Service Notification of Change of Segment", "x"),
    Flow("PUB-045", "Registration Service Reminder Notification", "x"),
    Flow("PUB-047", "Notification of the Publication of a Downloadable Asset", "x"),
    Flow("PUB-050", "EES Updates", "x"),
]

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def quiz_loop():
    random.shuffle(flows)

    print("🧠 Flashcard Trainer — Ctrl+C to quit\n")

    while True:
        card: Flow = flows.pop(0)

        if random.random() < 0.5:
            print(f"\n📘 Description: {card.desc}")
            answer = input("Enter the CODE: ").strip().upper()
            if answer == card.code:
                print("✅ Correct!")
                flows.append(card)  
            else:
                print(f"❌ Incorrect. Correct code: {card.code}")
                flows.insert(5, card)

        else: 
            print(f"\n📗 Code: {card.code}")
            answer = input("Enter the DESCRIPTION: ").strip()
            similarity = fuzz.token_sort_ratio(normalize(answer), normalize(card.short))
            if similarity >= 75:
                print(f"✅ Correct! (Similarity: {similarity}%)")
                flows.append(card)
            else:
                print(f"❌ Incorrect. Similarity: {similarity}%")
                print(f"Expected: {card.desc}")
                flows.insert(5, card)

if __name__ == "__main__":
    try:
        quiz_loop()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
