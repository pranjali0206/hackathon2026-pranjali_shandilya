import uuid
from datetime import datetime

EMAIL_LOG = []

def send_email(to: str, subject: str, body: str) -> dict:
    if not to or "@" not in to:
        return {"success": False, "error": f"Invalid email address: '{to}'"}
    record = {
        "email_id": f"EMAIL-{uuid.uuid4().hex[:6].upper()}",
        "to": to,
        "subject": subject,
        "body": body,
        "timestamp": datetime.now().isoformat(),
    }
    EMAIL_LOG.append(record)
    return {
        "success": True,
        "email_id": record["email_id"],
        "to": to,
        "subject": subject,
        "message": f"Email successfully sent to {to}."
    }