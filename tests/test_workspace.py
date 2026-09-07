import json
from pathlib import Path

from scribe.workspace import initialize_workspace, install_skills


def test_initialize_workspace_writes_a_portable_manifest(tmp_path: Path) -> None:
    source = tmp_path / "source-repo"
    target = tmp_path / "target-repo"
    source.mkdir()
    target.mkdir()

    manifest_path = initialize_workspace(
        project_dir=tmp_path / "workspace",
        source_repos=[source],
        target_repo=target,
        target_dir="documentation",
        agents=["hermes", "openclaw"],
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["source_repos"] == [str(source.resolve())]
    assert manifest["target_repo"] == str(target.resolve())
    assert manifest["target_dir"] == "documentation"
    assert manifest["agents"] == ["hermes", "openclaw"]
    assert manifest["schema_version"] == 1


def test_install_skills_creates_a_standard_skill_folder(tmp_path: Path) -> None:
    installed = install_skills(project_dir=tmp_path, agents=["hermes", "openclaw"])

    skill_file = tmp_path / ".agents" / "skills" / "scribe-docs" / "SKILL.md"
    assert installed == [skill_file]
    text = skill_file.read_text(encoding="utf-8")
    assert text.startswith("---\nname: scribe-docs\n")
    assert "Diataxis" in text
    assert "Hermes" in text
    assert "OpenClaw" in text


def test_initialize_workspace_rejects_a_target_dir_that_escapes_the_repo(tmp_path: Path) -> None:
    source = tmp_path / "source-repo"
    target = tmp_path / "target-repo"
    source.mkdir()
    target.mkdir()

    try:
        initialize_workspace(
            project_dir=tmp_path / "workspace",
            source_repos=[source],
            target_repo=target,
            target_dir="../outside",
            agents=["hermes"],
        )
    except ValueError as error:
        assert "target_dir" in str(error)
    else:
        raise AssertionError("expected an invalid target directory to be rejected")
