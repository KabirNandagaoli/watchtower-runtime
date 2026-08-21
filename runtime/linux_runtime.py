"""Experimental Linux-only namespace launcher. Not a complete security sandbox."""
import platform
import shutil
import subprocess

def namespace_available() -> bool:
    return platform.system() == "Linux" and shutil.which("unshare") is not None

def launch(command: list[str]) -> subprocess.CompletedProcess[str]:
    if not namespace_available():
        raise RuntimeError("Linux namespaces are unavailable on this platform; integration test skipped.")
    # This demonstrates namespace invocation only; it does not mount a safe filesystem or enforce policy.
    return subprocess.run(["unshare", "--user", "--map-root-user", "--mount", "--pid", "--fork", *command], text=True, capture_output=True, check=False)
