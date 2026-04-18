from data.mock_db import INVENTORY

def check_inventory(product_name: str) -> dict:
    key = product_name.strip().lower()
    if key in INVENTORY:
        item = INVENTORY[key].copy()
        item["product"] = product_name
        item["in_stock"] = item["stock"] > 0
        item["success"] = True
        return item
    return {
        "success": False,
        "error": f"Product '{product_name}' not found. Available: {list(INVENTORY.keys())}",
        "product": product_name
    }