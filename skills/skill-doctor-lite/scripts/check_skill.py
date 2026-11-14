#!/usr/bin/env python3
"""技能体检官 · 上架前体检脚本

用法:
    python3 check_skill.py <技能目录 | 技能包.zip> [--fix]

检查对象是 Agent Skills 技能包（目录或 zip）。规则以 WorkBuddy 提审
一手实测为准（2026-11-02，见 references/platform-field-rules.md）：
frontmatter 七字段齐全、英文展示名 ≤60 字符，缺一或超限直接解析失败。
其余项为命名/描述规范与包体统计，逐项输出 通过/警告/失败＋修法。

--fix（仅目录对象）：自动补齐缺失字段骨架、把超限英文名截到 60 字符内，
改完自动重跑体检。骨架值带「待填写」字样，体检会以警告提醒人工替换。

仅用标准库。退出码：0 = 无失败项，1 = 有失败项或用法错误。
"""
import os
import re
import sys
import zipfile

EN_NAME_LIMIT = 60

# (字段名, 中文名, 修法) —— 前两个是 Agent Skills 标准字段，
# 后五个是 WorkBuddy 提审解析必填（2026-11-02 一手实测）。
FIELDS = [
    ("name", "技能英文名（包内标识）",
     "在 frontmatter 补 `name: your-skill-name`（小写连字符命名）。"),
    ("description", "技能描述（标准字段）",
     "在 frontmatter 补 `description: 一句话说清何时用这个技能`。"),
    ("version", "Skill 版本号",
     "在 frontmatter 补 `version: \"1.0.0\"`（WorkBuddy 提审必填，缺失直接解析失败）。"),
    ("display_name", "Skill 中文展示名",
     "在 frontmatter 补 `display_name: \"你的技能中文展示名\"`（WorkBuddy 提审必填）。"),
    ("display_name_en", "Skill 英文展示名",
     "在 frontmatter 补 `display_name_en: \"Your Skill Display Name\"`（WorkBuddy 提审必填，且 ≤60 字符）。"),
    ("description_zh", "Skill 中文描述",
     "在 frontmatter 补 `description_zh: \"中文一句话描述\"`（WorkBuddy 提审必填）。"),
    ("description_en", "Skill 英文描述",
     "在 frontmatter 补 `description_en: \"One-line English description\"`（WorkBuddy 提审必填）。"),
]
DESC_FIELDS = ["description", "description_zh", "description_en"]
HYPHEN_CASE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
KEY_LINE = re.compile(r"^([A-Za-z0-9_]+):\s*(.*)$")
SKELETON_MARKS = ("待填写", "todo", "待补充", "to fill")


