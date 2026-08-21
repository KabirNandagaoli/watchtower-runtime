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
