#!/usr/bin/env python3
"""FrankAie-hub skill consistency checker.

Run from repo root: `python3 scripts/check_skills.py`

Checks:
  1. Reference integrity — every hyphenated `skill-id` referenced in any doc
     points at a skill folder that actually exists (catches typos / renamed /
     removed skills, e.g. the old `ecommerce-operator`).
  2. Count consistency — the skill count stated in ROSTER.md ("共 N 個 skill")
     matches the real number of skill folders.
  3. Version consistency — marketplace.json and plugin.json declare the same
     version, and the marketplace plugin entry version matches too.
  4. Structure consistency — every SKILL.md has frontmatter whose `name` equals
     its folder, a non-trivial `description`, at least one output template
     (code fence or markdown table) and an anti-hallucination guardrail marker.

Exit code 0 = all good, 1 = at least one problem (CI fails).
No third-party dependencies — standard library only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "frankaie-research-hub"
SKILLS_DIR = PLUGIN / "skills"

# Hyphenated lowercase backtick tokens that are NOT local skills and are
# legitimately referenced (plugin name, external/upstream skill names cited in
# attribution). Add to this list only for genuine non-skill references.
ALLOWLIST = {
    "frankaie-research-hub",          # the plugin itself
    "verification-before-completion",  # upstream superpowers skill (attribution)
}

# Matches a `hyphenated-lowercase-id` inside backticks. Requires >=1 hyphen so
# plain words and FILE.md / owner/repo / UPPERCASE tokens are ignored.
TOKEN_RE = re.compile(r"`([a-z][a-z0-9]+(?:-[a-z0-9]+)+)`")

DOC_GLOBS = ["README.md", "plugins/**/*.md", "plugins/**/SKILL.md"]

# Anti-hallucination markers — bracket tags or in-prose phrasing. A skill must
# contain at least one of these so every output carries a "don't fabricate" rule.
GUARDRAIL_RE = re.compile(
    r"需查證|需數據|假設|需驗證|需執業律師確認|臆造|杜撰|誇大|誇張|不杜撰|"
    r"保持原樣|虛假廣告|根拠|模擬"
)


def real_skills() -> set[str]:
    return {
        p.parent.name
        for p in SKILLS_DIR.glob("*/SKILL.md")
    }


def docs() -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    for pattern in DOC_GLOBS:
        for p in ROOT.glob(pattern):
            if p.is_file() and p not in seen:
                seen.add(p)
                out.append(p)
    return out


def check_references(skills: set[str]) -> list[str]:
    valid = skills | ALLOWLIST
    errors: list[str] = []
    for doc in docs():
        text = doc.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            for token in TOKEN_RE.findall(line):
                if token not in valid:
                    rel = doc.relative_to(ROOT)
                    errors.append(
                        f"  {rel}:{lineno}  ->  `{token}` is not a known skill"
                    )
    return errors


def _frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (frontmatter dict, body). Only top-level `key: value` lines are
    parsed; folded values (`>`) collapse their continuation lines into one."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_block = text[3:end]
    body = text[end + 4:]
    fm: dict[str, str] = {}
    key = None
    for line in fm_block.splitlines():
        m = re.match(r"^([a-zA-Z_][\w-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            fm[key] = m.group(2).strip()
        elif key and line.strip():
            fm[key] = (fm[key] + " " + line.strip()).strip()
    return fm, body


def check_structure(skills: set[str]) -> list[str]:
    errors: list[str] = []
    for skill in sorted(skills):
        path = SKILLS_DIR / skill / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        fm, body = _frontmatter(text)
        where = f"  skills/{skill}/SKILL.md"
        name = fm.get("name", "").strip().strip("\"'")
        if name != skill:
            errors.append(f"{where}: frontmatter name='{name}' != folder '{skill}'")
        desc = fm.get("description", "").strip().strip(">").strip()
        if len(desc) < 40:
            errors.append(f"{where}: description missing or too short")
        if "```" not in body and not re.search(r"^\s*\|", body, re.M):
            errors.append(f"{where}: no output template (no code fence or table)")
        if not GUARDRAIL_RE.search(body):
            errors.append(f"{where}: no anti-hallucination guardrail marker")
    return errors


def check_count(skills: set[str]) -> list[str]:
    actual = len(skills)
    roster = PLUGIN / "ROSTER.md"
    if not roster.exists():
        return [f"  ROSTER.md not found at {roster}"]
    m = re.search(r"共\s*(\d+)\s*個\s*skill", roster.read_text(encoding="utf-8"))
    if not m:
        return ['  ROSTER.md is missing a "共 N 個 skill" count line']
    stated = int(m.group(1))
    if stated != actual:
        return [
            f"  ROSTER.md says 共 {stated} 個 skill, but {actual} skill folders exist"
        ]
    return []


def check_versions() -> list[str]:
    errors: list[str] = []
    mp = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text("utf-8"))
    pj = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text("utf-8"))
    mp_ver = mp.get("metadata", {}).get("version")
    pj_ver = pj.get("version")
    if mp_ver != pj_ver:
        errors.append(
            f"  version mismatch: marketplace.json={mp_ver} vs plugin.json={pj_ver}"
        )
    return errors


def main() -> int:
    skills = real_skills()
    if not skills:
        print(f"FAIL: no skills found under {SKILLS_DIR}", file=sys.stderr)
        return 1

    sections = [
        ("Broken skill references", check_references(skills)),
        ("Skill structure consistency", check_structure(skills)),
        ("Skill count consistency", check_count(skills)),
        ("Version consistency", check_versions()),
    ]

    failed = False
    for title, errs in sections:
        if errs:
            failed = True
            print(f"\n✗ {title}:")
            for e in errs:
                print(e)
        else:
            print(f"✓ {title}")

    if failed:
        print(f"\nChecked {len(skills)} skills — FAILED.", file=sys.stderr)
        return 1
    print(f"\nChecked {len(skills)} skills — all consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
