from data.mock_db import ORDERS_BY_ID, CUSTOMERS_BY_ID, PRODUCTS_BY_ID

def get_order(args):
    order_id = args.get("order_id", "")
    
    order = ORDERS_BY_ID.get(order_id)
    
    if not order:
        return {
            "found": False,
            "message": f"No order found with ID '{order_id}'. Please verify the order ID and try again."
        }
    
    # Enrich with customer and product info
    customer = CUSTOMERS_BY_ID.get(order["customer_id"], {})
    product = PRODUCTS_BY_ID.get(order["product_id"], {})
    
    return {
        "found": True,
        "order_id": order["order_id"],
        "customer_name": customer.get("name", "Unknown"),
        "customer_tier": customer.get("tier", "standard"),
        "product_name": product.get("name", "Unknown"),
        "product_category": product.get("category", "Unknown"),
        "quantity": order["quantity"],
        "amount": order["amount"],
        "status": order["status"],
        "order_date": order["order_date"],
        "delivery_date": order["delivery_date"],
        "return_deadline": order["return_deadline"],
        "refund_status": order["refund_status"],
        "notes": order["notes"]
    }
