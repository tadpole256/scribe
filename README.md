# Scribe

Scribe is a small, open-source toolkit that helps Hermes and OpenClaw agents generate and maintain useful documentation for real codebases.

It installs a portable `SKILL.md` workflow. The agent inspects the source repository, identifies audiences, writes Diataxis-structured docs, and validates links and claims before calling the work complete.

## Why Scribe

Most generated documentation fails because it skips the codebase analysis and writes one generic document for everyone. Scribe asks the agent to work from evidence and separates documentation by reader need:

- **Tutorials** teach by guided practice.
- **How-to guides** solve a specific job.
- **Explanations** describe concepts, choices, and tradeoffs.
- **Reference** provides precise lookup material.

## Install

Scribe requires Python 3.11 or later and works with standard agent skill folders.

```bash
uv tool install scribe-docs
```

To develop from a checkout:

```bash
uv sync --group dev
uv run scribe --help
```

## Start a documentation workspace

```bash
scribe init ./scribe-workspace \
  --source-repo /path/to/source-repository \
  --target-repo /path/to/target-repository \
  --target-dir docs \
  --agents hermes,openclaw
```

That command creates:

```text
scribe-workspace/
  .scribe/workspace.json
  .agents/skills/scribe-docs/SKILL.md
```

Open Hermes or OpenClaw in that workspace and ask it to generate documentation for the configured repository. The installed skill supplies the workflow and completion checks.

To install the skill without workspace metadata:

```bash
scribe skills install --project /path/to/project --agents hermes,openclaw
```

## Agent compatibility

Hermes and OpenClaw both support a skill directory containing a `SKILL.md` file. Scribe uses that shared convention and deliberately avoids framework-specific task engines, private package indexes, vendor credentials, and hosted services.

## Safety and privacy

Scribe instructs agents to inspect source before making claims and to keep code and issue data inside approved repositories. Generated docs remain drafts until the agent validates commands, values, examples, and Markdown links against the source.

## Development

```bash
uv run pytest -q
uv run ruff check .
uv run python -m build
```

## License

Apache-2.0. See [LICENSE](LICENSE).
