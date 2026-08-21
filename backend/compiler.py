from typing import List, Optional
from .models import Boundary

def compile_task(task: str, tools: Optional[List[str]] = None) -> Boundary:
    """A deliberately simple, deterministic demo compiler."""
    text = task.lower()
    processes = ["python", "git", "pytest"]
    if "database" in text:
        processes.append("psql")
    if "deploy" in text:
        processes.append("docker")
    return Boundary(
        filesystem={"writable": ["/workspace"], "readable": ["/workspace"]},
        processes=processes,
        network="deny-all",
        expiry="30 minutes",
    )
