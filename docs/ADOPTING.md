# Adopting the SDLC Package

How to inject the package into a project, tool by tool and project by project. The reference projects were not modified while preparing the package.

## What You Copy

Everything inside `package/` goes to the **root** of the target repository:

```
AGENTS.md                              pointer for any agent tool
.agents/rules/instructions.md          general rules (same in every repo)
.agents/rules/project.md               project-specific rules (you fill it in)
.agents/guides/                        guides 00 to 16 (on demand)
.agents/references/                    templates and anti-patterns
.agents/skills/sdlc-*/SKILL.md         14 procedures
.agents/SDLC_VERSION                   package version
.github/pull_request_template.md
.github/workflows/ci-codereview.yml   advisory AI review
```

An agent always loads about **990 tokens** (`AGENTS.md`, `instructions.md`, `project.md`). Everything else is read on demand.

## Install

The installer is one Python file with no dependencies. It runs the same way on Windows, Linux, and macOS. Use `python` or `py` on Windows and `python3` on Linux and macOS.

```
# 1. Dry run: shows what would happen, changes nothing
python tools/install_package.py C:\WebApps\<project>          # Windows
python3 tools/install_package.py ~/projects/<project>         # Linux, macOS

# 2. Apply
python tools/install_package.py C:\WebApps\<project> --apply
python3 tools/install_package.py ~/projects/<project> --apply
```

Rules the installer follows:

| Kind | Files | Behavior |
|---|---|---|
| Project-owned | `.agents/rules/project.md` | Never overwritten |
| Templates | `.github/*` | Copied only when missing |
| Package-owned | `AGENTS.md`, `instructions.md`, guides, references, `sdlc-*` skills | First install: a differing file is a **conflict** and is skipped (`--force` saves it as `.bak` and replaces it). Later updates (detected by `.agents/SDLC_VERSION`): replaced |

The version marker is written only when no conflict is pending. Line endings are ignored when comparing, so a Windows checkout with CRLF does not look like a conflict. The exit code is 1 when a conflict remains, which makes it usable in scripts.

You can also copy `package/` by hand. The installer only adds the safety rules.

## Linux and macOS

The package contents contain no OS-specific commands. The installer uses only `pathlib` and the standard library. It has been **tested on Windows only**; run the dry run once on a Linux or macOS machine before relying on it. Two things to know:

- Windows Git may convert line endings (`autocrlf`); the installer and the checker tolerate that.
- File names in the package are case-sensitive on Linux. They are already consistent (`SKILL.md`, `AGENTS.md`).

## Claude Code (`--harness claude`)

The default layout is tool-agnostic: a root `AGENTS.md` pointer plus `.agents/`. For repos where Claude Code is used, add the harness option:

```
python tools/install_package.py <repo> --apply --harness claude
```

It adds a Claude layer **on top of** the generic one, which stays in place so other tools keep working in the same repo:

| Created | Why |
|---|---|
| `CLAUDE.md` with two `@` imports (`instructions.md` and `project.md`) | Claude Code reads `AGENTS.md` only when no `CLAUDE.md` exists, so a `CLAUDE.md` must import the rules itself. Imports load at launch, with no extra tool call |
| `.claude/skills/sdlc-*` (copies) | Claude Code discovers skills only in `.claude/skills/`, not in `.agents/skills/`. Copies, not symlinks: symlinks need administrator rights on Windows |

An existing `CLAUDE.md` is **never modified**: the installer prints the two lines to add. The `.claude/skills` copies are package-owned and refreshed on every update, so do not edit them.

Without `--harness claude`, recent Claude Code versions still read the root `AGENTS.md` pointer (per the documentation), but the agent then has to follow it to read the rules, and the skills are not discovered.

**Cost in Claude Code:** about 990 tokens for the rules plus about 750 for the listing of the 14 skill names and descriptions (measured from the files). Skill bodies load only when a skill is invoked. The listing budget defaults to 1% of the context window, so a repo with many other skills may see the least-used descriptions dropped.

