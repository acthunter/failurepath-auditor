# Finding taxonomy

Use this taxonomy to keep findings consistent across projects. Categories can overlap; select one primary category and optionally note secondary categories.

| Code | Category | Typical examples |
|---|---|---|
| FAIL | Failure handling | swallowed exception, false success, missing timeout |
| DATA | Data integrity | partial writes, invalid state, unsafe migration |
| CONC | Concurrency/idempotency | race condition, duplicate side effect, lost update |
| AUTH | Security and access control | authorization bypass, IDOR, secret exposure |
| RES | Resource lifecycle/capacity | leaked connection, unbounded queue, exhaustion |
| PERF | Performance/scalability | N+1 query, contention, unbounded fan-out |
| DEP | Dependency/compatibility | unsupported runtime, verified vulnerable dependency |
| OBS | Observability/operations | missing actionable telemetry, unsafe restart |
| ARCH | Maintainability/architecture | duplicated business rules, excessive coupling |
| TEST | Test quality/coverage | missing failure-path assertion, misleading mock |

## Evidence status

- **Confirmed**: directly supported by code/configuration or authoritative artifacts.
- **Reproduced**: safely reproduced with a documented command or test.
- **Plausible**: technically credible but one or more assumptions remain unverified.
- **Unverified**: requires additional access, runtime evidence, or human confirmation.

## Confidence

- **High**: direct evidence and clear causal path.
- **Medium**: evidence supports the concern but important behavior is inferred.
- **Low**: limited evidence; prioritize validation rather than presenting as fact.

Severity and confidence are independent. A high-impact hypothesis can require urgent validation while remaining unconfirmed.
