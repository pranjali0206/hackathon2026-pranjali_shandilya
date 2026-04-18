import json
import re
from groq import Groq
from config import GROQ_API_KEY
from tools import TOOL_REGISTRY

client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.1-8b-instant"

def build_tool_descriptions():
    lines = []
    for name, info in TOOL_REGISTRY.items():
        args = ", ".join(info["args"])
        lines.append(f"- {name}({args}): {info['description']}")
    return "\n".join(lines)

SYSTEM_PROMPT = f"""
You are an AI customer support agent. You resolve support tickets using tools.

AVAILABLE TOOLS:
{build_tool_descriptions()}

STRICT RULES — follow exactly:
1. Call ONE tool at a time using this exact format:
   TOOL_CALL: tool_name({{"arg1": "value1"}})

2. Wait for the tool result before calling another tool.

3. Do NOT invent or guess tool results. Only use real results returned to you.

4. When fully resolved, respond with:
   FINAL: <your message to the customer>

5. At the end of your FINAL message, add a confidence score like this:
   [Confidence: 85%]

6. If you cannot resolve after using tools, respond:
   FINAL: I'm escalating your ticket to our support team for further assistance. [Confidence: 0%]
"""

def extract_tool_call(text):
    """Parse the FIRST tool call only from LLM output."""
    match = re.search(r'TOOL_CALL:\s*(\w+)\((\{.*?\})\)', text, re.DOTALL)
    if match:
        tool_name = match.group(1)
        try:
            args = json.loads(match.group(2))
            return tool_name, args
        except json.JSONDecodeError:
            return None, None
    return None, None

def extract_confidence(text):
    """Extract confidence percentage from FINAL response."""
    match = re.search(r'\[Confidence:\s*(\d+)%\]', text)
    if match:
        return int(match.group(1))
    return 50  # default if not found

def run_tool(tool_name, args):
    """Execute a tool safely with error handling."""
    if tool_name not in TOOL_REGISTRY:
        return {"success": False, "error": f"Unknown tool '{tool_name}'. Only use listed tools."}
    try:
        fn = TOOL_REGISTRY[tool_name]["fn"]
        result = fn(**args)
        return result
    except TypeError as e:
        return {"success": False, "error": f"Wrong arguments for '{tool_name}': {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Tool error: {str(e)}"}

def process_ticket(ticket: dict, max_steps: int = 8) -> dict:
    ticket_id = ticket.get("id", "UNKNOWN")
    print(f"\n{'='*55}")
    print(f"🎫 Ticket: {ticket_id} | {ticket.get('customer_name','?')}")
    print(f"📝 Issue: {ticket.get('issue','')}")
    print(f"{'='*55}")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": (
            f"Ticket ID: {ticket_id}\n"
            f"Customer: {ticket.get('customer_name', 'Unknown')}\n"
            f"Email: {ticket.get('customer_email', '')}\n"
            f"Order ID: {ticket.get('order_id', 'N/A')}\n"
            f"Issue: {ticket.get('issue', '')}\n\n"
            f"Resolve this ticket. Call tools one at a time. Wait for each result."
        )}
    ]

    steps = []
    final_response = None
    confidence = 0

    for step in range(max_steps):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.1,
                max_tokens=300
            )
        except Exception as e:
            print(f"❌ Groq API error: {e}")
            break

        llm_output = response.choices[0].message.content.strip()
        print(f"\n[Step {step+1}] 🤖 {llm_output[:200]}")

        # ── FINAL response detected ──
        if "FINAL:" in llm_output:
            final_text = llm_output.split("FINAL:", 1)[1].strip()
            confidence = extract_confidence(final_text)
            # Clean the confidence tag out of the customer-facing message
            final_response = re.sub(r'\[Confidence:.*?\]', '', final_text).strip()
            steps.append({
                "step": step + 1,
                "type": "final",
                "content": final_response,
                "confidence": confidence
            })
            print(f"\n✅ RESOLVED | Confidence: {confidence}%")
            print(f"💬 Response: {final_response}")
            break

        # ── Tool call detected ──
        tool_name, args = extract_tool_call(llm_output)
        if tool_name:
            print(f"🔧 Tool: {tool_name} | Args: {args}")
            result = run_tool(tool_name, args)
            result_str = json.dumps(result)
            print(f"📦 Result: {result_str[:150]}")

            steps.append({
                "step": step + 1,
                "type": "tool_call",
                "tool": tool_name,
                "args": args,
                "result": result,
                "tool_success": result.get("success", False)
            })

            # Feed exactly ONE tool result back — prevents hallucination
            messages.append({"role": "assistant", "content": f"TOOL_CALL: {tool_name}({json.dumps(args)})"})
            messages.append({"role": "user", "content": f"TOOL RESULT: {result_str}\n\nNow call the next tool or write FINAL:"})

        else:
            # LLM produced thinking text — keep it but nudge it forward
            messages.append({"role": "assistant", "content": llm_output})
            messages.append({"role": "user", "content": "Continue. Call a tool or write FINAL:"})
            steps.append({"step": step + 1, "type": "thought", "content": llm_output})

    # ── Dead-letter queue: max steps hit without resolution ──
    if not final_response:
        final_response = "We were unable to automatically resolve your issue. A human agent will contact you shortly."
        confidence = 0
        steps.append({"step": max_steps, "type": "dead_letter", "content": final_response})
        print(f"\n⚠️  Dead-lettered: {ticket_id}")

    return {
        "ticket_id": ticket_id,
        "customer_name": ticket.get("customer_name"),
        "customer_email": ticket.get("customer_email"),
        "issue": ticket.get("issue"),
        "final_response": final_response,
        "confidence": confidence,
        "steps_taken": len(steps),
        "steps": steps,
        "status": "resolved" if confidence > 0 else "escalated"
    }