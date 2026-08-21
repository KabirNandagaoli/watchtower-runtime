from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field

class Decision(str, Enum):
    ALLOW = "ALLOW"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"

class AgentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    purpose: str
    model: str = "GPT-4.1"
    framework: str = "Custom"
    task: str
    tools: list[str] = []
    data: list[str] = []
    permissions: list[str] = []
    limits: dict[str, Any] = {}
    approval_requirements: str = "High-risk actions require human review"

class Agent(AgentCreate):
    id: str
    status: str = "Sandboxed"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ActionRequest(BaseModel):
    agent_id: str = "demo-agent"
    action: str
    target: str
    destination: Optional[str] = None
    amount: Optional[float] = None
    context: dict[str, Any] = {}

class SecurityEvent(BaseModel):
    id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    agent_id: str
    action: str
    target: str
    decision: Decision
    reason: str
    rule: str
    enforcement: str = "SIMULATED WEB-DEMO POLICY — no host action was intercepted"
    details: dict[str, Any] = {}

class Boundary(BaseModel):
    filesystem: dict[str, list[str]]
    processes: list[str]
    network: str
    expiry: str
    disclaimer: str = "Deterministic prototype boundary, not production-grade policy generation."