class Report:
    def __init__(self):
        self.items = []  # (level, title, detail) level: ok|warn|fail

    def ok(self, title, detail=""):
        self.items.append(("ok", title, detail))

    def warn(self, title, detail=""):
        self.items.append(("warn", title, detail))

    def fail(self, title, detail=""):
        self.items.append(("fail", title, detail))

    @property
    def fails(self):
        return [i for i in self.items if i[0] == "fail"]

    @property
    def warns(self):
        return [i for i in self.items if i[0] == "warn"]


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def parse_frontmatter(text):
    """返回 (fields dict, body_start_line_index, raw_lines)；无 frontmatter 返回 None。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None
    fields = {}
    for line in lines[1:end]:
        m = KEY_LINE.match(line)
        if m:
            fields[m.group(1)] = unquote(m.group(2))
    return fields, end, lines


def truncate_en_name(name, limit=EN_NAME_LIMIT):
    """按词边界截断到 limit 字符内，返回建议稿。"""
    if len(name) <= limit:
        return name
    cut = name[:limit]
    if " " in cut:
        cut = cut[:cut.rfind(" ")].rstrip(" :,-")
    return cut


def collect_from_dir(path):
    """目录对象：返回 (skill_md_path, files[(relpath, size)], structure_desc)。"""
    files = []
    for root, _dirs, names in os.walk(path):
        for n in sorted(names):
            full = os.path.join(root, n)
            files.append((os.path.relpath(full, path), os.path.getsize(full)))
    skill_md = None
    structure = ""
    if os.path.isfile(os.path.join(path, "SKILL.md")):
        skill_md = os.path.join(path, "SKILL.md")
        structure = "目录（SKILL.md 在根目录）"
    else:
        subs = [d for d in sorted(os.listdir(path))
                if os.path.isdir(os.path.join(path, d))
                and os.path.isfile(os.path.join(path, d, "SKILL.md"))]
        if len(subs) == 1:
            skill_md = os.path.join(path, subs[0], "SKILL.md")
            structure = f"目录（单顶层目录 {subs[0]}/）"
    return skill_md, files, structure


def collect_from_zip(path):
    """zip 对象：返回 (skill_md_text, files[(name, size)], structure_desc)。"""
    z = zipfile.ZipFile(path)
    infos = [i for i in z.infolist() if not i.is_dir()]
    files = [(i.filename, i.file_size) for i in infos]
    skill_text = None
    structure = ""
    names = [i.filename for i in infos]
    if "SKILL.md" in names:
        skill_text = z.read("SKILL.md").decode("utf-8", errors="replace")
        structure = "zip 包（平铺结构，SKILL.md 在根目录）"
    else:
        tops = sorted({n.split("/")[0] for n in names})
        for t in tops:
            if f"{t}/SKILL.md" in names:
                skill_text = z.read(f"{t}/SKILL.md").decode("utf-8", errors="replace")
                if len(tops) == 1:
                    structure = f"zip 包（单顶层目录 {t}/）"
                else:
                    structure = f"zip 包（多顶层目录，SKILL.md 在 {t}/ 下）"
                break
    return skill_text, files, structure


def run_checks(rep, skill_text, files, structure, has_scripts):
    # ---- 包体概况 ----
    total = sum(s for _n, s in files)
    biggest = max(files, key=lambda x: x[1]) if files else ("-", 0)
    rep.ok("包体统计",
           f"结构：{structure}；文件数：{len(files)}；总大小：{total/1024:.1f} KB；"
           f"最大文件：{biggest[0]}（{biggest[1]/1024:.1f} KB）")
    if len(files) <= 1:
        rep.warn("包内只有一个文件",
                 "只有 SKILL.md 的纯提示词技能可以上架，但带脚本/参考文件的技能更耐用（经验提示）。")

    # ---- SKILL.md 与 frontmatter ----
    if skill_text is None:
        rep.fail("未找到 SKILL.md",
                 "修法：技能包根目录（或单顶层目录内）必须有 SKILL.md，它是技能包的入口文件。")
        return
    rep.ok("SKILL.md 存在")
    parsed = parse_frontmatter(skill_text)
    if parsed is None:
        rep.fail("SKILL.md 没有合法 frontmatter",
                 "修法：文件最上方加 YAML frontmatter：第一行 `---`，逐行写 `字段: 值`，再以一行 `---` 收尾。")
        return
    fields, _end, _lines = parsed
    rep.ok("frontmatter 存在")

    # ---- 七字段齐全 ----
    for key, cn, fix in FIELDS:
        if key not in fields or not fields[key].strip():
            rep.fail(f"frontmatter 缺少字段 {key}（{cn}）", f"修法：{fix}")
        else:
            rep.ok(f"字段 {key} 齐全")

    # ---- 英文展示名字符数 ----
    en = fields.get("display_name_en", "")
    if en:
        n = len(en)
        if n > EN_NAME_LIMIT:
            rep.fail(f"display_name_en 超长：当前 {n} 字符，上限 {EN_NAME_LIMIT} 字符",
                     f"修法：删减到 {EN_NAME_LIMIT} 字符内。截断建议稿（{len(truncate_en_name(en))} 字符）："
                     f"`{truncate_en_name(en)}`，或运行 `check_skill.py <目录> --fix` 自动截断。")
        else:
            rep.ok(f"display_name_en 长度 {n} 字符（上限 {EN_NAME_LIMIT}）")
        if any(ord(c) > 127 for c in en):
            rep.warn("display_name_en 含非 ASCII 字符",
                     "英文展示名建议纯 ASCII，避免平台解析或展示异常（经验提示）。")

    # ---- name 命名规范 ----
    name = fields.get("name", "")
    if name:
        if HYPHEN_CASE.match(name):
            rep.ok(f"name 命名规范（hyphen-case）：{name}")
        else:
            rep.fail(f"name 不是 hyphen-case：{name}",
                     "修法：改成全小写字母＋数字＋连字符，如 `my-skill-name`，不要用大写、下划线或空格。")

    # ---- 描述无尖括号 ----
    for key in DESC_FIELDS:
        v = fields.get(key, "")
        if v and ("<" in v or ">" in v):
            rep.fail(f"{key} 含尖括号 < >",
                     "修法：删掉描述里的尖括号（占位符改用中文括号或直接写文字），尖括号会触发 frontmatter 校验失败。")
    desc_all = [k for k in DESC_FIELDS if fields.get(k) and "<" not in fields[k] and ">" not in fields[k]]
    if desc_all:
        rep.ok("描述字段无尖括号（已查：" + "、".join(desc_all) + "）")

    # ---- 骨架值提醒 ----
    for key, cn, _fix in FIELDS:
        v = fields.get(key, "")
        if v and any(m in v.lower() for m in SKELETON_MARKS):
            rep.warn(f"字段 {key} 还是骨架值",
                     f"「{v}」是自动补的占位内容，上架前替换成真实{cn}。")

    # ---- version 格式 ----
    ver = fields.get("version", "")
    if ver and not SEMVER.match(ver):
        rep.warn(f"version 格式不是 x.y.z：{ver}",
                 "建议写成 `1.0.0` 这样的三段版本号（经验提示，非平台明文规则）。")

    # ---- description 长度 ----
    d = fields.get("description", "")
    if d and len(d) < 20:
        rep.warn("description 过短（<20 字符）",
                 "描述是智能体判断何时调用技能的依据，写清「何时用＋做什么」（经验提示）。")

    # ---- scripts 目录 ----
    if not has_scripts:
        rep.warn("未发现 scripts/ 目录",
                 "纯提示词技能可忽略；带检查/生成脚本的技能更可信，也更难被替代（经验提示）。")


def apply_fix(dir_path):
    """对目录对象的 SKILL.md 自动修复；返回修复说明列表。"""
    skill_md, _files, _s = collect_from_dir(dir_path)
    if skill_md is None:
        return ["无法修复：未找到 SKILL.md"]
    text = open(skill_md, encoding="utf-8").read()
    parsed = parse_frontmatter(text)
    notes = []
    if parsed is None:
        skeleton = ["---", 'name: "待填写技能英文名"', 'description: "待填写技能描述"',
                    'version: "1.0.0"', 'display_name: "待填写中文展示名"',
                    'display_name_en: "Skill Name To Fill"', 'description_zh: "待填写中文描述"',
                    'description_en: "Description to fill in"', "---", ""]
        open(skill_md, "w", encoding="utf-8").write("\n".join(skeleton) + text)
        return ["已新建 frontmatter 骨架（全部为待填写占位，务必人工替换）"]
    fields, end, lines = parsed
    inserts = []
    skeleton_values = {
        "version": '"1.0.0"',
        "display_name": '"待填写中文展示名"',
        "display_name_en": '"Name To Fill In"',
        "description_zh": '"待填写中文描述（可由 description 改写）"',
        "description_en": '"Description to fill in"',
        "name": '"待填写技能英文名"',
        "description": '"待填写技能描述"',
    }
    for key, _cn, _fix in FIELDS:
        if key not in fields or not fields[key].strip():
            inserts.append(f"{key}: {skeleton_values[key]}")
            notes.append(f"已补字段骨架：{key}（占位值待人工替换）")
    en = fields.get("display_name_en", "")
    if en and len(en) > EN_NAME_LIMIT:
        new_en = truncate_en_name(en)
        for i in range(1, end):
            if lines[i].startswith("display_name_en:"):
                lines[i] = f'display_name_en: "{new_en}"'
                break
        notes.append(f"已截断 display_name_en：{len(en)} → {len(new_en)} 字符（{new_en}）")
    if inserts:
        lines = lines[:end] + inserts + lines[end:]
    if notes:
        open(skill_md, "w", encoding="utf-8").write("\n".join(lines) + ("\n" if not text.endswith("\n") else ""))
    return notes


def print_report(target, rep):
    print("# 技能体检报告")
    print(f"对象：{target}")
    print()
    icons = {"ok": "✅ [通过]", "warn": "⚠️ [警告]", "fail": "❌ [失败]"}
    for level, title, detail in rep.items:
        print(f"{icons[level]} {title}")
        if detail:
            print(f"   {detail}")
    print()
    print("## 体检结论")
    if rep.fails:
        print(f"❌ 不可上架：{len(rep.fails)} 项失败、{len(rep.warns)} 项警告。"
              "先按上面修法逐项改完，再跑一次体检清零。")
    elif rep.warns:
        print(f"✅ 可上架：0 项失败、{len(rep.warns)} 项警告。警告不拦上架，建议顺手处理。")
    else:
        print("✅ 可上架：全部通过，无警告。")
    return 1 if rep.fails else 0


def main():
    args = [a for a in sys.argv[1:] if a != "--fix"]
    do_fix = "--fix" in sys.argv[1:]
    if len(args) != 1:
        print("用法: python3 check_skill.py <技能目录 | 技能包.zip> [--fix]")
        return 1
    target = args[0]
    if do_fix:
        if not os.path.isdir(target):
            print("--fix 只支持目录对象；zip 包请先解压再修复。")
            return 1
        notes = apply_fix(target)
        print("## 自动修复")
        for n in notes or ["无可自动修复项"]:
            print(f"- {n}")
        print()
    rep = Report()
    if os.path.isdir(target):
        skill_md, files, structure = collect_from_dir(target)
        skill_text = open(skill_md, encoding="utf-8").read() if skill_md else None
        has_scripts = any(n.split("/")[0].endswith("scripts") or "/scripts/" in n or n.startswith("scripts/")
                          for n, _s in files)
        run_checks(rep, skill_text, files, structure, has_scripts)
    elif target.endswith(".zip") and os.path.isfile(target):
        skill_text, files, structure = collect_from_zip(target)
        has_scripts = any("/scripts/" in n or n.startswith("scripts/") for n, _s in files)
        run_checks(rep, skill_text, files, structure, has_scripts)
    else:
        print(f"对象不存在或不支持：{target}（需要技能目录或 .zip 包）")
        return 1
    return print_report(target, rep)


if __name__ == "__main__":
    sys.exit(main())
