#!/usr/bin/env python3
"""Copy the SDLC package into a target repository (Windows, Linux, macOS).

Dry run by default: prints what would happen and changes nothing.
Use --apply to copy. Existing files are never overwritten silently.

Harnesses (--harness)
  generic  the tool-agnostic layout: AGENTS.md pointer + .agents/  (default)
  claude   generic PLUS a Claude Code layer, so Claude Code loads the rules at launch:
             CLAUDE.md                 imports the two rules files (created only if missing)
             .claude/skills/sdlc-*     copies of the sdlc-* skills (Claude Code does not read .agents/skills)
           The generic layout stays in place, so other tools keep working in the same repo.

Ownership rules
  project-owned  .agents/rules/project.md       never overwritten
  templates      .github/*, CLAUDE.md           created only when missing, never overwritten
  package-owned  AGENTS.md, .agents/rules/instructions.md, guides, references,
                 sdlc-* skills (both locations), README, SDLC_VERSION
                   first install : a differing file is a CONFLICT and is skipped
                                   (with --force the old file is saved as .bak first)
                   later updates : overwritten (detected by .agents/SDLC_VERSION)

An existing CLAUDE.md is never touched. If it lacks the imports, the installer prints the
exact lines to add (a CLAUDE.md suppresses AGENTS.md in Claude Code, so the imports matter).

Line endings (CRLF versus LF) are ignored when comparing files.

Examples
  python tools/install_package.py C:\\WebApps\\my-project                     (Windows)
  python3 tools/install_package.py ~/projects/my-project --harness claude    (Linux, macOS)
"""
import argparse
import fnmatch
import shutil
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent / "package"
VERSION_FILE = ".agents/SDLC_VERSION"
PROJECT_OWNED = ".agents/rules/project.md"
OWNED = [
    "AGENTS.md",
    ".agents/rules/instructions.md",
    ".agents/README.md",
    VERSION_FILE,
    ".agents/guides/*",
    ".agents/references/*",
    ".agents/skills/sdlc-*",
    ".claude/skills/sdlc-*",
]
HARNESSES = ("generic", "claude")
SKILLS_SRC = ".agents/skills/"
SKILLS_CLAUDE = ".claude/skills/"
CLAUDE_IMPORTS = ["@.agents/rules/instructions.md", "@.agents/rules/project.md"]
CLAUDE_MD = "# Project Instructions\n\n" + "\n".join(CLAUDE_IMPORTS) + "\n"


def is_owned(rel):
    return any(fnmatch.fnmatchcase(rel, pattern) for pattern in OWNED)


def same_content(a, b):
    return a.read_bytes().replace(b"\r\n", b"\n") == b.read_bytes().replace(b"\r\n", b"\n")


def collect(harness):
    """Return sorted (relative destination, source file) pairs for the chosen harness."""
    entries = []
    for src in PACKAGE.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(PACKAGE).as_posix()
        entries.append((rel, src))
        if harness == "claude" and rel.startswith(SKILLS_SRC + "sdlc-"):
            entries.append((SKILLS_CLAUDE + rel[len(SKILLS_SRC):], src))
    return sorted(entries, key=lambda e: e[0])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Install the SDLC package into a repository.")
    parser.add_argument("target", help="path of the repository to install into")
    parser.add_argument("--apply", action="store_true", help="copy files (default is a dry run)")
    parser.add_argument("--force", action="store_true",
                        help="on first install, replace conflicting package-owned files (saves .bak)")
    parser.add_argument("--harness", choices=HARNESSES, default="generic",
                        help="generic (default) or claude (adds CLAUDE.md and .claude/skills)")
    args = parser.parse_args(argv)

    if not PACKAGE.is_dir():
        sys.exit("Package not found: %s" % PACKAGE)
    target = Path(args.target).expanduser().resolve()
    if not target.is_dir():
        sys.exit("Target not found: %s" % target)
    if target == PACKAGE or PACKAGE in target.parents or target in PACKAGE.parents:
        sys.exit("Refusing to install the package into itself or its parent.")

    is_update = (target / VERSION_FILE).exists()
    mode = "APPLY" if args.apply else "DRY RUN"
    print("SDLC package install [%s] -> %s (%s, harness=%s)"
          % (mode, target, "update" if is_update else "first install", args.harness))
    if not (target / ".git").exists():
        print("  warning: target is not a git repository root")

    counts = {}
    conflicts = []
    version_pending = False

    for rel, src in collect(args.harness):
        dest = target / rel
        write = False

        if not dest.exists():
            action, write = "NEW", True
        elif same_content(src, dest):
            action = "SAME"
        elif rel == PROJECT_OWNED or not is_owned(rel):
            action = "KEEP"
        elif is_update:
            action, write = "UPDATE", True
        elif args.force:
            action, write = "REPLACE", True
        else:
            action = "CONFLICT"
            conflicts.append(rel)

        counts[action] = counts.get(action, 0) + 1
        if action != "SAME":
            print("  %-9s %s" % (action, rel))

        # The version marker is written last, and only when no conflict was skipped.
        # Otherwise the next run would look like an update and overwrite the skipped
        # file without a backup.
        if rel == VERSION_FILE:
            version_pending = version_pending or write
        elif args.apply and write:
            if action == "REPLACE":
                shutil.copyfile(str(dest), str(dest) + ".bak")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(src), str(dest))

    todo = []
    if args.harness == "claude":
        claude_md = target / "CLAUDE.md"
        if not claude_md.exists():
            counts["NEW"] = counts.get("NEW", 0) + 1
            print("  %-9s %s" % ("NEW", "CLAUDE.md"))
            if args.apply:
                claude_md.write_bytes(CLAUDE_MD.encode("utf-8"))  # bytes: keep LF on Windows
        else:
            text = claude_md.read_text(encoding="utf-8", errors="replace")
            todo = [line for line in CLAUDE_IMPORTS if line not in text]
            if todo:
                counts["TODO"] = counts.get("TODO", 0) + 1
                print("  %-9s %s" % ("TODO", "CLAUDE.md (exists; not modified)"))
            else:
                counts["SAME"] = counts.get("SAME", 0) + 1

    if args.apply and version_pending and not conflicts:
        dest = target / VERSION_FILE
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(PACKAGE / VERSION_FILE), str(dest))

    print()
    print("Summary: " + ", ".join("%s=%d" % (k, counts[k]) for k in sorted(counts)))
    if conflicts:
        print()
        print("Conflicts were skipped. Move any project-specific content from the existing file into")
        print(".agents/rules/project.md, then re-run with --apply --force (the old file is saved as .bak).")
    if todo:
        print()
        print("Your existing CLAUDE.md was not modified. Add these lines to it so Claude Code loads the")
        print("rules at launch (a CLAUDE.md suppresses AGENTS.md):")
        for line in todo:
            print("  " + line)
    if not args.apply:
        print("Nothing was changed. Re-run with --apply to copy.")
    return 1 if conflicts else 0


if __name__ == "__main__":
    sys.exit(main())
