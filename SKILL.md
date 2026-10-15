---
name: failurepath-auditor
description: Audit software projects for hidden technical debt, happy-path bias, failure handling gaps, security weaknesses, data integrity risks, concurrency bugs, recovery failures, operational risks, and missing tests. Use when asked to audit, assess, review, inventory, or prioritize technical debt across a codebase or workspace. Read-only by default.
license: MIT
compatibility: Works with coding agents that support the Agent Skills SKILL.md format and can inspect local files.
metadata:
  author: acthunter
  version: "1.1.0"
  category: software-quality
---

# FailurePath Auditor

Perform evidence-driven audits that deliberately look beyond the happy path. Identify realistic failure modes and hidden technical debt—not speculative code smells.

## Operating principles

1. **Read-only by default.** Do not modify application source, tests, configuration, dependencies, databases, or deployment state during an audit. Creating new audit reports in a clearly designated report directory is allowed. Never overwrite existing reports without permission.
2. **Evidence before claims.** Every actionable finding must point to a file and symbol/line range when available, explain the trigger, and distinguish confirmed behavior from inference. Do not invent runtime behavior, dependency behavior, test results, or security advisories.
3. **Trace end-to-end.** Follow entry points through validation, authorization, business logic, persistence, external calls, side effects, and response/acknowledgment.
4. **Adversarial, not alarmist.** Ask what happens when each step fails, repeats, races, times out, or receives unexpected data. Do not label a theoretical possibility as a confirmed vulnerability.
5. **Coverage honesty.** Track what was inspected, tested, inferred, and blocked. Listing files or passing existing tests does not prove full audit coverage.
6. **Preserve the environment.** Never run destructive tests, migrations, load tests, or fault injection against production unless explicitly authorized and safely scoped.
7. **Secrets hygiene.** Never reproduce secrets in reports. Redact tokens, credentials, private keys, and sensitive personal data.
8. **Prioritize impact.** Favor actionable findings with plausible triggers and meaningful consequences over style preferences.

## Workflow

### Phase 0 — Scope and safety

- Identify workspace root and user-specified boundaries.
- Inspect `AGENTS.md`, `CLAUDE.md`, README, contributor guidance, and existing audit reports. Do not overwrite existing reports.
- Identify production-facing systems. Risky tests are prohibited by default.
- If root is ambiguous, inspect current directory and immediate children; ask only if safe scope cannot be determined.

### Phase 1 — Discover and inventory

Discover repositories and applications without traversing huge generated directories unnecessarily. Look for Git roots, manifests, build files, entry points, deployments, migrations, tests, and configuration. Common generated/vendor paths to skip during routine analysis: `.git`, `node_modules`, `vendor`, `dist`, `build`, `coverage`, caches, compiled artifacts, and virtual environments. Inspect them if a concrete finding requires it.

Record each candidate's path, language/framework/runtime with evidence, entry points, databases, queues, caches, external services, identity/security boundaries, build/test/deploy setup, cross-project dependencies, tests actually run, audit status, limitations, and confidence. Do not assume every folder is an active project. For large workspaces, checkpoint and process batches.

### Phase 2 — Architecture and assumptions

Trace critical request/event flows through side effects. Map state transitions, persistence and transaction boundaries, external dependencies, failure propagation, trust boundaries, and assumptions about input, identity, ordering, uniqueness, timing, availability, and permissions. Mark inferred architecture separately from verified architecture.

### Phase 3 — Detect stack and apply playbooks

Detect actual languages, framework versions, concurrency model, database engines, build tools, and deployment targets from manifests/source evidence. Read `references/language-framework-matrix.md` and `references/race-condition-playbook.md` when present. Select applicable checks only. These playbooks are starting points, not exhaustive guarantees. For unsupported stacks, derive checks from runtime semantics and record limitations. Keyword searches alone are insufficient: inspect call paths and semantics.

Audit these categories:

- **Failure handling:** swallowed exceptions, false-success responses, missing deadlines/timeouts, partial failure, unsafe retries/backoff, cancellation gaps, broken error contracts.
- **Data integrity and transactions:** non-atomic writes, check-then-act races, lost updates, duplicates/orphans/stale state, null and boundary errors, precision/timezone/encoding, missing constraints, unsafe migrations/rollback, lock contention, engine/version assumptions.
- **Concurrency/idempotency:** duplicate execution, shared mutable state, overlapping jobs, lock lifecycle, retrying side effects, commit-success/ack-failure ambiguity, out-of-order events.
- **Security:** authentication and authorization gaps, IDOR, privilege escalation, tenant isolation, injection, XSS, CSRF, SSRF, path traversal, unsafe deserialization/file handling, session/token lifecycle, secrets in code/logs, excessive privileges, unsafe TLS/CORS/cookie/header/debug defaults. Verify controls on real execution paths.
- **Resource lifecycle/capacity:** unreleased connections/files/sockets/locks, memory or worker leaks, unbounded queues, pool exhaustion, oversized requests, disk-full and permission behavior.
- **Performance/scalability:** N+1, avoidable scans, missing/mismatched indexes, critical-path blocking, cache invalidation, lock contention, oversized payloads, unbounded fan-out. Do not claim performance regressions without evidence.
- **Dependencies/compatibility:** incompatible or unsupported versions, confirmed applicable advisories, uncontrolled transitive dependencies, build/runtime mismatch, undocumented behavior, schema/API breaking changes, environment drift.
- **Observability/operations:** context-poor or missing logs, absent correlation identifiers where useful, missing alerts, shallow health checks, premature readiness, restart duplication/lost work, unverifiable backup/recovery, missing rollback, sensitive telemetry.
- **Maintainability/architecture:** harmful duplication, circular coupling, oversized modules, dead code, scattered business rules, inconsistent error handling, ambiguous contracts, unsafe compatibility workarounds, changes that break consumers.
- **Testing:** weak assertions, nominal-only tests, missing failure-path, integration, concurrency, property, mutation, or migration tests where relevant; over-mocking and flaky/non-reproducible tests.

