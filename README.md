# Watchtower

**Secure what AI does.** Watchtower is a Linux-first runtime and control-plane MVP for autonomous AI agents.

## Honest scope

The dashboard, policy decisions, action log, task compiler, and Security Lab are **simulated web-demo controls**. They demonstrate a product workflow; they do not secure a host or contain an arbitrary agent.

`runtime/linux_runtime.py` is an experimental Linux-only launcher which invokes `unshare` when available. It is not a complete sandbox, security boundary, or production-ready isolation layer. It is intentionally unavailable on macOS and Windows.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
make test
make run
```

Open http://127.0.0.1:8000. Use the Security Lab to run six prebuilt scenarios or create an agent from the dashboard.

## What is real vs simulated

| Capability | Status |
| --- | --- |
| Dashboard, API, deterministic policy evaluation, audit records | Real application behavior |
| Lab action results and policy classifications | Simulated demo policy decisions |
| Task-to-boundary compiler | Deterministic prototype, not policy generation |
| Linux namespace launcher | Experimental implementation, Linux only |
| Host-level enforcement, secrets protection, production isolation | Not implemented |

## Structure

- `backend/` FastAPI API, models, policy engine, compiler
- `frontend/` vanilla HTML/CSS/JavaScript dashboard
- `runtime/` experimental Linux namespace launcher
- `attacks/` Security Lab scenario definitions
- `tests/` API and policy tests
- `docs/` architecture notes
