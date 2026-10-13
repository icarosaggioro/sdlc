#!/usr/bin/env python3
"""Validate package/ before a release. Exit code 1 when anything is wrong.

Checks
  - required files exist
  - guides 00..16 are present and contiguous
  - every sdlc-* skill has valid frontmatter and is listed in instructions.md (and vice versa)
  - no leftovers that do not belong in a copy-in package (evidence links, Windows-only scripts)
  - every `.agents/...` or `.github/...` path mentioned in the text exists
  - SDLC_VERSION matches the latest entry in CHANGELOG.md

Run:  python tools/check_package.py   (or python3 on Linux and macOS)
"""
import fnmatch
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG = ROOT / "package"

REQUIRED = [
    "AGENTS.md",
    ".agents/README.md",
    ".agents/SDLC_VERSION",
    ".agents/rules/instructions.md",
    ".agents/rules/project.md",
    ".github/pull_request_template.md",
    ".github/workflows/ci-codereview.yml",
]
FORBIDDEN = ["evidence/", "R3-", "R4-", "R5-", "playbooks/", ".ps1", "../"]
# Paths the text mentions on purpose that a project creates itself (not shipped).
PROJECT_CREATED = [
    ".github/ocr-rules.json",
    ".github/ISSUE_TEMPLATE/*",
    ".agents/skills/go-live/SKILL.md",
]

problems = []


def read(rel):
    return (PKG / rel).read_text(encoding="utf-8")


def main():
    for rel in REQUIRED:
        if not (PKG / rel).is_file():
            problems.append("missing required file: " + rel)

    # guides
    nums = sorted(int(p.name[:2]) for p in (PKG / ".agents/guides").glob("[0-9][0-9]-*.md"))
    if nums != list(range(len(nums))) or not nums:
        problems.append("guides are not contiguous from 00: %s" % nums)

    # skills
    skill_dirs = sorted(p.name for p in (PKG / ".agents/skills").iterdir() if p.is_dir())
    for name in skill_dirs:
        f = PKG / ".agents/skills" / name / "SKILL.md"
        if not name.startswith("sdlc-"):
            problems.append("skill without sdlc- prefix: " + name)
        if not f.is_file():
            problems.append("missing SKILL.md in " + name)
            continue
        m = re.match(r'---\nname: (.+)\ndescription: "(.+)"\n---\n', f.read_text(encoding="utf-8"))
        if not m:
            problems.append("bad frontmatter in " + name)
        elif m.group(1) != name:
            problems.append("frontmatter name %r does not match folder %r" % (m.group(1), name))
    listed = set(re.findall(r"sdlc-[a-z]+(?:-[a-z]+)*", read(".agents/rules/instructions.md")))
    if listed != set(skill_dirs):
        problems.append("skills listed in instructions.md differ from folders: %s" % sorted(listed ^ set(skill_dirs)))

    # leftovers and path references
    files = [p for p in PKG.rglob("*") if p.is_file()]
    for p in files:
        rel = p.relative_to(PKG).as_posix()
        text = p.read_text(encoding="utf-8")
        for bad in FORBIDDEN:
            if bad in text:
                problems.append("%s contains %r" % (rel, bad))
        for ref in set(re.findall(r"`((?:\.agents|\.github)/[^`\s]+\.(?:md|yml|json))`", text)):
            if "<" in ref or "*" in ref:
                continue
            if any(fnmatch.fnmatchcase(ref, pattern) for pattern in PROJECT_CREATED):
                continue
            if not (PKG / ref).is_file():
                problems.append("%s mentions a missing file: %s" % (rel, ref))

    # version
    m = re.match(r"sdlc-package (\d+\.\d+\.\d+) \((\d{4}-\d{2}-\d{2})\)\s*$", read(".agents/SDLC_VERSION"))
    if not m:
        problems.append("SDLC_VERSION has an unexpected format")
    else:
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        if "## [%s]" % m.group(1) not in changelog:
            problems.append("CHANGELOG.md has no entry for version " + m.group(1))

    def tokens(rel):
        return len(read(rel)) // 4

    always = ["AGENTS.md", ".agents/rules/instructions.md", ".agents/rules/project.md"]
    print("files: %d | guides: %d | skills: %d" % (len(files), len(nums), len(skill_dirs)))
    print("always-loaded tokens (approx): %d" % sum(tokens(a) for a in always))
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  - " + p)
        return 1
    print("package OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