Do not force irrelevant checks onto a project. Use N/A with a reason as needed. Do not claim a dependency is vulnerable without exact version and applicable advisory evidence.

### Phase 4 — Adversarial failure scenarios

For each critical flow, analyze relevant cases among: database unavailable; timeout or malformed external response; partial operation failure; duplicate request/event; concurrent state mutation; invalid/oversized data; cache/database divergence; token expiry; restart during work; disk full/permission error; deployment failure during migration; load beyond capacity.

For each case, record trigger, execution sequence, detection behavior, state consistency, retry safety, recoverability, operator signals, and test evidence. Keep hypothetical scenarios distinct from reproduced/confirmed ones.

### Phase 5 — Testing and validation

Review tests, assertions, mocks, fixtures, boundary conditions, and missing scenarios. Run existing tests only if safe and dependencies/environment are available. Record exact commands and outcomes. Do not claim a test passed unless actually run. Add tests only in a separately authorized remediation stage. Never run destructive or production load/fault/concurrency tests by default.

### Phase 6 — Root cause and blast radius

For every finding, identify underlying cause, impacted modules/data/business process, cross-project consumers, whether the issue is local or systemic, regression risks, and recurring patterns in other projects. Do not claim a local fix resolves other consumers until checked.

### Phase 7 — Severity and confidence

Severity:
- **CRITICAL:** confirmed or highly credible immediate risk to major security boundaries, data integrity, or critical operations.
- **HIGH:** realistic significant impact on security, availability, data, or essential transactions.
- **MEDIUM:** meaningful defect or maintenance burden with narrower impact/prerequisites.
- **LOW:** limited impact or straightforward improvement.
- **INFO:** observation not established as a defect.

Also record confidence (High/Medium/Low), evidence, status (confirmed/reproduced/plausible/unverified), blast radius, effort (S/M/L/XL), and priority. Do not equate severity with confidence; critical-looking low-confidence hypotheses need validation.

### Phase 8 — Deliverables

Create reports in a separate `audit-reports/` directory without overwriting existing files. Produce:

1. `00_EXECUTIVE_SUMMARY.md` — audited/blocked counts, top risks, cross-project patterns, immediate actions.
2. `01_PROJECT_INVENTORY.md` — every candidate, stack evidence, entry points, dependencies, and audit status.
3. `02_CROSS_PROJECT_RISK_REGISTER.md` — prioritized evidence-backed findings and shared root causes.
4. `03_PROJECT_DEEP_DIVE.md` — architecture, findings, failure scenarios, test gaps, recommendations per project.
5. `04_FAILURE_SCENARIO_MATRIX.md` — critical flows, triggers, expected/actual behavior, state risk, recovery, test status.
6. `05_REMEDIATION_ROADMAP.md` — P0/P1/P2/P3 order, dependencies, effort, regression risk, acceptance criteria.
7. `06_TEST_GAP_MATRIX.md` — critical flows versus existing tests and missing failure coverage.
8. `07_AUDIT_COVERAGE.md` — inspected, partial, blocked, untested, and human-review items.

Priority: P0 validated critical risk; P1 high risk/data integrity; P2 resilience/performance/observability; P3 maintainability. Explain rationale.

### Phase 9 — Execution strategy and done criteria

1. Discover all candidates.
2. Map dependencies and prioritize by risk/centrality.
3. Audit projects in batches, with checkpointing for long sessions.
4. Adversarially inspect critical flows.
5. Validate findings and compare cross-project patterns.
6. Consolidate reports and verify coverage.

Use subagents if available, with clear non-overlapping scopes; avoid conflicting writes. If time/context is insufficient, report actual progress and resume from checkpoint rather than claiming completion.

Audit is complete only when every discovered candidate has an explicit status; critical projects are inspected or blockers documented; high-priority findings have evidence; failure scenarios/test gaps are documented; cross-project risks and roadmap exist; and all execution/validation claims are truthful.

Begin with discovery and inventory. Do not modify application code during the initial audit. Continue with safe read-only steps without waiting for approval.
