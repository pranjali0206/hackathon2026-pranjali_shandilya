def update_ticket_status(args):
    ticket_id = args.get("ticket_id", "")
    new_status = args.get("new_status", "")
    note = args.get("note", "")

    valid_statuses = ["open", "in_progress", "resolved", "escalated", "closed"]
    if new_status not in valid_statuses:
        return {
            "success": False,
            "message": f"Invalid status '{new_status}'. Valid options: {valid_statuses}"
        }

    return {
        "success": True,
        "ticket_id": ticket_id,
        "new_status": new_status,
        "note": note,
        "message": f"Ticket {ticket_id} status updated to '{new_status}'. Note: {note}"
    }
