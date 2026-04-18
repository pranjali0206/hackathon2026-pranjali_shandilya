from datetime import datetime

TICKET_STORE = {}
VALID_STATUSES = {"open", "in_progress", "resolved", "closed", "escalated", "pending"}

def update_ticket_status(ticket_id: str, new_status: str, note: str = "") -> dict:
    new_status = new_status.lower().strip()
    if new_status not in VALID_STATUSES:
        return {
            "success": False,
            "error": f"Invalid status '{new_status}'.",
            "ticket_id": ticket_id
        }
    previous = TICKET_STORE.get(ticket_id, {}).get("status", "unknown")
    TICKET_STORE[ticket_id] = {
        "ticket_id": ticket_id,
        "status": new_status,
        "note": note,
        "updated_at": datetime.now().isoformat(),
        "previous_status": previous
    }
    return {
        "success": True,
        "ticket_id": ticket_id,
        "previous_status": previous,
        "new_status": new_status,
        "message": f"Ticket '{ticket_id}' updated to '{new_status}'."
    }