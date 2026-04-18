from tools.get_order import get_order
from tools.check_inventory import check_inventory
from tools.process_refund import process_refund
from tools.send_email import send_email
from tools.escalate_ticket import escalate_ticket
from tools.check_shipping import check_shipping
from tools.update_ticket_status import update_ticket_status
from tools.get_customer_info import get_customer_info

TOOL_REGISTRY = {
    "get_order": {
        "fn": get_order,
        "description": "Get order details by order ID (e.g. ORD-1001)",
        "args": ["order_id"]
    },
    "check_inventory": {
        "fn": check_inventory,
        "description": "Check stock level for a product by name",
        "args": ["product_name"]
    },
    "process_refund": {
        "fn": process_refund,
        "description": "Process a refund for a delivered or cancelled order",
        "args": ["order_id", "reason"]
    },
    "send_email": {
        "fn": send_email,
        "description": "Send an email to a customer",
        "args": ["to", "subject", "body"]
    },
    "escalate_ticket": {
        "fn": escalate_ticket,
        "description": "Escalate a ticket to a human agent with a priority level",
        "args": ["ticket_id", "reason", "priority"]
    },
    "check_shipping": {
        "fn": check_shipping,
        "description": "Check shipping/tracking status for an order",
        "args": ["order_id"]
    },
    "update_ticket_status": {
        "fn": update_ticket_status,
        "description": "Update the status of a support ticket",
        "args": ["ticket_id", "new_status", "note"]
    },
    "get_customer_info": {
        "fn": get_customer_info,
        "description": "Get customer info by customer ID or email address",
        "args": ["identifier"]
    },
}