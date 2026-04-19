import json
import os

BASE = os.path.dirname(__file__)

def _load(filename):
    filepath = os.path.join(BASE, filename)
    with open(filepath, "r", encoding="utf-8-sig") as f:
        return json.load(f)

# Load all data from separate files
CUSTOMERS = _load("customers.json")
ORDERS    = _load("orders.json")
PRODUCTS  = _load("products.json")
TICKETS   = _load("tickets.json")

# Build lookup indexes
CUSTOMERS_BY_EMAIL = {c["email"]: c for c in CUSTOMERS}
CUSTOMERS_BY_ID    = {c["customer_id"]: c for c in CUSTOMERS}
ORDERS_BY_ID       = {o["order_id"]: o for o in ORDERS}
PRODUCTS_BY_ID     = {p["product_id"]: p for p in PRODUCTS}

# Load knowledge base
KB_PATH = os.path.join(os.path.dirname(BASE), "knowledge-base.md")
with open(KB_PATH, "r", encoding="utf-8-sig") as f:
    KNOWLEDGE_BASE = f.read()