**Verified** on 2026-10-14 with Claude Code 2.1.299, on a temporary install: imports from `.agents/rules/` load at launch, and with `.claude/skills` the session quotes a skill description exactly, while the generic layout alone does not expose it. Documentation: [memory](https://code.claude.com/docs/en/memory) and [skills](https://code.claude.com/docs/en/skills). Other versions were not tested.

## Per-Tool Notes (verify once)

Antigravity, Codex, and OpenCode were not tested from here, so treat their rows as expectations and confirm each once by asking the agent (Claude Code is covered in the section above): *"Which rule files and skills did you load for this repository?"*

| Tool | Expected behavior | If it does not work |
|---|---|---|
| Google Antigravity | Loads `.agents/rules/*` (your existing files use `trigger: always_on`) and `.agents/skills/*` | Check the rule activation mode in its settings |
| Codex | Reads the root `AGENTS.md`, which points to the rules | Ask it to read `.agents/rules/instructions.md` explicitly once |
| OpenCode | Reads the root `AGENTS.md`, which points to the rules | Same as Codex |
| Claude Code | Use `--harness claude` (see above) | Verified |

Skill discovery may differ between tools. That is why `instructions.md` lists every skill name and its path, so any agent can open the right `SKILL.md` by hand.

## Per-Project Steps

### LivroJogo (`ships-to-users: yes`, `team-profile: solo`)

1. Run the installer in dry-run mode. Expect a **conflict** on `.agents/rules/instructions.md`.
2. Move the project-specific parts of the existing `instructions.md` into `.agents/rules/project.md`: the stack constraints, the schema contract (`backend/livro-jogo-schema.json`), the documentation map, and the module scopes. Drop what the package now covers (language, git conventions, review, release steps) and move the workstation topology to `docs/dev-environment.md` (it already exists).
3. Re-run with `--apply --force`. Delete the `.bak` after checking.
4. Do **not** rely on the package's `ci-codereview.yml`: `ci-livrojogo-codereview.yml` already exists, so the installer will add a second workflow. Delete the package copy, then align the existing one: pin `OCR_LLM_MODEL` with no `openrouter/free` fallback, and correct `X-Title=LoreVault ...` to `Lore Vault`.
5. Make the Snyk step fail closed (guide 07).
6. Keep the project skills (`go-live`, `remote-mobile-env`). `sdlc-cut-release` defers to `go-live`. `.skill-lock.json` is untouched.
7. Set branch protection to require the CI checks and zero approvals.

### MusicMatch (`ships-to-users: no`, `team-profile: solo`)

1. The existing `AGENTS.md` has only language rules, which `instructions.md` now covers. The installer reports a conflict; use `--force` after moving anything unique into `project.md`.
2. Fill `project.md` from `PROJECT_CONTEXT.md` (stack, architecture direction, EN-INT rule). Keep `PROJECT_CONTEXT.md` as the long document and link it from the docs map.
3. Add CI using the `sdlc-bootstrap-repo` skill (the package does not ship a stack-specific CI workflow). This is the largest gap.
4. Fix the drift: the test count in `README.md` and `CHANGELOG.md`, the ADR count in the changelog, and Python 3.14 versus `>=3.11`.
5. Add the review workflow and its secret and variable.

### Vibe Coding Benchmarks (`ships-to-users: no`, `team-profile: solo`)

1. Copy the package. Guides 11 to 14 do not apply, and `instructions.md` already says so for `ships-to-users: no`.
2. In `project.md`, point to `docs/measurement-and-analysis.md` as the evidence rules for results.
3. Add CI for the test suite. Everything else is optional for this repo.

## New Projects

Install the package, fill `project.md`, then run the `sdlc-bootstrap-repo` skill.

## Updating the Package

1. Edit files in `package/`. It is the single source of truth.
2. Bump `package/.agents/SDLC_VERSION` and add an entry to `CHANGELOG.md`.
3. Run `python tools/check_package.py`. It fails on a missing file, a bad skill, a broken path mention, a Windows-only leftover, or a version that does not match the changelog.
4. Run the installer on each repo that should receive the update. It replaces only package-owned files.

## Background Documents

`docs/background/` holds the survey of the three reference projects, the decisions log, the evidence map, and the rollout analysis. They explain why the rules look the way they do and are not copied into projects.

## Not Yet Covered

- A stack-specific CI workflow (Python, Node, Flutter). `sdlc-bootstrap-repo` describes what it must contain.
- Issue templates (optional in the solo profile) and a Dependabot file. The snippets are in R1.
- Testing on Linux and macOS.
