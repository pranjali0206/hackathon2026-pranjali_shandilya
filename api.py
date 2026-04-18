from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
import os

from agent import process_ticket

app = FastAPI(title="AI Customer Support Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run-tickets")
async def run_tickets(payload: dict):
    tickets = payload.get("tickets", [])

    def generate():
        results = []
        for ticket in tickets:
            ticket_id = ticket.get("ticket_id", "N/A")
            customer = ticket.get("customer_name", "Unknown")
            issue = ticket.get("issue", "")

            yield f"data: {json.dumps({'event': 'ticket_start', 'ticket_id': ticket_id, 'customer': customer, 'issue': issue})}\n\n"

            result = process_ticket(ticket)
            results.append(result)

            yield f"data: {json.dumps({'event': 'ticket_done', 'ticket_id': ticket_id, 'response': result.get('response', ''), 'confidence': result.get('confidence', 0), 'steps': result.get('steps', [])})}\n\n"

        os.makedirs("logs", exist_ok=True)
        with open("logs/audit_log.json", "w") as f:
            json.dump(results, f, indent=2)

        yield f"data: {json.dumps({'event': 'done', 'total': len(results)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/audit-log")
def get_audit_log():
    path = "logs/audit_log.json"
    if not os.path.exists(path):
        return {"error": "No audit log found. Run tickets first."}
    with open(path, "r") as f:
        return json.load(f)
