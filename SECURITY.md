# Security scope

Watchtower is an experimental, Linux-first prototype. It is not production-grade endpoint security and not a complete OS sandbox.

## Real enforcement

`ControlledRuntime` fails closed for mediated workspace paths: paths resolving outside its configured workspace, including traversal and absolute-path escapes, are denied before filesystem access. Tilde paths are denied. It allowlists only `git` and `pytest`, so other mediated commands do not start. Audit fields distinguish policy decision, enforcement status, and actual result.

This is enforcement only for actions that go through `ControlledRuntime`. It does not intercept arbitrary shell commands, applications, model tool calls, or filesystem access on the host. The hosted web UI cannot enforce operations on a visitor's computer.

## Simulation and state

The Security Lab is an in-memory policy simulation, not a host attack environment. Product metrics and Cloud Early Access submissions are in memory, are not publicly exposed, and disappear when the server restarts. Do not submit sensitive data.

Linux namespace functionality is experimental and platform dependent. It is not relied on as a complete boundary. Do not connect this prototype to production credentials, customer data, or payment systems.
