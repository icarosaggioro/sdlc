# SDLC Compendium for Small and Medium Teams

Practices for building, reviewing, shipping, and operating software in an organization of 1 to 15 engineers, with AI assistance as a normal part of the work. Derived from three reference projects, filled in with general practice where they are silent.

Every practice is essential, with a **minimum form** a small team can adopt quickly and a **scale-up** note for later.

## The Package (copy into every project)

`package/` is generated from this compendium and is what you copy into each repository: a root `AGENTS.md` pointer, general rules in `.agents/rules/instructions.md`, a project-owned `project.md`, the guides, templates, 13 `sdlc-*` skills, a PR template, and an advisory AI review workflow. It works with Antigravity, Codex, and OpenCode; no `CLAUDE.md`. Always-loaded cost is about 990 tokens per session.

- How to adopt it, tool by tool and project by project: [docs/ADOPTING.md](docs/ADOPTING.md)
- Build: `python3 tools/build_package.py` (generates and validates `package/`)
- Install: `tools/install-package.ps1 -Target <repo>` (dry run by default)
- History: [CHANGELOG.md](CHANGELOG.md)

Edit the sources (`guides/`, `playbooks/`, `references/`, `package-src/`), never `package/` directly.

## Start Here

1. [guides/00-principles-and-scope.md](guides/00-principles-and-scope.md): how to read the compendium.
2. [playbooks/](playbooks/): the procedures a developer follows day to day.
3. [references/R1-templates.md](references/R1-templates.md): copy-paste templates, including the AI code review workflow.
4. [references/R4-open-decisions.md](references/R4-open-decisions.md): choices that still need your answer.

## Guides (normative)

| # | Guide |
|---|---|
| 00 | [Principles and scope](guides/00-principles-and-scope.md) |
| 01 | [Source control and branching](guides/01-source-control-and-branching.md) |
| 02 | [Commits and pull requests](guides/02-commits-and-pull-requests.md) |
| 03 | [Issues and planning](guides/03-issues-and-planning.md) |
| 04 | [Code review](guides/04-code-review.md) |
| 05 | [Definition of Done](guides/05-definition-of-done.md) |
| 06 | [Testing strategy](guides/06-testing-strategy.md) |
| 07 | [Quality gates and CI](guides/07-quality-gates-and-ci.md) |
| 08 | [Dependencies and security](guides/08-dependencies-and-security.md) |
| 09 | [Architecture decisions](guides/09-architecture-decisions.md) |
| 10 | [Documentation](guides/10-documentation.md) |
| 11 | [Versioning and release](guides/11-versioning-and-release.md) |
| 12 | [Deployment and rollback](guides/12-deployment-and-rollback.md) |
| 13 | [Data safety](guides/13-data-safety.md) |
| 14 | [Operations and incidents](guides/14-operations-and-incidents.md) |
| 15 | [AI-assisted development](guides/15-ai-assisted-development.md) |
| 16 | [Roles and responsibilities](guides/16-roles-and-responsibilities.md) |

## Playbooks

| # | Playbook |
|---|---|
| S01 | [Start a task](playbooks/S01-start-a-task.md) |
| S02 | [Implement a change](playbooks/S02-implement-a-change.md) |
| S03 | [Open a pull request](playbooks/S03-open-a-pull-request.md) |
| S04 | [Review a pull request](playbooks/S04-review-a-pull-request.md) |
| S05 | [Fix a bug](playbooks/S05-fix-a-bug.md) |
| S06 | [Hotfix production](playbooks/S06-hotfix-production.md) |
| S07 | [Write an ADR](playbooks/S07-write-an-adr.md) |
| S08 | [Update dependencies](playbooks/S08-update-dependencies.md) |
| S09 | [Cut a release](playbooks/S09-cut-a-release.md) |
| S10 | [Roll back a release](playbooks/S10-roll-back-a-release.md) |
| S11 | [Respond to an incident](playbooks/S11-respond-to-an-incident.md) |
| S12 | [Bootstrap a new repo](playbooks/S12-bootstrap-a-new-repo.md) |
| S13 | [Use an AI agent on a task](playbooks/S13-use-an-ai-agent-on-a-task.md) |

## References

- [R1 Templates](references/R1-templates.md)
- [R2 Anti-patterns](references/R2-anti-patterns.md)
- [R3 Evidence map](references/R3-evidence-map.md)
- [R4 Open decisions](references/R4-open-decisions.md)
- [R5 Rollout impact, solo profile, and context strategy](references/R5-rollout-and-context-strategy.md)

## Evidence

The survey behind the compendium is in [evidence/](evidence/README.md): one file per reference project and a cross-project matrix.

## Status

First complete draft, 2026-10-12. Not yet reviewed by the team. Numbers such as 400-line PRs, a ten-minute CI target, and an eight-week window for promoting an AI review rule are proposals; see [R3](references/R3-evidence-map.md#not-supported-by-evidence).
