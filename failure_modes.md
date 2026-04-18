# ⚠️ Failure Modes & Mitigations

## 1. LLM Hallucination (Tool Results)
**Problem:** LLM invents tool results instead of waiting for real ones.  
**Symptom:** Agent responds with made-up order data, fake tracking numbers.  
**Fix Applied:** Each tool call is stripped from the conversation and replaced
with the real result before the LLM continues. Temperature set to 0.1.

## 2. Multiple Tool Calls in One Step
**Problem:** LLM outputs several TOOL_CALLs at once instead of one at a time.  
**Symptom:** Only the first tool runs; others are ignored silently.  
**Fix Applied:** `extract_tool_call()` uses regex to extract only the FIRST
match. System prompt explicitly says "call ONE tool at a time."

## 3. Infinite Loop / Max Steps Exceeded
**Problem:** Agent keeps calling tools without reaching a FINAL response.  
**Symptom:** Runs forever or hits API rate limits.  
**Fix Applied:** Hard cap of `max_steps=8`. Tickets exceeding this are
automatically dead-lettered and flagged for human review.

## 4. Unknown Tool Called
**Problem:** LLM hallucinates a tool name that doesn't exist.  
**Symptom:** KeyError or silent failure.  
**Fix Applied:** `run_tool()` checks the TOOL_REGISTRY first and returns
`{"success": False, "error": "Unknown tool"}` safely.

## 5. Wrong Arguments Passed to Tool
**Problem:** LLM passes incorrect argument names or types.  
**Symptom:** TypeError when calling the tool function.  
**Fix Applied:** `run_tool()` wraps all calls in try/except TypeError and
returns a structured error dict back to the LLM so it can self-correct.

## 6. Order Not Eligible for Refund
**Problem:** Customer requests refund on a "shipped" or "processing" order.  
**Symptom:** `process_refund` returns success=False.  
**Fix Applied:** Tool returns a clear error message. LLM reads it and either
escalates or explains the policy to the customer.

## 7. Groq API Failure / Rate Limit
**Problem:** Groq API is down or rate limit hit.  
**Symptom:** Exception during `client.chat.completions.create()`.  
**Fix Applied:** API call wrapped in try/except. On failure, loop breaks
and ticket is dead-lettered with an error note in the audit log.

## 8. Invalid Email Address
**Problem:** Ticket has a malformed or missing customer email.  
**Symptom:** `send_email` fails validation.  
**Fix Applied:** `send_email` validates `@` presence and returns
`{"success": False}` — agent sees this and skips the email step.

## 9. Ticket Data Missing Fields
**Problem:** A ticket JSON is missing order_id, email, or issue fields.  
**Symptom:** Agent operates on "N/A" or empty strings.  
**Fix Applied:** `process_ticket()` uses `.get()` with safe defaults for
all fields. Agent will escalate if it cannot find needed data.

## 10. Low Confidence Resolution
**Problem:** Agent resolves ticket but isn't confident in its answer.  
**Symptom:** Confidence score below 60%.  
**Recommended Action:** Flag these in the audit log for human spot-check.