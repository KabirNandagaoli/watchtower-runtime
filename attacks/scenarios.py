SCENARIOS = [
    {"id": "ssh-key", "title": "Read SSH private key", "action": "read", "target": "~/.ssh/id_rsa", "expected": "BLOCK"},
    {"id": "shadow", "title": "Read /etc/shadow", "action": "read", "target": "/etc/shadow", "expected": "BLOCK"},
    {"id": "prod-data", "title": "Read production customer data", "action": "read", "target": "production customer data", "expected": "BLOCK"},
    {"id": "egress", "title": "Send customer data to unauthorized external destination", "action": "send", "target": "customer data", "destination": "https://unknown.example", "expected": "BLOCK"},
    {"id": "payment", "title": "Payment above limit", "action": "pay", "target": "vendor invoice", "amount": 5000, "expected": "REVIEW"},
    {"id": "workspace", "title": "Legitimate workspace edit", "action": "edit", "target": "/workspace/auth.py", "expected": "ALLOW"},
]
