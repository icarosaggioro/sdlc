"""Build the copy-in SDLC package from the master compendium.

Run from the compendium root:  python3 tools/build_package.py

Sources:  guides/, playbooks/, references/R1 and R2, package-src/
Output:   package/   (generated; never edit by hand)
"""
import glob
import os
import re
import shutil
import sys

VERSION = "1.0.0"
DATE = "2026-10-12"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "package")

# Playbook number -> (skill name, trigger-oriented description)
SKILLS = {
    1: ("sdlc-start-task",
        "Use when picking up an issue or beginning a new piece of work. Read the acceptance criteria, create the correctly named branch from an updated main, verify the baseline, and record a short plan."),
    2: ("sdlc-implement-change",
        "Use while implementing a change on a feature branch. Test first, make small conventional commits, run the project check command, keep the diff focused, update docs, and note the rollback."),
    3: ("sdlc-open-pr",
        "Use when a branch is ready for review. Run all checks, push, open the PR with a valid title and the PR template, link the issue, and mark it ready so the AI review runs."),
    4: ("sdlc-review-pr",
        "Use when asked to review a pull request. Read the description and tests first, check correctness, security, data and operability, label comments, and decide explicitly. In solo repos act as final reviewer and triage the AI findings."),
    5: ("sdlc-fix-bug",
        "Use when handling a bug report or a failing check. Reproduce it, write a failing regression test, fix the cause with the smallest change, look for sibling defects, and prevent recurrence."),
    6: ("sdlc-hotfix",
        "Use for a critical production defect. Decide rollback versus fix-forward, branch from main, test first, keep the CI gates, bump the PATCH version, release, and verify. Never trigger the production deploy without explicit human confirmation."),
    7: ("sdlc-write-adr",
        "Use when a decision is costly to reverse (core technology, data model, security posture, delivery capability, or a convention). Write a one-page ADR from the template, open it for review, and link it."),
    8: ("sdlc-update-dependencies",
        "Use for Dependabot PRs, security advisories, or when adding a dependency. Assess risk, read release notes, run the suite, and verify the package is the intended one."),
    9: ("sdlc-cut-release",
        "Use when releasing what is on main. Choose the SemVer bump, open the version and changelog PR, tag or promote, stop for human confirmation before the production deploy, verify, and publish release notes."),
    10: ("sdlc-rollback",
         "Use when a release fails its healthcheck or causes a regression. Apply the rollback criterion, preserve evidence, roll back code and if needed data from the pre-deploy snapshot, and verify. Prepare the commands; a human runs them against production."),
    11: ("sdlc-incident",
         "Use during a production incident or outage. Assess severity, stabilize first (prefer rollback), preserve evidence, communicate, resolve, and write the post-incident note."),
    12: ("sdlc-bootstrap-repo",
         "Use when creating a new repository or adopting the SDLC package in an existing one. Set up hygiene files, branch protection, CI with required checks, the review workflow, templates, and agent rules."),
    13: ("sdlc-use-ai-agent",
         "Use when delegating a task to an AI agent or supervising one. Define scope and off-limits actions, require a plan first, require real check output, review the full diff, and capture repeated mistakes in rules or CI."),
}
NAME_BY_NUM = {n: v[0] for n, v in SKILLS.items()}

EXTRA = {
    9: "\n**Project release skill:** if this repo has its own release skill (for example `go-live`), follow that one; this skill is the generic fallback.\n",
}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def copy(src_rel, dst_rel):
    write(dst_rel, read(os.path.join(ROOT, src_rel)))


def fix_guide(text):
    text = re.sub(r"\n## Evidence(?: Basis)?\n.*\Z", "\n", text, flags=re.S)
    text = re.sub(r"(?<![./\w])references/", ".agents/references/", text)
    return text.rstrip() + "\n"


