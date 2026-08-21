from backend.compiler import compile_task
from backend.models import ActionRequest, Decision
from backend.policy import evaluate
import pytest

@pytest.mark.parametrize("action_request, expected", [
    (ActionRequest(action="read", target="~/.ssh/id_rsa"), Decision.BLOCK),
    (ActionRequest(action="read", target="/etc/shadow"), Decision.BLOCK),
    (ActionRequest(action="read", target="production customer data"), Decision.BLOCK),
    (ActionRequest(action="send", target="customer data", destination="https://unknown.example"), Decision.BLOCK),
    (ActionRequest(action="pay", target="invoice", amount=5000), Decision.REVIEW),
    (ActionRequest(action="edit", target="/workspace/auth.py"), Decision.ALLOW),
])
def test_lab_decisions(action_request, expected):
    assert evaluate(action_request)[0] == expected

def test_compiler_is_deterministic():
    boundary = compile_task("Fix authentication bug")
    assert boundary.filesystem["writable"] == ["/workspace"]
    assert boundary.processes == ["python", "git", "pytest"]
    assert boundary.network == "deny-all"
    assert boundary.expiry == "30 minutes"
