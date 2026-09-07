"""The Scribe command-line interface."""

from pathlib import Path
from typing import Annotated

import typer

from .workspace import SUPPORTED_AGENTS, initialize_workspace, install_skills

app = typer.Typer(help="Portable documentation-generation skills for coding agents.")
skills_app = typer.Typer(help="Install Scribe skills in a project.")
app.add_typer(skills_app, name="skills")


def _agents(value: str) -> list[str]:
    agents = [part.strip().lower() for part in value.split(",") if part.strip()]
    unknown = sorted(set(agents) - SUPPORTED_AGENTS)
    if unknown:
        raise typer.BadParameter(f"unsupported agent(s): {', '.join(unknown)}")
    return agents


@app.command()
def init(
    project_dir: Annotated[Path, typer.Argument(help="Directory for Scribe workspace state")],
    source_repo: Annotated[list[Path], typer.Option("--source-repo", help="Repository to document")],
    target_repo: Annotated[Path, typer.Option("--target-repo", help="Repository that receives documentation")],
    target_dir: Annotated[str, typer.Option(help="Relative output directory within target repository")] = "docs",
    agents: Annotated[str, typer.Option(help="Comma-separated: hermes,openclaw")] = "hermes,openclaw",
) -> None:
    """Create agent-neutral workspace metadata and install the Scribe skill."""
    selected_agents = _agents(agents)
    manifest = initialize_workspace(project_dir, source_repo, target_repo, target_dir, selected_agents)
    installed = install_skills(project_dir, selected_agents)
    typer.echo(f"Created {manifest}")
    typer.echo(f"Installed {installed[0]}")


@skills_app.command("install")
def skills_install(
    project_dir: Annotated[Path | None, typer.Option("--project", help="Project directory")] = None,
    agents: Annotated[str, typer.Option(help="Comma-separated: hermes,openclaw")] = "hermes,openclaw",
) -> None:
    """Install the portable Scribe skill without creating workspace state."""
    installed = install_skills(project_dir or Path.cwd(), _agents(agents))
    typer.echo(f"Installed {installed[0]}")
