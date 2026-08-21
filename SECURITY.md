# Security notice

This repository is an MVP demonstration. Its web policy decisions do **not** enforce security on the operating system, network, filesystem, model, or tool calls. Do not connect it to production agents, customer data, credentials, or payment systems.

The optional Linux namespace launcher is experimental and incomplete. Namespace isolation alone is not a sufficient security boundary. Production use needs reviewed privilege separation, syscall filtering, cgroups, mount design, network controls, signed policies, audit protection, key management, and independent security review.

Report repository vulnerabilities privately to the project maintainer; do not include secrets in reports.
