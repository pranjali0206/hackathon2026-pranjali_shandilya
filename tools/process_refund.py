from data.mock_db import ORDERS_BY_ID

def process_refund(args):
    order_id = args.get("order_id", "")
    reason = args.get("reason", "")

    order = ORDERS_BY_ID.get(order_id)

    if not order:
        return {
            "success": False,
            "message": f"Order '{order_id}' not found. Cannot process refund."
        }

    if order.get("refund_status") == "refunded":
        return {
            "success": False,
            "message": f"Refund for order '{order_id}' was already processed. No duplicate refund issued."
        }

    # Mark as refunded in memory
    order["refund_status"] = "refunded"

    return {
        "success": True,
        "order_id": order_id,
        "amount": order["amount"],
        "reason": reason,
        "message": f"Refund of  processed successfully for order {order_id}. Customer will receive funds in 5-7 business days."
    }
