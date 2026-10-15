# Language and Framework Audit Matrix

This is a targeted checklist, not a claim that every defect can be detected statically. Detect the actual stack and version from manifests, lockfiles, build files, runtime configuration, and source; then select applicable checks.

## Cross-language method

1. Identify entry points, trust boundaries, mutable shared state, async/task boundaries, persistence boundaries, external side effects, and lifecycle hooks.
2. Trace a normal flow plus failure, duplicate, and concurrent variants for every critical business operation.
3. Use ecosystem-native linters, type checks, dependency scanners, test runners, and static analyzers only when installed/configured or authorized. Record tool/version and actual result.
4. Distinguish pattern matches from verified defects. Consider framework semantics, version, configuration, and existing mitigations.
5. Report unsupported stacks and areas requiring runtime or domain-specific review.

## PHP, Laravel, Symfony, CodeIgniter

- Check request validation and authorization separately; do not trust route visibility or frontend validation.
- Trace PDO/ORM transactions and ensure writes participate in the intended transaction; check exception paths and nested transaction semantics.
- Inspect check-then-insert/update races; a prior SELECT is not a substitute for a unique constraint or atomic write.
- Review queue/job retry behavior, idempotency, overlapping scheduled jobs, and duplicate event handling.
- Check session locking/shared session behavior, session regeneration, CSRF protections, file upload/path handling, and secret exposure.
- For Laravel/Symfony, inspect middleware order, policy/voter enforcement, transaction boundaries, queue retry/backoff, failed-job handling, and ORM lazy-loading/N+1.
- For legacy CodeIgniter, verify controller/route filters, context-appropriate escaping, query builder/raw SQL boundaries, and legacy PHP/runtime compatibility.
- Check PHP-FPM worker saturation, persistent connections, resource cleanup, error display, and production debug configuration.

## Java, Spring, Hibernate/JPA, Jakarta EE

- Verify @Transactional semantics against proxy boundaries, propagation, rollback rules, checked exceptions, and self-invocation; annotation presence alone is not proof.
- Check mutable singleton/service fields for thread safety and unsafe shared state.
- Review executor/thread-pool sizing, queue bounds, rejection policy, cancellation, interruption, and shutdown lifecycle.
- Inspect lazy loading, N+1 queries, detached entities, optimistic/pessimistic locking, isolation levels, and transaction scope.
- Check CompletableFuture error propagation, timeout handling, context propagation, and executor selection.
- Verify method security and filter-chain ordering; check SSRF, deserialization, mass assignment, and secrets in config/logs.
- Check readiness/liveness, graceful shutdown, migrations, and compatibility between JDK/framework/library versions.

## JavaScript / TypeScript, Node.js, Express, NestJS, React, Next.js, Vue, Angular

- Treat every await boundary as a potential interleaving point; inspect check-then-act sequences and shared mutable state across requests/jobs.
- Check unhandled promise rejections, detached promises, missing error propagation, cancellation/timeout support, and cleanup in finally/lifecycle handlers.
- Check event-loop blocking, unbounded concurrency, stream backpressure, event-listener leaks, worker lifecycle, and connection-pool saturation.
- Verify idempotency for payment/webhook/job handlers and safe handling of duplicate/out-of-order events.
- Inspect SSRF, prototype pollution, unsafe deserialization, command execution, path traversal, and server-side secret exposure where applicable.
- For React/Next/Vue/Angular, inspect stale async responses, effect cleanup, hydration mismatch, cache invalidation, server/client trust boundaries, and authorization enforced only in the UI.
- Verify middleware/guard order, DTO/schema validation, output encoding, and server-side authorization.

## Python, Django, Flask, FastAPI, asyncio, Celery

- Check blocking I/O inside async handlers, task cancellation propagation, un-awaited coroutines, detached tasks, and exception retrieval.
- Review thread/process safety, shared mutable state, multiprocessing boundaries, executor lifecycle, and global caches.
- Verify ORM transaction scope, isolation, select-for-update/atomic update use where needed, and async ORM constraints for the installed version.
- Inspect Celery/job redelivery, acknowledgment timing, retry policy, idempotency, task time limits, and worker shutdown.
- Check request validation, authorization, unsafe pickle/deserialization, path handling, SSRF, debug mode, and secret leakage.
- Check dependency pinning/lockfiles, virtual environment assumptions, migrations, and runtime version compatibility.

## C# / .NET, ASP.NET Core, Entity Framework Core

