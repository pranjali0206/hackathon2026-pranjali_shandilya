def escalate_ticket(args):
    ticket_id = args.get("ticket_id", "")
    reason = args.get("reason", "")
    priority = args.get("priority", "medium")

    valid_priorities = ["low", "medium", "high", "urgent"]
    if priority not in valid_priorities:
        priority = "medium"

    return {
        "success": True,
        "ticket_id": ticket_id,
        "escalated": True,
        "priority": priority,
        "reason": reason,
        "message": f"Ticket {ticket_id} has been escalated to a human agent with {priority} priority. Reason: {reason}"
    }
