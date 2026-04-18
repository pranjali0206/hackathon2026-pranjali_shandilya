from data.mock_db import ORDERS

def get_order(order_id: str) -> dict:
    order_id = order_id.strip().upper()
    if order_id in ORDERS:
        order = ORDERS[order_id].copy()
        order["order_id"] = order_id
        order["success"] = True
        return order
    return {
        "success": False,
        "error": f"Order '{order_id}' not found. Available orders: {list(ORDERS.keys())}",
        "order_id": order_id
    }