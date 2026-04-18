from data.mock_db import CUSTOMERS, EMAIL_INDEX

def get_customer_info(identifier: str) -> dict:
    identifier = identifier.strip()
    if identifier.upper() in CUSTOMERS:
        customer = CUSTOMERS[identifier.upper()].copy()
        customer["customer_id"] = identifier.upper()
        customer["success"] = True
        return customer
    if identifier.lower() in EMAIL_INDEX:
        cust_id = EMAIL_INDEX[identifier.lower()]
        customer = CUSTOMERS[cust_id].copy()
        customer["customer_id"] = cust_id
        customer["success"] = True
        return customer
    return {
        "success": False,
        "error": f"Customer '{identifier}' not found. Available emails: {list(EMAIL_INDEX.keys())}",
        "identifier": identifier
    }