---
name: skill-doctor-lite
description: Pre-flight check for Agent Skills packages before you submit them to a skill platform. Runs scripts/check_skill.py on a skill directory or zip and reports pass/warn/fail per item — required frontmatter fields, naming rules, angle brackets in descriptions, package structure and size — so you fix parse errors before the platform bounces your submission. Lite edition of Skill Doctor.
version: "1.0.0"
display_name: "技能体检官（精简版）：上架前给技能包做全检"
display_name_en: "Skill Doctor Lite: Pre-Flight Check for Skill Packs"
description_zh: "技能包提审总被平台报错退回？精简版在上架前体检：必填字段、命名规范、包结构一次查清，逐项输出通过/警告/失败。"
description_en: "Skill pack submissions bounced by cryptic parse errors? The Lite edition checks required frontmatter fields, naming rules and package structure before you submit, with pass/warn/fail per item."
---

# Skill Doctor — Lite Edition

Skill packs usually get rejected for packaging, not quality: one missing field or an
over-long display name and the whole submission bounces. This skill checks the pack
before the platform does:

- Are all required frontmatter fields present?
  (`name`, `description`, `version`, `display_name`, `display_name_en`,
  `description_zh`, `description_en`)
- Is `name` valid hyphen-case, and free of characters that break parsers?
- Does any description contain angle brackets?
- Package structure and size overview (file count, total size, largest file)

## Workflow

### Step 1: Run the checker

```bash
python3 scripts/check_skill.py <skill-directory-or-zip-path>
```

Exit code 0 = no failures, 1 = failures present. Treat the script output as the
source of truth — do not re-judge items by eye.

### Step 2: Read the report, failures first

For each failed item the report names the field and the problem. Fix failures in
your SKILL.md frontmatter, then re-run until failures reach zero. Warnings do not
block submission but are worth a quick pass.

### Step 3: Submit

With 0 failures, follow your platform's submission flow. If the platform still
rejects the pack with a new error, keep the exact error text — it usually points
at one specific field.

## Lite vs Full

This Lite edition is the checker plus this workflow. The full edition adds:

- The platform field-rules reference: per-platform limits and formatting rules
  (including hard-won submission findings, e.g. the 60-character English
  display-name cap measured on WorkBuddy in Nov 2026)
- The guided fix playbook: which failures can be auto-fixed, how to scaffold
  missing fields, and how to re-check to zero
- A self-test pack for verifying the checker itself

Full edition: see the link in the repository README.
