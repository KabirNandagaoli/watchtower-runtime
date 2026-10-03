# Watchtower

Watchtower is an experimental control plane for autonomous-agent actions. It makes task-scoped authority visible and includes a narrow, real local-runtime prototype alongside a clearly separate policy simulation lab.

## What works now

`ControlledRuntime` mediates selected local filesystem and process requests in a dedicated temporary workspace. It resolves paths before acting, blocks absolute paths and traversal outside that workspace, rejects `~` credential paths, and starts only the approved `git` and `pytest` commands. A blocked mediated request is not opened or executed: its audit event reports `BLOCK`, `BLOCKED_AT_RUNTIME`, and `DENIED`.

The **LIVE RUNTIME** UI calls this endpoint. The **Policy Simulation Lab** calls the in-memory policy engine only; it is not host-level enforcement.

## Run locally

```bash
cd /Users/apple/Desktop/watchtower
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000. Run tests with `python -m pytest -q`.

## Runtime proof

```bash
curl -X POST http://127.0.0.1:8000/api/runtime/actions \
  -H 'content-type: application/json' \
  -d '{"operation":"read","target":"../../outside"}'
```

The response is a real mediated denial: `policy_decision: BLOCK`, `enforcement_status: BLOCKED_AT_RUNTIME`, and `actual_result: DENIED`.

## Free and Cloud

The MVP tracks up to 100 web runtime-action requests in memory. Once reached, the web endpoint returns 429; direct local/open-source `ControlledRuntime` usage remains available. Cloud Early Access stores name, work email, company, and use case only in memory and is not publicly listed; records disappear at restart.

Watchtower Cloud is planned, not available. Planned capabilities include centralized policies, persistent audit history, fleet management, team/RBAC, analytics, integrations, private deployment, and SSO/compliance.

## Limitations

This is not a complete OS sandbox or production endpoint-security product. Enforcement applies only to operations mediated through `ControlledRuntime`; a hosted dashboard cannot secure a visitor's computer. Runtime/process policy is intentionally narrow, state is in memory, and the optional Linux namespace support is experimental.
