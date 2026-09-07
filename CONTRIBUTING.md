# Contributing to Scribe

Thank you for improving Scribe.

## Development setup

```bash
uv sync --group dev
uv run pytest -q
uv run ruff check .
```

## Contribution rules

- Keep agent instructions portable. Do not require private services, credentials, or a specific employer's tools.
- Test behavior before changing production Python code.
- Base generated-documentation claims on source evidence.
- Do not add telemetry or transmit repository contents without an explicit, documented opt-in.
- Keep changes small and explain user-facing effects in the pull request.

## Pull requests

Use a focused branch, include tests for behavior changes, and confirm that the complete test suite and Ruff checks pass.
