import json
import os
import time
from agent import process_ticket
from data.mock_db import TICKETS

print("🤖 AI Customer Support Agent Starting...")
print(f"\n📋 Loaded {len(TICKETS)} tickets")

TICKETS_TO_RUN = TICKETS
print(f"🚀 Running all {len(TICKETS_TO_RUN)} tickets")

results = []
os.makedirs("logs", exist_ok=True)

for idx, ticket in enumerate(TICKETS_TO_RUN, 1):
    ticket_id      = ticket.get("ticket_id", "N/A")
    customer_email = ticket.get("customer_email", "Unknown")
    subject        = ticket.get("subject", "")
    body           = ticket.get("body", "")

    print(f"\n{'='*55}")
    print(f"🎫 Ticket: {ticket_id} | {customer_email}")
    print(f"📝 Subject: {subject}")
    print(f"💬 {body[:80]}...")
    print(f"{'='*55}")

    # ✅ WRITE PROCESSING — frontend shows this instantly
    with open("logs/live_status.json", "w") as f:
        json.dump({
            "current_ticket": ticket_id,
            "current_email": customer_email,
            "current_subject": subject,
            "status": "processing",
            "progress": idx,
            "total": len(TICKETS_TO_RUN)
        }, f)

    result = process_ticket(ticket)
    results.append(result)

    # ✅ WRITE DONE — frontend updates to green
    with open("logs/live_status.json", "w") as f:
        json.dump({
            "current_ticket": ticket_id,
            "current_email": customer_email,
            "current_subject": subject,
            "status": "done",
            "progress": idx,
            "total": len(TICKETS_TO_RUN)
        }, f)

    # ✅ SAVE audit log — ticket card appears in dashboard
    with open("logs/audit_log.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ {ticket_id} done — waiting 8s before next...")
    time.sleep(8)

# ✅ ALL DONE
with open("logs/live_status.json", "w") as f:
    json.dump({
        "current_ticket": "ALL DONE",
        "status": "complete",
        "progress": len(TICKETS_TO_RUN),
        "total": len(TICKETS_TO_RUN)
    }, f)

print(f"\n✅ All {len(results)} tickets processed!")