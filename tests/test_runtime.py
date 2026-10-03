from pathlib import Path
from runtime.linux_runtime import ControlledRuntime

def test_runtime_enforces_workspace_and_processes(tmp_path: Path):
    runtime=ControlledRuntime(tmp_path/"workspace")
    assert runtime.write("ok.txt","hello").actual_result=="WRITTEN"
    assert runtime.read("ok.txt").output=="hello"
    for target in ["../../outside.txt","/etc/shadow","~/.ssh/id_rsa"]:
        result=runtime.read(target);assert result.enforcement_status=="BLOCKED_AT_RUNTIME";assert result.actual_result=="DENIED"
    assert runtime.execute(["sh","-c","echo nope"]).actual_result=="DENIED"
    assert runtime.execute(["git","--version"]).enforcement_status=="EXECUTED"