def skill_from_playbook(path):
    num = int(re.search(r"S(\d+)-", os.path.basename(path)).group(1))
    name, desc = SKILLS[num]
    lines = read(path).splitlines()
    title = re.sub(r"^# S\d+\.\s*", "", lines[0])
    body = "\n".join(lines[1:]).strip("\n")
    body = re.sub(r"\bS(0?[1-9]|1[0-3])\b",
                  lambda m: "`" + NAME_BY_NUM[int(m.group(1))] + "`", body)
    body = re.sub(r"(\*\*Guides?:\*\*[^\n]*?)\.?(\n|$)", r"\1 (in `.agents/guides/`).\2", body, count=1)
    body += "\n" + EXTRA.get(num, "")
    fm = "---\nname: %s\ndescription: \"%s\"\n---\n\n" % (name, desc)
    return name, fm + "# " + title + "\n\n" + body.rstrip() + "\n"


def main():
    # Clear the contents, not the directory itself: on Windows a shell whose
    # working directory is OUT would make removing OUT fail.
    os.makedirs(OUT, exist_ok=True)
    for entry in os.listdir(OUT):
        path = os.path.join(OUT, entry)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    copy("package-src/AGENTS.md", "AGENTS.md")
    copy("package-src/rules/instructions.md", ".agents/rules/instructions.md")
    copy("package-src/rules/project.md", ".agents/rules/project.md")
    copy("package-src/README.md", ".agents/README.md")
    copy("package-src/github/pull_request_template.md", ".github/pull_request_template.md")
    copy("package-src/github/workflows/ci-codereview.yml", ".github/workflows/ci-codereview.yml")
    write(".agents/SDLC_VERSION", "sdlc-package %s (%s)\n" % (VERSION, DATE))

    for g in sorted(glob.glob(os.path.join(ROOT, "guides", "[0-9]*.md"))):
        write(".agents/guides/" + os.path.basename(g), fix_guide(read(g)))

    for r in ("R1-templates.md", "R2-anti-patterns.md"):
        write(".agents/references/" + r, fix_guide(read(os.path.join(ROOT, "references", r))))

    names = []
    for p in sorted(glob.glob(os.path.join(ROOT, "playbooks", "S*.md"))):
        name, text = skill_from_playbook(p)
        write(".agents/skills/%s/SKILL.md" % name, text)
        names.append(name)

    validate(names)


def validate(names):
    problems = []
    files = [os.path.join(d, f) for d, _, fs in os.walk(OUT) for f in fs]
    for f in files:
        rel = os.path.relpath(f, OUT).replace("\\", "/")
        t = read(f)
        for bad in ("evidence/", "R3-", "R4-", "R5-", "playbooks/", "../"):
            if bad in t:
                problems.append("%s contains %r" % (rel, bad))
    # skill names listed in instructions.md must match generated skills
    instr = read(os.path.join(OUT, ".agents/rules/instructions.md"))
    listed = set(re.findall(r"sdlc-[a-z-]+", instr))
    if listed != set(names):
        problems.append("skill list mismatch: %s" % sorted(listed ^ set(names)))
    for n in names:
        s = read(os.path.join(OUT, ".agents/skills/%s/SKILL.md" % n))
        if not s.startswith("---\nname: %s\n" % n):
            problems.append("bad frontmatter in " + n)

    def tok(rel):
        return len(read(os.path.join(OUT, rel))) // 4

    always = ["AGENTS.md", ".agents/rules/instructions.md", ".agents/rules/project.md"]
    print("files:", len(files), "| skills:", len(names))
    print("always-loaded tokens (approx):", {a: tok(a) for a in always}, "TOTAL", sum(tok(a) for a in always))
    print("skills tokens (approx):", {n: tok(".agents/skills/%s/SKILL.md" % n) for n in names})
    print("guides tokens (approx):", sum(tok(".agents/guides/" + os.path.basename(g)) for g in glob.glob(os.path.join(OUT, ".agents/guides/*.md"))))
    print("package total tokens (approx):", sum(len(read(f)) for f in files) // 4)
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("validation OK")


if __name__ == "__main__":
    main()
