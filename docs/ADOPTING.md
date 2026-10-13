# Adopting the SDLC Package

How to inject the package into a project, tool by tool and project by project. The package is built from this compendium; the project folders were not touched while preparing it.

## What You Copy

Everything inside `package/` goes to the **root** of the target repository:

```
AGENTS.md                              pointer for any agent tool
.agents/rules/instructions.md          general rules (same in every repo)
.agents/rules/project.md               project-specific rules (you fill it in)
.agents/guides/                        guides 00 to 16 (on demand)
.agents/references/                    templates and anti-patterns
.agents/skills/sdlc-*/SKILL.md         13 procedures
.agents/SDLC_VERSION                   package version
.github/pull_request_template.md
.github/workflows/ci-codereview.yml   advisory AI review
```

Always loaded by an agent: about **990 tokens** (`AGENTS.md`, `instructions.md`, `project.md`). Everything else is read on demand.

Use the script (dry run by default) or copy by hand:

```powershell
.\tools\install-package.ps1 -Target C:\WebApps\<project>           # shows what would happen
.\tools\install-package.ps1 -Target C:\WebApps\<project> -Apply    # copies
```

It never overwrites `project.md` or anything under `.github/`. On a first install, a differing package-owned file is reported as a **conflict** and skipped. On later updates (detected by `.agents/SDLC_VERSION`), package-owned files are replaced.

## Why Not `CLAUDE.md`

The projects are used with several tools, so the rules do not depend on one vendor's filename. A root `AGENTS.md` is a short pointer to `.agents/rules/`, which is where the LivroJogo rules already live. If someone uses a tool that reads only `CLAUDE.md`, a one-line `CLAUDE.md` containing `@AGENTS.md` bridges it; it is not part of the package.

## Per-Tool Notes (verify once)

I could not test these tools from here. Treat them as expectations and confirm each once per tool by asking the agent: *"Which rule files and skills did you load for this repository?"*

| Tool | Expected behavior | If it does not work |
|---|---|---|
| Google Antigravity | Loads `.agents/rules/*` (your existing files use `trigger: always_on`) and `.agents/skills/*` | Check the rule activation mode in its settings |
| Codex | Reads the root `AGENTS.md`, which points to the rules | Ask it to read `.agents/rules/instructions.md` explicitly once |
| OpenCode | Reads the root `AGENTS.md`, which points to the rules | Same as Codex |

Skill discovery may differ between tools. That is why `instructions.md` lists every skill name and its path, so any agent can open the right `SKILL.md` by hand.

## Per-Project Steps

### LivroJogo (`ships-to-users: yes`, `team-profile: solo`)

1. Run the installer in dry-run mode. Expect a **conflict** on `.agents/rules/instructions.md`.
2. Move the project-specific parts of the existing `instructions.md` into `.agents/rules/project.md`: the stack constraints, the schema contract (`backend/livro-jogo-schema.json`), the documentation map, and the module scopes. Drop what the package now covers (language, git conventions, review, release steps) and move the workstation topology to `docs/dev-environment.md` (it already exists).
3. Re-run with `-Apply -Force`. Delete the `.bak` after checking.
4. Do **not** copy `ci-codereview.yml`: `ci-livrojogo-codereview.yml` already exists. Instead align it: pin `OCR_LLM_MODEL` with no `openrouter/free` fallback, and correct `X-Title=LoreVault ...` to `Lore Vault`.
5. Make the Snyk step fail closed (guide 07).
6. Keep the project skills (`go-live`, `remote-mobile-env`). `sdlc-cut-release` defers to `go-live`. `.skill-lock.json` is untouched.
7. Set branch protection to require the CI checks and zero approvals.

### MusicMatch (`ships-to-users: no`, `team-profile: solo`)

1. The existing `AGENTS.md` has only language rules, which `instructions.md` now covers. The installer reports a conflict; use `-Force` after moving anything unique into `project.md`.
2. Fill `project.md` from `PROJECT_CONTEXT.md` (stack, architecture direction, EN-INT rule). Keep `PROJECT_CONTEXT.md` as the long document; link it from the docs map.
3. Add CI using `sdlc-bootstrap-repo` (the package does not ship a stack-specific CI workflow). This is the largest gap.
4. Fix the drift: the test count in `README.md` and `CHANGELOG.md`, the ADR count in the changelog, and Python 3.14 versus `>=3.11`.
5. Add the review workflow and its secret and variable.

### Vibe Coding Benchmarks (`ships-to-users: no`, `team-profile: solo`)

1. Copy the package. Guides 11 to 14 do not apply, and `instructions.md` already says so for `ships-to-users: no`.
2. In `project.md`, point to `docs/measurement-and-analysis.md` as the evidence rules for results.
3. Add CI for the test suite. Everything else is optional for this repo.

## New Projects

Copy the package, fill `project.md`, then run the `sdlc-bootstrap-repo` skill.

## Updating the Package

1. Edit the sources in this compendium (`guides/`, `playbooks/`, `references/R1` and `R2`, `package-src/`).
2. Bump `VERSION` and `DATE` in `tools/build_package.py` and add a line to `CHANGELOG.md`.
3. Run `python3 tools/build_package.py`. It fails if a link or a skill name drifted.
4. Run the installer on each repo. Packages updates replace only package-owned files.

`package/` is generated; never edit it by hand.

## What Is Not in the Package

`R3` (evidence map), `R4` (open decisions), and `R5` (rollout analysis) are about the organization and the three reference projects, not about any one repo. They stay here. The `evidence/` folder stays here too.

## Not Yet Covered

- A stack-specific CI workflow (Python, Node, Flutter). `sdlc-bootstrap-repo` describes what it must contain.
- Issue templates (optional in the solo profile). They are in `R1`.
- A Dependabot file (the ecosystems differ per project). The snippet is in `R1`.
