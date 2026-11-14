---
name: agents-md-forge-lite
description: Give your AI coding assistant (Claude Code, Codex, Cursor, WorkBuddy) a project rulebook so it stops rambling and rewriting files it should not touch. Scans your project, then fills three ready-to-use templates — a global rules file, a project AGENTS.md, and a task-contract/acceptance checklist. Lite edition of AGENTS.md Forge.
version: "1.0.0"
display_name: "给AI立规矩（精简版）：用三份模板生成项目AGENTS.md"
display_name_en: "AGENTS.md Forge Lite: Project Rules from 3 Templates"
description_zh: "AI写代码废话多、爱乱改？精简版用三份模板（全局规矩＋项目AGENTS.md＋任务合同）给它立规矩，扫描项目后直接套用。"
description_en: "AI assistant rambling and rewriting the wrong files? The Lite edition generates a global rules file, a project AGENTS.md and a task contract from three field-tested templates, filled in from a scan of your project."
---

# AGENTS.md Forge — Lite Edition

Turn "my AI writes too much and changes the wrong things" into three files:

1. `global-agents.md` — global rules (set up once, applies to every project)
2. `AGENTS.md` — project-specific rules (lives in your project root)
3. `task-contract.md` — a contract + acceptance checklist for each task you delegate

## Workflow

### Step 1: Scan the project (read-only)

Extract the project fingerprint: language and version, build tool, module/directory layout,
existing README and config files, test framework, and any existing AGENTS.md
(if one exists, merge into it — never silently overwrite).

### Step 2: Fill the three templates in `assets/`

- `assets/global-agents-template.md` — usually delivered as-is.
- `assets/project-agents-template.md` — fill every section from the fingerprint.
- `assets/task-contract-template.md` — deliver as the per-task hand-off sheet.

Hard rules while filling:

- Project AGENTS.md stays under 120 lines; every rule must be executable and verifiable.
  Delete any "pay attention to code quality" style filler.
- The "Never do this" section comes first, and every item in it must come from a real
  incident or the real project structure — no generic lists.
- No real accounts, passwords or secrets in the output; clear all placeholders before delivery.

### Step 3: Verify with a small task

Run one task of under ~50 lines with the new rules and watch three signals:
the assistant plans before editing, stays out of the forbidden zones, and shows
evidence when done. If a signal fails, add exactly one rule for that failure —
do not start over.

## Lite vs Full

This Lite edition is the template core. The full edition adds:

- A 12-question interview flow for projects that cannot be scanned (or founders
  who only have an idea so far)
- An automated validation script that checks the generated AGENTS.md
  (sections complete, no leftover placeholders, line budget)
- Anti-redundancy rules and quality gates used to review every generated file
- A worked example output

Full edition: see the link in the repository README.
