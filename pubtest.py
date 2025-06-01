import random
from rapidfuzz import fuzz
import re
from collections import deque

pairs = {
    "PUB-001": "Change of Supplier",
    "PUB-002": "New Supplier Site Information",
    "PUB-004": "Comms Hub Information",
    "PUB-005": "Metering Service MTD Updates",
    "PUB-006": "Notification of Metering Service MTD Update",
    "PUB-007": "Change of Energisation Status Outcome",
    "PUB-008": "Change of Energisation Status",
    "PUB-009": "LDSO Disconnection",
    "PUB-013": "MDS Defaults Applied",
    "PUB-014": "Rejected Consumption Data",
    "PUB-015": "Request Historic Consumption Replay (ADV Sites only)",
    "PUB-016": "HH Consumption History Replay  (ADV Sites only)",
    "PUB-018": "Registration Data Item Changes",
    "PUB-019": "Maintain MPAN Relationships",
    "PUB-020": "Maintain MPAN Relationships Outcome",
    "PUB-021": "Consumption Data",
    "PUB-022": "LSS Period Data",
    "PUB-023": "LSS Totals Data",
    "PUB-024": "Supplier Advisory Notification",
    "PUB-025": "Supplier Updates",
    "PUB-026": "Supplier Data Chg",
    "PUB-027": "Consumption Amendment Request",
    "PUB-028": "Consumption Amendment Request Response",
    "PUB-031": "Appointment Request",
    "PUB-032": "Appointment Request Response",
    "PUB-033": "Service Appointment Request",
    "PUB-034": "Appointment Request Response",
    "PUB-035": "Appointment Status Notification",
    "PUB-036": "Appointment & Supporting Info",
    "PUB-037": "Service De-Appointment",
    "PUB-038": "Customer Direct Contract Advisory",
    "PUB-039": "Customer Direct Contract Advisory Response",
    "PUB-040": "Annual Consumption",
    "PUB-041": "Readings",
    "PUB-043": "Change of Connection Type",
    "PUB-044": "Change of Segment",
    "PUB-045": "Reminder Notification",
    "PUB-047": "Publication of a Downloadable Asset",
    "PUB-050": "EES Updates",
}


# Normalize for fuzzy matching
def normalize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

# Flashcard format
class Flashcard:
    def __init__(self, code, desc):
        self.code = code
        self.desc = desc

# Initialize queue with shuffled items
def make_queue(pairs):
    items = [Flashcard(code, desc) for code, desc in pairs.items()]
    random.shuffle(items)
    return deque(items)

def quiz_loop():
    queue = make_queue(pairs)
    cooldown_queue = deque()  # (turns_remaining, flashcard)
    turn = 0

    print("🧠 Flashcard Trainer — Ctrl+C to quit\n")

    while True:
        # Reinsert cooled-down flashcards
        for _ in range(len(cooldown_queue)):
            turns_left, card = cooldown_queue.popleft()
            if turns_left <= 0:
                queue.append(card)
            else:
                cooldown_queue.append((turns_left - 1, card))

        # Get next flashcard
        if not queue:
            print("🎉 Queue empty (this shouldn't happen) — restarting...")
            queue = make_queue(pairs)

        card = queue.popleft()
        quiz_type = random.choice(["code", "desc"])

        if quiz_type == "desc":
            print(f"\n📘 Description: {card.desc}")
            answer = input("Enter the CODE: ").strip().upper()
            if answer == card.code:
                print("✅ Correct!")
                queue.append(card)  # send to back
            else:
                print(f"❌ Incorrect. Correct code: {card.code}")
                cooldown_queue.append((5, card))  # reappear after 5 turns

        else:  # quiz_type == "code"
            print(f"\n📗 Code: {card.code}")
            answer = input("Enter the DESCRIPTION: ").strip()
            similarity = fuzz.token_sort_ratio(normalize(answer), normalize(card.desc))
            if similarity >= 85:
                print(f"✅ Correct! (Similarity: {similarity}%)")
                queue.append(card)
            else:
                print(f"❌ Incorrect. Similarity: {similarity}%")
                print(f"Expected: {card.desc}")
                cooldown_queue.append((5, card))

        turn += 1

if __name__ == "__main__":
    try:
        quiz_loop()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
