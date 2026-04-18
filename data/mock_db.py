import json
import os

# Load everything from one single JSON file
_path = os.path.join(os.path.dirname(__file__), "mock_data.json")
with open(_path, "r") as f:
    _data = json.load(f)

ORDERS    = _data["orders"]
INVENTORY = _data["inventory"]
CUSTOMERS = _data["customers"]
SHIPPING  = _data["shipping"]

# Build email → customer_id reverse index
EMAIL_INDEX = {v["email"]: k for k, v in CUSTOMERS.items()}