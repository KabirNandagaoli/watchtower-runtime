from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_dashboard_and_frontend_load():
    assert client.get("/").status_code == 200
    dashboard = client.get("/api/dashboard")
    assert dashboard.status_code == 200
    assert "enforcement_notice" in dashboard.json()

def test_create_agent_compile_and_log_action():
    created = client.post("/api/agents", json={"name":"Test Agent", "purpose":"Test", "task":"Fix authentication bug"})
    assert created.status_code == 200
    agent_id = created.json()["id"]
    boundary = client.get(f"/api/agents/{agent_id}/boundary").json()
    assert boundary["network"] == "deny-all"
    action = client.post("/api/actions", json={"agent_id":agent_id,"action":"edit","target":"/workspace/app.py"})
    assert action.status_code == 200
    assert action.json()["decision"] == "ALLOW"
    assert "SIMULATED" in action.json()["enforcement"]

def test_runtime_action_is_honestly_audited():
    denied=client.post("/api/runtime/actions",json={"operation":"read","target":"../../credential"})
    assert denied.status_code==200
    body=denied.json()
    assert body["decision"]=="BLOCK" and body["enforcement_status"]=="BLOCKED_AT_RUNTIME" and body["actual_result"]=="DENIED"

def test_metrics_and_early_access_are_private_api_only():
    before=client.get("/api/product-metrics").json()["free_usage"]
    response=client.post("/api/early-access",json={"name":"Ada", "email":"ada@example.com", "company":"Example", "ai_use_case":"Testing AI agents"})
    assert response.status_code==200 and response.json()["status"]=="received"
    assert client.post("/api/early-access",json={"name":"Ada", "email":"invalid", "company":"Example", "ai_use_case":"Testing AI agents"}).status_code==422
    assert client.get("/api/product-metrics").json()["free_usage"]==before
