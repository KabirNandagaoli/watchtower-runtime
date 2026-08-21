from .models import ActionRequest, Decision

SENSITIVE_PATHS = {"/etc/shadow": "Linux password hashes", "~/.ssh/id_rsa": "SSH private keys"}

def evaluate(action: ActionRequest) -> tuple[Decision, str, str]:
    target = action.target.lower()
    destination = (action.destination or "").lower()
    if target in SENSITIVE_PATHS or "ssh" in target and "key" in target:
        return Decision.BLOCK, f"Protected secret access: {SENSITIVE_PATHS.get(target, 'private key material')}.", "secrets-deny"
    if target == "/etc/shadow":
        return Decision.BLOCK, "Protected system credential database.", "system-files-deny"
    if "production customer" in target or "customer data" in target and "production" in target:
        return Decision.BLOCK, "Production customer data is outside this agent's approved data scope.", "data-scope-deny"
    if "customer data" in target and destination and not destination.endswith("trusted.example"):
        return Decision.BLOCK, "Customer data cannot be sent to an unauthorized external destination.", "egress-deny"
    if action.amount is not None and action.amount > 1000:
        return Decision.REVIEW, f"Payment of ${action.amount:,.2f} exceeds the $1,000 approval limit.", "payment-approval"
    if target.startswith("/workspace") and action.action.lower() in {"write", "edit", "update"}:
        return Decision.ALLOW, "Workspace edit is within the scoped writable boundary.", "workspace-write"
    return Decision.REVIEW, "No deterministic rule can safely authorize this action.", "default-review"
