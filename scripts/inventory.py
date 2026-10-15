#!/usr/bin/env python3
"""Read-only, standard-library project inventory helper.

Usage:
    python scripts/inventory.py [workspace-root] [--output inventory.md]

This helper identifies likely project markers; it does not prove that every
folder is an active project. Generated/vendor directories are skipped by default.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build",
    "coverage", ".next", ".nuxt", ".venv", "venv", "env", "__pycache__",
    ".mypy_cache", ".pytest_cache", "target", "bin", "obj", "out", "Pods",
}
MARKERS = {
    "package.json": "Node.js / JavaScript",
    "pyproject.toml": "Python",
    "requirements.txt": "Python",
    "Pipfile": "Python",
    "Cargo.toml": "Rust",
    "go.mod": "Go",
    "pom.xml": "Java / Maven",
    "build.gradle": "Java/Kotlin / Gradle",
    "build.gradle.kts": "Kotlin/Gradle",
    "composer.json": "PHP / Composer",
    "Gemfile": "Ruby",
    "*.csproj": ".NET",
    "*.sln": ".NET solution",
    "Dockerfile": "Containerized application",
    "docker-compose.yml": "Docker Compose",
    "compose.yml": "Docker Compose",
    "Makefile": "Make-based project",
    "go.work": "Go workspace",
    "Cargo.lock": "Rust lockfile",
}


def discover(root: Path) -> dict[Path, set[str]]:
    found: dict[Path, set[str]] = {}
    for current, dirs, names in os.walk(root):
        current_path = Path(current)
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        files = set(names)
        markers: set[str] = set()
        for marker, label in MARKERS.items():
            if marker.startswith("*"):
                if any(name.endswith(marker[1:]) for name in files):
                    markers.add(label)
            elif marker in files:
                markers.add(label)
        if markers or ".git" in dirs or ".git" in files:
            found[current_path] = markers or {"Repository / project marker"}
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Workspace root")
    parser.add_argument("--output", help="Optional Markdown output path")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"Not a directory: {root}")
    projects = discover(root)
    lines = [
        f"# Project discovery inventory: {root}", "",
        "> Heuristic inventory only. Verify project boundaries and inspect ignored directories if relevant.", "",
        f"Candidate directories found: **{len(projects)}**", "",
        "| Candidate path | Detected markers |", "|---|---|",
    ]
    for path, markers in sorted(projects.items(), key=lambda item: str(item[0]).lower()):
        rel = "." if path == root else str(path.relative_to(root)).replace("|", "\\|")
        lines.append(f"| {rel} | {', '.join(sorted(markers))} |")
    lines.append("")
    result = "\n".join(lines)
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.exists():
            parser.error(f"Refusing to overwrite existing file: {output}")
        output.write_text(result, encoding="utf-8")
        print(f"Wrote {output}")
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
