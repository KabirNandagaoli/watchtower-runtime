from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .compiler import compile_task
from .models import ActionRequest, Agent, AgentCreate, SecurityEvent, RuntimeActionRequest, EarlyAccessSignup
from .policy import evaluate
from attacks.scenarios import SCENARIOS
from runtime.linux_runtime import ControlledRuntime

ROOT = Path(__file__).resolve().parent.parent
app = FastAPI(title="Watchtower MVP", version="0.1.0")
app.mount("/static", StaticFiles(directory=ROOT / "frontend"), name="static")

agents: dict[str, Agent] = {
    "demo-agent": Agent(id="demo-agent", name="Atlas Fixer", purpose="Fix application bugs safely", model="GPT-4.1", framework="OpenAI Agents SDK", task="Fix authentication bug", tools=["git", "pytest"], data=["workspace source"], permissions=["workspace write"], limits={"payment_usd": 1000})
}
events: list[SecurityEvent] = []
runtime = ControlledRuntime(Path("/tmp/watchtower-runtime-workspace"))
FREE_RUNTIME_LIMIT = 100
runtime_usage = 0
early_access_signups: list[EarlyAccessSignup] = []

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

@app.post("/api/runtime/actions", response_model=SecurityEvent)
def run_runtime_action(payload: RuntimeActionRequest):
    global runtime_usage
    if payload.agent_id not in agents: raise HTTPException(404, "Agent not found")
    if runtime_usage >= FREE_RUNTIME_LIMIT:
        raise HTTPException(429, "You've reached your Watchtower Free limit. Local/open-source runtime functionality remains available.")
    if payload.operation == "read": result = runtime.read(payload.target)
    elif payload.operation == "write": result = runtime.write(payload.target, payload.content)
    elif payload.operation == "execute": result = runtime.execute(payload.command)
    else: raise HTTPException(422, "Unsupported runtime operation")
    event = SecurityEvent(id=str(uuid4())[:8], agent_id=payload.agent_id, action=payload.operation, target=payload.target or " ".join(payload.command), decision=result.policy_decision, policy_decision=result.policy_decision, reason=result.reason, rule="controlled-runtime", enforcement=result.enforcement_status, enforcement_status=result.enforcement_status, actual_result=result.actual_result, details={"output": result.output})
    events.insert(0, event)
    runtime_usage += 1
    return event

@app.get("/api/product-metrics")
def product_metrics():
    return {"agents_created": len(agents), "runtime_actions_attempted": runtime_usage, "actions_allowed": sum(e.actual_result not in {None, "DENIED"} for e in events), "actions_blocked": sum(e.actual_result == "DENIED" for e in events), "free_limit": FREE_RUNTIME_LIMIT, "free_usage": runtime_usage, "early_access_signups": len(early_access_signups)}

@app.post("/api/early-access")
def join_early_access(payload: EarlyAccessSignup):
    if "@" not in payload.email or "." not in payload.email.rsplit("@", 1)[-1]: raise HTTPException(422, "Enter a valid work email.")
    early_access_signups.append(payload)
    return {"status": "received"}

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
