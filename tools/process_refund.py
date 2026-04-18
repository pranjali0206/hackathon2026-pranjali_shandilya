from tools.get_order import get_order

REFUNDABLE_STATUSES = {"delivered", "cancelled"}

def process_refund(order_id: str, reason: str = "Customer request") -> dict:
    order = get_order(order_id)
    if not order.get("success"):
        return {
            "success": False,
            "error": f"Cannot refund: {order.get('error')}",
            "order_id": order_id
        }
    status = order.get("status")
    if status not in REFUNDABLE_STATUSES:
        return {
            "success": False,
            "error": f"Order '{order_id}' has status '{status}' and is not eligible for refund.",
            "order_id": order_id
        }
    import uuid
    refund_id = f"REF-{uuid.uuid4().hex[:6].upper()}"
    return {
        "success": True,
        "refund_id": refund_id,
        "order_id": order_id,
        "amount_refunded": order["price"],
        "item": order["item"],
        "reason": reason,
        "message": f"Refund of ${order['price']:.2f} approved for {order['item']}."
    }