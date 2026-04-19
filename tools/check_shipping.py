from data.mock_db import ORDERS_BY_ID

def check_shipping(args):
    order_id = args.get("order_id", "")

    order = ORDERS_BY_ID.get(order_id)

    if not order:
        return {
            "found": False,
            "message": f"Order '{order_id}' not found."
        }

    status = order.get("status", "unknown")
    notes = order.get("notes", "")

    # Extract tracking number from notes if present
    tracking = None
    if "Tracking:" in notes:
        tracking = notes.split("Tracking:")[-1].strip().rstrip(".")

    return {
        "found": True,
        "order_id": order_id,
        "status": status,
        "order_date": order.get("order_date"),
        "delivery_date": order.get("delivery_date"),
        "tracking_number": tracking,
        "notes": notes
    }
