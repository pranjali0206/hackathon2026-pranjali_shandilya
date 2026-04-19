from data.mock_db import CUSTOMERS_BY_EMAIL, CUSTOMERS_BY_ID

def get_customer_info(args):
    identifier = args.get("identifier", "")
    
    # Try email first
    customer = CUSTOMERS_BY_EMAIL.get(identifier)
    
    # Try customer ID if email not found
    if not customer:
        customer = CUSTOMERS_BY_ID.get(identifier)
    
    if not customer:
        return {
            "found": False,
            "message": f"No customer found with identifier '{identifier}'. Ask customer for their registered email or order ID."
        }
    
    return {
        "found": True,
        "customer_id": customer["customer_id"],
        "name": customer["name"],
        "email": customer["email"],
        "tier": customer["tier"],
        "member_since": customer["member_since"],
        "total_orders": customer["total_orders"],
        "total_spent": customer["total_spent"],
        "notes": customer["notes"]
    }
