from data.mock_db import SHIPPING

def check_shipping(order_id: str) -> dict:
    order_id = order_id.strip().upper()
    if order_id in SHIPPING:
        info = SHIPPING[order_id].copy()
        info["order_id"] = order_id
        info["success"] = True
        return info
    return {
        "success": False,
        "error": f"No shipping info for '{order_id}'. Available: {list(SHIPPING.keys())}",
        "order_id": order_id
    }