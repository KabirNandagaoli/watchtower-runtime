# Architecture

The frontend calls FastAPI endpoints to create agents, compile task boundaries, and evaluate actions. The policy engine is a deterministic, inspectable ruleset. It records every decision in an in-memory audit log; persistence is deliberately outside this MVP.

The `runtime` package is separate so a future controller can delegate to an actual Linux enforcement service rather than confusing UI policy evaluation with enforcement.
