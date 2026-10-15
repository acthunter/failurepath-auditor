# FailurePath Auditor

**An agent skill for evidence-driven technical debt, failure-path, security, concurrency, and resilience audits across software projects.**

FailurePath Auditor helps coding agents look beyond the happy path: partial failures, unsafe retries, concurrency, data integrity, authorization boundaries, resource leaks, recovery behavior, operational risks, and tests that pass without proving resilience.

## What it does

- Discovers and inventories projects in a workspace.
- Maps entry points, data flows, trust boundaries, and cross-project dependencies.
- Audits hidden technical debt and realistic failure modes.
- Selects language/framework-specific checks after detecting the actual stack.
- Includes a dedicated race-condition playbook for async, threads, jobs, and distributed operations.
- Distinguishes evidence-backed findings from hypotheses.
- Assesses test gaps and records tests actually run.
- Produces a cross-project risk register and prioritized remediation roadmap.
- Tracks coverage and checkpoints for large workspaces.

## Safety defaults

- Read-only against application code and runtime state.
- No automatic refactoring or source changes.
- No destructive tests, production fault injection, migrations, or load tests by default.
- No secret values in reports.
- No claim of full coverage without explicit coverage evidence.

## Installation

This repository follows the Agent Skills format: a skill directory containing `SKILL.md` with YAML frontmatter and supporting resources.

### Claude Code

Copy the `failurepath-auditor` directory into your user-level skills directory:

```text
~/.claude/skills/failurepath-auditor/SKILL.md
```

For a project-specific installation, use:

```text
<project>/.claude/skills/failurepath-auditor/SKILL.md
```

On Windows, the user-level directory is typically under `%USERPROFILE%\.claude\skills\failurepath-auditor\`.

Then ask Claude Code to use `failurepath-auditor` to audit the workspace. Follow the current Claude Code documentation if its skill discovery path changes.

### Codex

Copy the directory into:

```text
~/.agents/skills/failurepath-auditor/SKILL.md
```

For a project-specific installation, use:

```text
<project>/.agents/skills/failurepath-auditor/SKILL.md
```

On Windows, the user-level directory is typically `%USERPROFILE%\.agents\skills\failurepath-auditor\`. If your Codex installation is configured to discover skills from `%USERPROFILE%\.codex\skills\`, you can install the same skill there instead.

Codex versions and installations may differ; consult the current Codex skills documentation if your environment uses another discovery path.

### Other Agent Skills-compatible agents

Install the directory wherever your agent searches for Agent Skills. The core skill is plain Markdown with YAML frontmatter and does not depend on a particular vendor API.

## Windows PowerShell installation

From the extracted repository directory, run the following to install for the current user in the shared Agent Skills location:

```powershell
$source = (Resolve-Path .\failurepath-auditor).Path
$target = Join-Path $HOME ".agents\skills\failurepath-auditor"
New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
if (Test-Path $target) { throw "Target already exists; inspect it before replacing: $target" }
Copy-Item -Recurse $source $target
Write-Host "Installed to $target"
```

For Claude Code, change the target parent to `$HOME\.claude\skills`. For a project-local installation, use the relevant `.claude\skills` or `.agents\skills` directory inside that project. Avoid silently overwriting an existing skill.

## Example usage

- "Use failurepath-auditor to inventory and audit every project under this workspace. Start read-only and create a checkpoint."
- "Audit this service for failure-path debt, unsafe retries, state consistency, and missing tests. Do not modify code."
- "Continue the existing FailurePath Auditor checkpoint and audit the next unaudited project."
- "Review the cross-project risk register and validate the top three findings without changing source files."

## Recommended workflow

1. Run discovery and inventory first.
2. Audit critical projects in bounded batches.
3. Validate high-severity findings with safe evidence or tests.
4. Review the coverage report before treating the audit as complete.
5. Remediate findings in a separate task, one coherent change at a time.

## Repository layout

```text
failurepath-auditor/
├── SKILL.md
├── README.md
├── LICENSE
├── .gitignore
├── references/
│   ├── finding-taxonomy.md
│   ├── language-framework-matrix.md
│   └── race-condition-playbook.md
├── templates/
│   ├── finding-template.md
│   ├── project-inventory-template.md
│   └── failure-scenario-template.md
└── scripts/
    └── inventory.py
```

## Language/framework coverage

The included matrix covers common PHP, Java, JavaScript/TypeScript, Python, C#/.NET, Go, Rust, Ruby/Rails, relational databases, frontend, container, and CI/CD patterns. It is a curated checklist, not exhaustive support for every language, framework, or version. Agents must report the stacks actually detected, applicable checks performed, and gaps.

## Limitations

The skill guides an agent's audit process; it cannot guarantee detection of every defect. Runtime evidence, production-like environments, domain knowledge, and independent verification may be required. Security severity and dependency status must be grounded in evidence rather than guesswork.

## Contributing

Contributions should improve reproducibility, evidence quality, safety, and cross-agent compatibility. Avoid adding vendor-specific assumptions to the core skill unless clearly marked as optional.

## License

MIT. See `LICENSE`.
