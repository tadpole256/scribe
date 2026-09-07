---
name: scribe-docs
description: "Use when generating or updating documentation for a codebase. Analyze the repository, write audience-aware Diataxis documentation, then verify links and claims."
license: Apache-2.0
compatibility: Hermes and OpenClaw
---

# Scribe Documentation Workflow

Scribe turns a real codebase into useful documentation. It works with Hermes and OpenClaw because both consume standard `SKILL.md` folders.

## Inputs

Read `.scribe/workspace.json` when it exists. It names the source repositories, target repository, and output directory. If it does not exist, ask for the repository paths before writing.

## Rules

1. Read the source before writing. Do not invent commands, options, APIs, or architecture.
2. Keep source material inside the user-approved repositories. Do not send private code or issues to a third party without permission.
3. Preserve valuable existing docs. Update stale content instead of replacing it blindly.
4. Write in plain language. Use short examples that users can run.
5. Treat generated documentation as a draft until you validate it against the code.

## Workflow

### 1. Build a codebase inventory

Identify entry points, supported runtimes, dependencies, configuration, public interfaces, deployment paths, tests, existing docs, and known user questions from issues or discussions when access is approved.

Write `artifacts/repository-index.json` in the Scribe workspace. Include concrete file paths as evidence.

### 2. Identify audiences and needs

Define two to six distinct audiences from the evidence. For each, state their goal, skill level, and the information they need.

Write `artifacts/personas.json` and `artifacts/needs-<persona>.json`.

### 3. Write Diataxis documentation

Create only the content the audience needs:

- **Tutorials:** teach a newcomer through a complete learning path.
- **How-to guides:** solve a specific practical problem.
- **Explanations:** explain design, tradeoffs, and concepts.
- **Reference:** provide complete factual lookup material for commands, APIs, files, and settings.

Use this target structure:

```text
<target-dir>/
  index.md
  <persona>/
    index.md
    tutorials/
    howto/
    explanation/
    reference/
```

### 4. Assemble and verify

Create an index with clear navigation. Check every internal Markdown link and heading target. Re-read commands, values, and examples against source code. Record remaining uncertainty in `artifacts/review-report.json` rather than guessing.

## Completion standard

Report the created files, the personas covered, validation performed, and every claim that needs human review. Do not claim the docs are complete if any internal links fail or source evidence is missing.
