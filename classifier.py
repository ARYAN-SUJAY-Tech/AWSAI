def classify_issue(text: str) -> str:
    try:
        text = text.lower()

        if any(k in text for k in ["accessdenied", "not authorized", "permission"]):
            return "IAM / Permissions"

        if any(k in text for k in ["timeout", "endpoint", "connection refused"]):
            return "Networking"

        if any(k in text for k in ["rds", "dynamodb", "database", "unable to connect"]):
            return "Service Integration"

        return "General AWS Issue"

    except Exception:
        return "General AWS Issue"
