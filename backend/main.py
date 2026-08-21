from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .compiler import compile_task
from .models import ActionRequest, Agent, AgentCreate, SecurityEvent
from .policy import evaluate
from attacks.scenarios import SCENARIOS

ROOT = Path(__file__).resolve().parent.parent
app = FastAPI(title="Watchtower MVP", version="0.1.0")
app.mount("/static", StaticFiles(directory=ROOT / "frontend"), name="static")

agents: dict[str, Agent] = {
    "demo-agent": Agent(id="demo-agent", name="Atlas Fixer", purpose="Fix application bugs safely", model="GPT-4.1", framework="OpenAI Agents SDK", task="Fix authentication bug", tools=["git", "pytest"], data=["workspace source"], permissions=["workspace write"], limits={"payment_usd": 1000})
}
events: list[SecurityEvent] = []

@app.get("/")
def index():
    return FileResponse(ROOT / "frontend" / "index.html")

@app.get("/api/agents")
def list_agents(): return list(agents.values())

@app.post("/api/agents", response_model=Agent)
def create_agent(payload: AgentCreate):
    agent = Agent(id=str(uuid4())[:8], **payload.model_dump())
    agents[agent.id] = agent
    return agent

@app.get("/api/agents/{agent_id}")
def get_agent(agent_id: str):
    if agent_id not in agents: raise HTTPException(404, "Agent not found")
    return agents[agent_id]

@app.get("/api/agents/{agent_id}/boundary")
def get_boundary(agent_id: str):
    if agent_id not in agents: raise HTTPException(404, "Agent not found")
    return compile_task(agents[agent_id].task, agents[agent_id].tools)

@app.post("/api/actions", response_model=SecurityEvent)
def run_action(payload: ActionRequest):
    if payload.agent_id not in agents: raise HTTPException(404, "Agent not found")
    decision, reason, rule = evaluate(payload)
    event = SecurityEvent(id=str(uuid4())[:8], agent_id=payload.agent_id, action=payload.action, target=payload.target, decision=decision, reason=reason, rule=rule, details=payload.model_dump(exclude={"agent_id", "action", "target"}, exclude_none=True))
    events.insert(0, event)
    return event

@app.get("/api/events")
def list_events(): return events

@app.get("/api/events/{event_id}")
def get_event(event_id: str):
    for event in events:
        if event.id == event_id: return event
    raise HTTPException(404, "Security event not found")

@app.get("/api/scenarios")
def scenarios(): return SCENARIOS

@app.get("/api/dashboard")
def dashboard():
    return {"active_agents": len(agents), "actions_today": len(events), "blocked": sum(e.decision == "BLOCK" for e in events), "human_review": sum(e.decision == "REVIEW" for e in events), "high_risk": sum(e.decision in {"BLOCK", "REVIEW"} for e in events), "enforcement_notice": "Demo policy evaluation only; no OS-level enforcement is active from this dashboard."}
