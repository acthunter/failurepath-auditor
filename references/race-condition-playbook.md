# Race Condition and Concurrency Playbook

Use this playbook for critical flows and shared resources. A race condition is not limited to threads: concurrent HTTP requests, async tasks, scheduled jobs, duplicate messages, multiple service instances, and retry/recovery can interleave even in single-threaded event loops.

## 1. Find concurrency boundaries

Look for:
- Shared mutable state, globals, singleton services, caches, session state, in-memory registries.
- Async/await, promises/futures, callbacks, goroutines, threads, executors, workers, background services.
- Scheduled tasks, queue consumers, webhook handlers, event listeners, cron jobs, distributed schedulers.
- Read-check-write sequences, read-modify-write counters, allocation of identifiers, inventory/quotas, permissions, status transitions.
- Database transactions, ORM unit-of-work, locks, queues, caches, file writes, external side effects.
- Multiple replicas/processes that do not share in-memory coordination.

## 2. Adversarial interleavings

For each operation, reason through at least these schedules where relevant:

1. Two callers read the same initial value before either writes.
2. Caller A validates a condition; caller B changes it; caller A writes based on stale validation.
3. A side effect succeeds but the caller times out before receiving acknowledgment, then retries.
4. A database commit succeeds but a queue publish or HTTP response fails.
5. A lock holder crashes or stalls; another caller waits indefinitely.
6. Two operations acquire locks/resources in opposite order.
7. A job is delivered twice or two scheduler instances start the same job.
8. A cancellation/shutdown happens after work starts but before completion/acknowledgment.
9. A cache and database are updated in different orders or one update fails.
10. A migration/deployment overlaps with old and new application versions.

## 3. Required questions

- What invariant must remain true (e.g. balance >= 0, inventory >= reserved, one active owner, monotonic state transition)?
- What exact interleaving violates it?
- Is the operation atomic at the layer that owns the invariant?
- Is enforcement only in application code, or is there a database constraint/atomic primitive?
- What isolation level and locking semantics actually apply to this engine/runtime/version?
- Are retries idempotent? How is a duplicate identified and retained long enough?
- What happens when the outcome is unknown to the caller?
- Can deadlock, starvation, or unbounded waiting occur?
- Can the issue be safely reproduced in a local/test environment?

## 4. Common weak patterns

These are investigation signals, not automatic findings:
- Check-if-not-exists followed by insert, with no database uniqueness enforcement.
- Read balance, check, then write balance without an atomic conditional update or suitable lock.
- Read status, perform side effect, then write status with no claim/lease/state guard.
- In-memory mutex used to protect work that runs across multiple processes/replicas.
- Retry around a non-idempotent external call.
- Fire-and-forget asynchronous task without supervision or durable tracking.
- Lock acquired without guaranteed release or with unbounded hold time.
- Multiple locks acquired in inconsistent order.
- Cache update assumed to be atomic with a database commit.
- A single-threaded event loop assumed to make all async workflows race-free.

## 5. Validation techniques

Prefer safe, bounded tests with barriers/latches to force an interleaving, repeated concurrent requests, unique-constraint tests, transaction-isolation tests, and invariant assertions. Use language-native race detectors or sanitizers when appropriate. Record tool versions and the exact test exercised.

Never run concurrency/load/fault tests against production by default. A passing race detector or test does not prove absence of races; it only provides evidence for exercised paths.

## 6. Remediation patterns to consider

Choose based on the invariant and architecture, not by default:
- Database unique/check constraints and atomic conditional updates.
- Explicit transaction and appropriate isolation/locking.
- Optimistic concurrency/version columns or compare-and-swap.
- Idempotency keys and durable deduplication records.
- Queue partitioning/serialization, leases, or distributed coordination when justified.
- Bounded queues, deadlines, cancellation propagation, and supervised workers.
- Consistent lock ordering and short critical sections.
- Outbox/inbox patterns or compensating actions for cross-system side effects.

Do not prescribe a distributed lock when a database constraint or atomic operation is sufficient. Document failure modes of any proposed coordination mechanism.

## 7. Finding evidence format

For every race/concurrency finding, record:
- Shared invariant/resource.
- Competing operations and exact interleaving.
- Relevant code locations and persistence/runtime semantics.
- Preconditions and likely frequency/exposure.
- Existing mitigation and why it is insufficient (if applicable).
- Reproduction/test strategy and whether actually run.
- Remediation alternatives, tradeoffs, and regression risks.
