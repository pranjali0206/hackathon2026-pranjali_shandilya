from data.mock_db import PRODUCTS_BY_ID, PRODUCTS

def check_inventory(args):
    product_name = args.get("product_name", "").lower()
    
    # Search by name (partial match)
    matches = [
        p for p in PRODUCTS
        if product_name in p["name"].lower()
    ]
    
    if not matches:
        return {
            "found": False,
            "message": f"No product found matching '{product_name}'."
        }
    
    product = matches[0]
    
    return {
        "found": True,
        "product_id": product["product_id"],
        "name": product["name"],
        "category": product["category"],
        "price": product["price"],
        "stock": product["stock"],
        "in_stock": product["stock"] > 0,
        "warranty_months": product["warranty_months"],
        "return_window_days": product["return_window_days"],
        "registered_online": product["registered_online"]
    }
