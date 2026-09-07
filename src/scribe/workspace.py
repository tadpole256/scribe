"""Workspace initialization and portable agent-skill installation."""

from __future__ import annotations

import json
import shutil
from collections.abc import Iterable
from pathlib import Path

SKILL_NAME = "scribe-docs"
SUPPORTED_AGENTS = {"hermes", "openclaw"}


def _normalise_agents(agents: Iterable[str]) -> list[str]:
    selected = list(dict.fromkeys(agent.lower() for agent in agents))
    unknown = sorted(set(selected) - SUPPORTED_AGENTS)
    if unknown:
        raise ValueError(f"unsupported agent(s): {', '.join(unknown)}")
    if not selected:
        raise ValueError("at least one agent is required")
    return selected


def _validate_target_dir(target_dir: str) -> str:
    path = Path(target_dir)
    if path.is_absolute() or ".." in path.parts or target_dir in {"", "."}:
        raise ValueError("target_dir must be a non-empty relative directory within target_repo")
    return path.as_posix()


def initialize_workspace(
    project_dir: Path,
    source_repos: Iterable[Path],
    target_repo: Path,
    target_dir: str = "docs",
    agents: Iterable[str] = ("hermes", "openclaw"),
) -> Path:
    """Write a portable, agent-neutral workspace manifest."""
    selected_agents = _normalise_agents(agents)
    safe_target_dir = _validate_target_dir(target_dir)
    sources = [str(Path(source).resolve()) for source in source_repos]
    if not sources:
        raise ValueError("at least one source repository is required")

    project_dir = Path(project_dir)
    manifest_path = project_dir / ".scribe" / "workspace.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "source_repos": sources,
        "target_repo": str(Path(target_repo).resolve()),
        "target_dir": safe_target_dir,
        "agents": selected_agents,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def install_skills(project_dir: Path, agents: Iterable[str] = ("hermes", "openclaw")) -> list[Path]:
    """Install Scribe's SKILL.md in a skills.sh-compatible project location.

    Hermes and OpenClaw both consume a directory containing SKILL.md. The
    installed skill uses no framework-specific commands, so one copy works for
    both supported agents.
    """
    _normalise_agents(agents)
    project_dir = Path(project_dir)
    destination = project_dir / ".agents" / "skills" / SKILL_NAME / "SKILL.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).parent / "skills" / SKILL_NAME / "SKILL.md"
    shutil.copyfile(source, destination)
    return [destination]
