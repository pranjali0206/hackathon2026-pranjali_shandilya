import json
import os
from datetime import datetime
from agent import process_ticket

TICKETS_FILE = "data/tickets.json"
LOG_FILE = "logs/audit_log.json"

def load_tickets():
    with open(TICKETS_FILE, "r") as f:
        return json.load(f)

def save_log(results):
    os.makedirs("logs", exist_ok=True)
    log = {
        "run_timestamp": datetime.now().isoformat(),
        "total_tickets": len(results),
        "results": results
    }
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)
    print(f"\n📁 Audit log saved to {LOG_FILE}")

def main():
    print("🤖 AI Customer Support Agent Starting...\n")
    tickets = load_tickets()
    print(f"📋 Loaded {len(tickets)} tickets\n")

    results = []
    for ticket in tickets:
        result = process_ticket(ticket)
        results.append(result)

    save_log(results)
    print("\n✅ All tickets processed!")
    print(f"   Total: {len(results)}")

if __name__ == "__main__":
    main()