- Look for .Result, .Wait(), sync-over-async, lost exceptions, and async methods that do not propagate cancellation.
- Check CancellationToken flow through HTTP, database, and background operations; consider overall timeout budgets.
- Verify DbContext lifetime and ensure it is not used concurrently; inspect transaction/isolation behavior and optimistic concurrency tokens.
- Check scoped service capture by singleton/background services, HttpClient lifetime/factory usage, and stream/resource disposal.
- Inspect hosted-service shutdown, channel/queue bounds, retry idempotency, and duplicate background work.
- Verify authorization policies, tenant/resource checks, model binding/validation, secret configuration, and exception handling.

## Go

- Check shared map/state access and data races; use go test -race only when safe/supported and record that it detects only races exercised by tests.
- Trace context.Context deadlines/cancellation into downstream calls; find goroutines that outlive requests or have no exit path.
- Inspect channel ownership/closure, blocked sends/receives, unbounded goroutines, worker shutdown, and timer/ticker cleanup.
- Review ignored errors, retry budgets, HTTP client/server timeouts, and response-body closure.
- Check transaction lifecycle, connection-pool settings, idempotent handlers, and graceful shutdown.

## Rust

- Memory safety does not prove business correctness or freedom from deadlocks. Inspect lock ordering, lock scope, contention, async blocking, and cancellation/drop behavior.
- Check unwrap/expect on externally influenced or operationally fallible paths; assess whether panic is acceptable.
- Review spawned tasks, task supervision, channel closure, backpressure, resource ownership, and shutdown.
- Inspect Send/Sync assumptions, shared-state synchronization, transaction boundaries, error context, and retry idempotency.
- Check unsafe blocks and FFI boundaries separately; their existence alone is not a defect.

## Ruby / Rails

- Check ActiveRecord transaction scope, callbacks with side effects, uniqueness races (application validation versus database constraint), N+1 queries, and lock behavior.
- Inspect ActiveJob/Sidekiq retries, duplicate execution, idempotency, concurrency, and failed-job recovery.
- Verify strong parameters, authorization, CSRF, mass assignment, secrets, and production debug settings.
- Check thread safety, connection-pool sizing, middleware ordering, and graceful shutdown.

## SQL and databases

### MySQL / MariaDB
- Verify transaction engine/table support, isolation, lock scope, deadlock handling, unique constraints, and transaction boundaries.
- Check SELECT-then-write races, upsert semantics, gap/next-key locks where relevant, implicit commits, migration compatibility, and replication assumptions.

### PostgreSQL
- Review isolation anomalies, ON CONFLICT semantics, row/advisory lock use, serialization-failure retry, long transactions, connection pools, and migration lock impact.

### Oracle
- Check transaction scope, row locking, sequence/identity assumptions, exception handling, implicit conversion/NLS dependencies, DDL commit behavior, and migration rollback.

### SQL Server
- Review isolation, locking hints, deadlocks, MERGE assumptions for the specific version/use case, transaction error handling, connection pooling, and deployment/migration behavior.

### All relational databases
- Validate database constraints, not only application checks; inspect indexes against actual predicates and execution plans when available.
- Check parameterization, least privilege, sensitive data, schema drift, migration ordering, rollback/forward-fix, and backup/restore evidence.
- Never run destructive queries, migrations, or production diagnostics without explicit scope and authorization.

## Frontend and client applications

- Do not treat frontend validation or hidden controls as authorization.
- Check stale requests, cancellation, duplicate submissions, optimistic-update rollback, offline/retry behavior, token storage, XSS sinks, and sensitive data in browser logs/storage.
- Verify API contracts, pagination boundaries, timezone/locale handling, error states, and supported browser/device compatibility.

## Containers, Kubernetes, and CI/CD

- Check health/readiness/liveness distinctions, graceful termination, signal handling, non-root execution, filesystem permissions, resource limits, and ephemeral storage.
- Check secret injection, image provenance/pinning, excessive permissions, exposed ports, unsafe build arguments, and environment configuration drift.
- Review rollout ordering, backward-compatible schema changes, retrying deployment jobs, concurrent pipelines, artifact integrity, and rollback limitations.
- Do not run cluster changes, load tests, or production fault injection during a read-only audit.

## Coverage reporting

For every detected stack, report:
- Detected language/framework/runtime and evidence.
- Applicable checks performed.
- Native tools/tests run and actual results.
- Checks not performed and why.
- Findings confirmed versus inferred.
- Areas requiring domain knowledge or runtime validation.

Do not state “all languages/frameworks covered.” State precisely which stacks were detected and which checks were applied.
