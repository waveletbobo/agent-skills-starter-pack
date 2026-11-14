# Agent Skills Starter Pack — Free Lite Edition

Two field-tested Agent Skills for people who build with AI coding assistants
(Claude Code, Codex, Cursor, WorkBuddy, and other Agent Skills–compatible tools).
This repository is the **free Lite edition** of both skills — the working core,
no signup required to download.

## What's inside (exactly 2 skills)

| Skill | What it does | Lite includes | Full edition adds |
|---|---|---|---|
| **AGENTS.md Forge Lite** (`skills/agents-md-forge-lite/`) | Stops your AI assistant rambling and rewriting the wrong files: scans your project and generates a global rules file, a project `AGENTS.md`, and a task-contract checklist from 3 templates | SKILL.md workflow + all 3 templates | 12-question interview flow for unscannable projects, automated AGENTS.md validation script, anti-redundancy rules + quality gates, worked example |
| **Skill Doctor Lite** (`skills/skill-doctor-lite/`) | Pre-flight check for Agent Skills packages before platform submission: required frontmatter fields, naming rules, package structure — pass/warn/fail per item | SKILL.md workflow + the checker script (`scripts/check_skill.py`) | Platform field-rules reference (incl. measured submission limits), guided fix playbook with auto-fix flow, self-test pack |

## Quick start

1. Copy a skill folder into your tool's skills directory, e.g. for Claude Code:

   ```bash
   cp -r skills/agents-md-forge-lite ~/.claude/skills/
   cp -r skills/skill-doctor-lite ~/.claude/skills/
   ```

   (For Codex / Cursor / WorkBuddy, use that tool's documented skills folder —
   the package format is the same `SKILL.md` + folders layout.)

2. In your project, ask your assistant to use the skill:
   - "Use agents-md-forge-lite to set up an AGENTS.md for this project."
   - "Use skill-doctor-lite to check my skill package at ./my-skill before I submit it."

Both skills are bilingual (English / 中文）: instructions and templates work in
either language.

## Full edition

The full edition (both complete skills, one bundle) is **¥9.9, one-time payment**
— not a subscription. Our current payment channels only support one-time
payments, so that is the honest format. Checkout is not open yet; the first
release goes to the waitlist first:

**Join the waitlist:** https://gate.wuqiongzhiwai.com/skillpack

## Why free Lite?

These two skills were built for real projects first and sold second. The Lite
editions are genuinely usable — if they save you one bad AI edit or one rejected
submission, the full edition is there when you want the interview flow, the
validation tooling and the platform rules reference.

## License

The Lite editions in this repository are released under the MIT License
(see `LICENSE`). The full editions are a paid product and are not covered by
this license.

---

中文说明：本仓库是两个 Agent Skills 的免费精简版——「给AI立规矩」（生成项目
AGENTS.md）和「技能体检官」（上架前提检技能包）。完整版为两件套 ¥9.9 一次性
买断（非订阅，收款通道目前只支持一次性付款），候补名单见上方链接。
