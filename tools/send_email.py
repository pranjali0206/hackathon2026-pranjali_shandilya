def send_email(args):
    to = args.get("to", "")
    subject = args.get("subject", "")
    body = args.get("body", "")

    if not to or not subject or not body:
        return {
            "success": False,
            "message": "Missing required fields: to, subject, or body."
        }

    return {
        "success": True,
        "to": to,
        "subject": subject,
        "message": f"Email successfully sent to {to} with subject '{subject}'."
    }
