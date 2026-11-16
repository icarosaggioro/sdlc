# SDLC Compendium for Small and Medium Teams

Practices for building, reviewing, shipping, and operating software in an organization of 1 to 15 engineers, with AI assistance as a normal part of the work. Derived from three reference projects, filled in with general practice where they are silent.

Every practice is essential, with a **minimum form** a small team can adopt quickly and a **scale-up** note for later. Repos declare a `solo` or `team` profile; see guide 00.

## How This Repository Works

`package/` is the single source of truth **and** the thing you copy into each project. There is no build step: edit files in `package/`, then install.

```
package/            copy-in payload: AGENTS.md, .agents/ (rules, guides, skills, references), .github/
tools/              install_package.py (cross-platform installer), check_package.py (validator), test_install_package.py
docs/ADOPTING.md    how to adopt it, tool by tool and project by project
docs/background/    survey of the three reference projects, decisions, rollout analysis
CHANGELOG.md        package versions
```

An agent loads about **990 tokens** per session (`AGENTS.md`, `instructions.md`, `project.md`). The guides and skills are read on demand. It works with Antigravity, Codex, and OpenCode; there is no `CLAUDE.md`.

## Install

Dry run first (changes nothing), then apply. Works on Windows, Linux, and macOS with Python 3.8 or newer.

```
python tools/install_package.py C:\WebApps\my-project            # Windows
python3 tools/install_package.py ~/projects/my-project           # Linux, macOS
python3 tools/install_package.py ~/projects/my-project --apply   # copy for real
python3 tools/install_package.py ~/projects/my-project --apply --harness claude   # also add the Claude Code layer
```

`--harness claude` adds a `CLAUDE.md` that imports the rules and copies the skills to `.claude/skills/`, on top of the generic layout (Claude Code reads neither `.agents/skills` nor `AGENTS.md` once a `CLAUDE.md` exists).

It never overwrites `.agents/rules/project.md` or anything under `.github/`. Read [docs/ADOPTING.md](docs/ADOPTING.md) before the first install in an existing project.

## Guides (in `package/.agents/guides/`)

| # | Guide |
|---|---|
| 00 | [Principles, scope, and profiles](package/.agents/guides/00-principles-and-scope.md) |
| 01 | [Source control and branching](package/.agents/guides/01-source-control-and-branching.md) |
| 02 | [Commits and pull requests](package/.agents/guides/02-commits-and-pull-requests.md) |
| 03 | [Issues and planning](package/.agents/guides/03-issues-and-planning.md) |
| 04 | [Code review](package/.agents/guides/04-code-review.md) |
| 05 | [Definition of Done](package/.agents/guides/05-definition-of-done.md) |
| 06 | [Testing strategy](package/.agents/guides/06-testing-strategy.md) |
| 07 | [Quality gates and CI](package/.agents/guides/07-quality-gates-and-ci.md) |
| 08 | [Dependencies and security](package/.agents/guides/08-dependencies-and-security.md) |
| 09 | [Architecture decisions](package/.agents/guides/09-architecture-decisions.md) |
| 10 | [Documentation](package/.agents/guides/10-documentation.md) |
| 11 | [Versioning and release](package/.agents/guides/11-versioning-and-release.md) |
| 12 | [Deployment and rollback](package/.agents/guides/12-deployment-and-rollback.md) |
| 13 | [Data safety](package/.agents/guides/13-data-safety.md) |
| 14 | [Operations and incidents](package/.agents/guides/14-operations-and-incidents.md) |
| 15 | [AI-assisted development](package/.agents/guides/15-ai-assisted-development.md) |
| 16 | [Roles and responsibilities](package/.agents/guides/16-roles-and-responsibilities.md) |

## Skills (in `package/.agents/skills/`)

Fourteen procedures an agent follows for common tasks, named `sdlc-*`:
`start-task`, `implement-change`, `open-pr`, `review-tour`, `review-pr`, `fix-bug`, `hotfix`, `write-adr`, `update-dependencies`, `cut-release`, `rollback`, `incident`, `bootstrap-repo`, `use-ai-agent`.

## References (in `package/.agents/references/`)

- [R1 Templates](package/.agents/references/R1-templates.md): PR, issue, ADR, README, runbook, review workflow, Dependabot.
- [R2 Anti-patterns](package/.agents/references/R2-anti-patterns.md)

## Background (not copied into projects)

- [Survey of the three reference projects](docs/background/evidence/README.md)
- [R3 Evidence map](docs/background/R3-evidence-map.md): which guide rule comes from which project, and which is general practice.
- [R4 Open decisions](docs/background/R4-open-decisions.md): decisions and their log.
- [R5 Rollout impact, solo profile, and context strategy](docs/background/R5-rollout-and-context-strategy.md)
- [R6 PR review tooling: options and recommendation](docs/background/R6-pr-review-tooling.md) (proposal)

## Maintaining the Package

1. Edit files in `package/`.
2. Bump `package/.agents/SDLC_VERSION` and add an entry to `CHANGELOG.md`.
3. Run `python tools/check_package.py` and `python tools/test_install_package.py`.
4. Install into the projects that should receive the update.

## Status

Numbers such as 400-line PRs, a ten-minute CI target, and one-business-day reviews are proposals; see [R3](docs/background/R3-evidence-map.md#not-supported-by-evidence). The installer has been tested on Windows only. The Claude Code layer was verified against Claude Code 2.1.299.
