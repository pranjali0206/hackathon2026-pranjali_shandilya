import json
import os
import time
from agent import process_ticket
from data.mock_db import TICKETS

print("🤖 AI Customer Support Agent Starting...")
print(f"\n📋 Loaded {len(TICKETS)} tickets")

demo_ids = ["TKT-001", "TKT-010", "TKT-017", "TKT-018"]
TICKETS_TO_RUN = [t for t in TICKETS if t.get("ticket_id") in demo_ids]
print(f"🎬 Demo mode: running {len(TICKETS_TO_RUN)} tickets")

results = []

for ticket in TICKETS_TO_RUN:
    ticket_id = ticket.get("ticket_id", "N/A")
    customer_email = ticket.get("customer_email", "Unknown")
    subject = ticket.get("subject", "")
    body = ticket.get("body", "")

    print(f"\n{'='*55}")
    print(f"🎫 Ticket: {ticket_id} | {customer_email}")
    print(f"📝 Subject: {subject}")
    print(f"💬 {body[:80]}...")
    print(f"{'='*55}")

    result = process_ticket(ticket)
    results.append(result)
    time.sleep(3)

# Save audit log
os.makedirs("logs", exist_ok=True)
with open("logs/audit_log.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\n📁 Audit log saved to logs/audit_log.json")
print(f"\n✅ All tickets processed!")
print(f"   Total: {len(results)}")