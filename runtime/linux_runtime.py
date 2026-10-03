"""Controlled local runtime prototype; not a complete OS sandbox."""
from __future__ import annotations
import platform, subprocess
from dataclasses import dataclass
from pathlib import Path
ALLOWED_COMMANDS={"git","pytest"}
@dataclass
class RuntimeResult:
    policy_decision:str; enforcement_status:str; actual_result:str; reason:str; output:str=""
class ControlledRuntime:
    def __init__(self,workspace:Path): self.workspace=workspace.resolve();self.workspace.mkdir(parents=True,exist_ok=True)
    def _inside(self,target:str):
        if target.startswith("~"): return None
        p=(self.workspace/target).resolve() if not Path(target).is_absolute() else Path(target).resolve()
        try:p.relative_to(self.workspace);return p
        except ValueError:return None
    def read(self,target):
        p=self._inside(target)
        if not p:return RuntimeResult("BLOCK","BLOCKED_AT_RUNTIME","DENIED","Outside task-scoped workspace boundary")
        try:return RuntimeResult("ALLOW","EXECUTED","READ","Workspace read allowed",p.read_text())
        except FileNotFoundError:return RuntimeResult("ALLOW","EXECUTED","NOT_FOUND","Workspace path allowed but file does not exist")
    def write(self,target,content):
        p=self._inside(target)
        if not p:return RuntimeResult("BLOCK","BLOCKED_AT_RUNTIME","DENIED","Outside task-scoped workspace boundary")
        p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content);return RuntimeResult("ALLOW","EXECUTED","WRITTEN","Workspace write allowed")
    def execute(self,command):
        if not command or command[0] not in ALLOWED_COMMANDS:return RuntimeResult("BLOCK","BLOCKED_AT_RUNTIME","DENIED","Process is not approved for this task")
        r=subprocess.run(command,cwd=self.workspace,text=True,capture_output=True,timeout=30,check=False);return RuntimeResult("ALLOW","EXECUTED","EXITED","Approved process executed",(r.stdout+r.stderr)[:4000])
def namespace_available():
    import shutil
    return platform.system()=="Linux" and shutil.which("unshare") is not None
