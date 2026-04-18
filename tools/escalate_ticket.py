import uuid
from datetime import datetime

ESCALATION_QUEUE = []
PRIORITY_LEVELS = {"low", "medium", "high", "critical"}

def escalate_ticket(ticket_id: str, reason: str, priority: str = "medium") -> dict:
    priority = priority.lower()
    if priority not in PRIORITY_LEVELS:
        priority = "medium"
    escalation = {
        "escalation_id": f"ESC-{uuid.uuid4().hex[:6].upper()}",
        "ticket_id": ticket_id,
        "reason": reason,
        "priority": priority,
        "timestamp": datetime.now().isoformat(),
    }
    ESCALATION_QUEUE.append(escalation)
    return {
        "success": True,
        "escalation_id": escalation["escalation_id"],
        "ticket_id": ticket_id,
        "priority": priority,
        "message": f"Ticket '{ticket_id}' escalated with {priority} priority."
    }