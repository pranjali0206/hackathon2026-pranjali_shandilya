from tools.get_order import get_order
from tools.check_inventory import check_inventory
from tools.process_refund import process_refund
from tools.send_email import send_email
from tools.escalate_ticket import escalate_ticket
from tools.check_shipping import check_shipping
from tools.update_ticket_status import update_ticket_status
from tools.get_customer_info import get_customer_info

TOOL_REGISTRY = {
    "GET_CUSTOMER_INFO": get_customer_info,
    "GET_ORDER": get_order,
    "CHECK_INVENTORY": check_inventory,
    "PROCESS_REFUND": process_refund,
    "SEND_EMAIL": send_email,
    "ESCALATE_TICKET": escalate_ticket,
    "CHECK_SHIPPING": check_shipping,
    "UPDATE_TICKET_STATUS": update_ticket_status,
    "get_customer_info": get_customer_info,
    "get_order": get_order,
    "check_inventory": check_inventory,
    "process_refund": process_refund,
    "send_email": send_email,
    "escalate_ticket": escalate_ticket,
    "check_shipping": check_shipping,
    "update_ticket_status": update_ticket_status,
}