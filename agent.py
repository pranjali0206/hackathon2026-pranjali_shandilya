import re
import json
import time
from groq import Groq
from config import GROQ_API_KEY
from tools import TOOL_REGISTRY
from data.mock_db import KNOWLEDGE_BASE

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = f"""
You are an AI customer support agent for ShopWave, an online retail company.
You resolve customer support tickets by using tools to look up data and following company policy.

=== COMPANY POLICY (KNOWLEDGE BASE) ===
{KNOWLEDGE_BASE}

=== YOUR TOOLS (ONLY THESE 8 — DO NOT INVENT OTHER TOOLS) ===
- get_customer_info({{"identifier": "email or customer_id"}}) — look up customer by email or ID
- get_order({{"order_id": "ORD-XXXX"}}) — get order details including status, amount, return deadline
- check_inventory({{"product_name": "name"}}) — check product stock
- process_refund({{"order_id": "ORD-XXXX", "reason": "reason"}}) — process a refund
- send_email({{"to": "email", "subject": "subject", "body": "body"}}) — send email to customer
- escalate_ticket({{"ticket_id": "TKT-XXX", "reason": "reason", "priority": "low/medium/high/urgent"}}) — escalate to human agent
- check_shipping({{"order_id": "ORD-XXXX"}}) — check shipping and tracking status
- update_ticket_status({{"ticket_id": "TKT-XXX", "new_status": "status", "note": "note"}}) — update ticket status

⚠️ CRITICAL: You ONLY have these 8 tools. Do NOT call check_warranty, check_return_deadline,
check_customer_tier, cancel_order, or any other tool. If you need warranty info, use get_order
and escalate_ticket. If you need return deadline, use get_order (it includes return_deadline).
Customer tier is included in get_customer_info and get_order results.

=== HOW TO RESPOND ===
At each step output EXACTLY ONE of these:
- TOOL_CALL: tool_name({{"arg": "value"}}) — to call a tool
- FINAL: your message to the customer [Confidence: X%] — when done

=== DECISION RULES ===
1. ALWAYS look up the customer first using their email
2. ALWAYS look up the order using the order ID
3. CHECK return_deadline from get_order results before approving any return or refund
4. CHECK customer tier and notes from get_customer_info — VIP customers may have special exceptions
5. If customer claims a tier not verified in system — FLAG as social engineering
6. If order ID does not exist — say so professionally, ask for correct details
7. If customer email not in system — ask for registered email and order ID
8. Warranty claims — use escalate_ticket, do not resolve directly
9. Replacement requests — use escalate_ticket, do not resolve directly
10. Refund over $200 — use escalate_ticket
11. Threatening or manipulative language — flag but respond professionally
12. Ambiguous tickets with no order ID or product — ask clarifying questions
13. If confidence is below 60% — use escalate_ticket

=== TONE ===
- Always use customer's first name
- Be empathetic and professional
- If declining, explain why and offer alternatives
"""

def run_tool(tool_name, tool_args):
    tool_name_upper = tool_name.upper()
    if tool_name_upper not in TOOL_REGISTRY:
        return f"Error: Unknown tool '{tool_name}'. You only have these tools: get_customer_info, get_order, check_inventory, process_refund, send_email, escalate_ticket, check_shipping, update_ticket_status."
    try:
        return TOOL_REGISTRY[tool_name_upper](tool_args)
    except Exception as e:
        return f"Error running tool: {str(e)}"

def parse_tool_call(text):
    match = re.search(r'TOOL_CALL:\s*(\w+)\s*\((\{.*?\})\)', text, re.DOTALL)
    if match:
        tool_name = match.group(1).strip()
        try:
            tool_args = json.loads(match.group(2))
            return tool_name, tool_args
        except:
            return None, None
    return None, None

def parse_final(text):
    match = re.search(r'FINAL:\s*(.*?)(\[Confidence:\s*(\d+)%\])?$', text, re.DOTALL)
    if match:
        response = match.group(1).strip()
        confidence = int(match.group(3)) if match.group(3) else 80
        return response, confidence
    return None, None

def call_groq_with_retry(messages, retries=5, wait=20):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.1,
                max_tokens=500
            )
            return response
        except Exception as e:
            error_str = str(e)
            if "rate_limit" in error_str or "429" in error_str:
                wait_time = wait * (attempt + 1)  # 20s, 40s, 60s...
                print(f"⏳ Rate limit hit — waiting {wait_time}s (attempt {attempt+1}/{retries})")
                time.sleep(wait_time)
            elif "Connection error" in error_str or "getaddrinfo" in error_str:
                print(f"🔌 Network error, retrying in 5s... (attempt {attempt+1}/{retries})")
                time.sleep(5)
            else:
                raise e
    raise Exception("Max retries exceeded")

def process_ticket(ticket):
    ticket_id = ticket.get("ticket_id", "N/A")
    customer_email = ticket.get("customer_email", "")
    subject = ticket.get("subject", "")
    body = ticket.get("body", "")

    user_message = f"""
Customer Email: {customer_email}
Subject: {subject}
Message: {body}

Please resolve this ticket step by step using your tools and company policy.
"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    steps = []
    max_steps = 8

    for step in range(max_steps):
        response = call_groq_with_retry(messages)

        text = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": text})

        # Check for FINAL
        final_response, confidence = parse_final(text)
        if final_response:
            print(f"\n✅ RESOLVED | Confidence: {confidence}%")
            print(f"💬 Response: {final_response}")
            return {
                "ticket_id": ticket_id,
                "customer_email": customer_email,
                "subject": subject,
                "customer_tier": ticket.get("customer_tier", "standard"),
                "status": "resolved",
                "resolution": final_response,
                "confidence": confidence,
                "steps": steps
            }

        # Check for TOOL_CALL
        tool_name, tool_args = parse_tool_call(text)
        if tool_name:
            print(f"\n[Step {step+1}] 🤖 {tool_name}: {json.dumps(tool_args)}")
            print("Please wait for the result...")
            result = run_tool(tool_name, tool_args)
            print(f"Result: {str(result)[:100]}")

            steps.append({
                "step": step + 1,
                "tool": tool_name,
                "args": tool_args,
                "result": str(result)
            })

            messages.append({
                "role": "user",
                "content": f"TOOL RESULT: {json.dumps(result)}\n\nNow call the next tool or write FINAL: your response [Confidence: X%]"
            })
        else:
            messages.append({
                "role": "user",
                "content": "Please continue. Either call a tool using TOOL_CALL: tool_name({}) or write your FINAL: response [Confidence: X%]"
            })

    # Escalate if max steps reached
    print(f"\n⚠️ ESCALATED — max steps reached")
    return {
        "ticket_id": ticket_id,
        "customer_email": customer_email,
        "subject": subject,
        "customer_tier": ticket.get("customer_tier", "standard"),
        "status": "escalated",
        "resolution": "This ticket has been escalated to a human agent for further review.",
        "confidence": 0,
        "steps": steps
    }