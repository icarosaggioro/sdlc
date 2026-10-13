# R5. Rollout Impact, Solo Profile, and Context Strategy

Status: **solo profile adopted on 2026-10-12** and applied to the guides (00, 03, 04, 05, 06, 14, 16). The analysis below is kept as the reasoning record. All time figures are **estimates**, not measurements. The token figures are measured file sizes converted at roughly 4 characters per token (range 3 to 5).

## Part 1. Overhead on the Current Process

### Where the three projects start

| Project | Already in place | Gap against the compendium | Estimated one-time effort |
|---|---|---|---|
| LivroJogo | PR flow, CI, AI review, CD with snapshot and rollback, ADRs, rules file | Fail-closed Snyk, pin the review model, PR template with Definition of Done, fix the "LoreVault" string, a CLAUDE.md that loads the rules (see Part 2) | 2 to 4 hours |
| MusicMatch | Conventional Commits, ADRs, changelog, rules file, `.gitignore` hygiene | No CI, no PR template, no branch protection, no AI review, stale counts in README and CHANGELOG | 4 to 8 hours |
| Benchmarks | Evidence discipline, docs hub, tests | No CI, no rules file. Release, deploy, and data-safety guides **do not apply** to a research repo | 2 to 3 hours |

The delta is smallest where the work is already happening. For LivroJogo, most of the compendium is a description of what the project does.

### Ongoing cost per event for one engineer

| Event | Full compendium as written | Solo profile (below) |
|---|---|---|
| Each PR | about 17 to 22 min: template 4, self-review checklist 5, AI finding triage 5 to 10, changelog 2, title 1 | about 8 to 12 min |
| Each release | about 20 to 30 min | about 10 to 15 min |
| Risky change (data, auth, deploy) | adds a **24-hour wait** (calendar delay, not effort) | wait applies only to destructive data changes |
| Periodic | monthly backlog review, monthly AI review metrics, quarterly restore test | quarterly backlog skim, no metrics, restore test twice a year |

At about ten PRs a month, the full set costs roughly three hours a month and the solo profile about one and a half. The estimates do not include the benefit side, which is also unmeasured.

### Where the compendium over-reaches for one engineer

The compendium said "all essential, right-sized". Reading it as a one-person team, these parts are too heavy and I recommend deferring them until a trigger fires:

| Guide | Too heavy for one engineer | Defer until |
|---|---|---|
| 03 | Monthly backlog review, three issue templates | A second person triages issues |
| 04 | Blanket 24-hour wait; formal self-review checklist on every PR | Keep the wait only for destructive data changes |
| 05 | Nine-item Definition of Done | Use five items (below) |
| 06 | Coverage ratchet | Coverage is reported by CI at no extra effort |
| 14 | Severity table, formal post-incident review | A second person or paying users appear. A short note after a Sev 1 is enough |
| 15 | Monthly review metrics, AI steward role | Already removed by decision D4 and D12 |
| 16 | Roles table | A second engineer joins. One named owner is enough |

### Solo Profile (proposed)

Applies to any repository with one engineer. Everything not listed here follows the guide as written.

1. **Definition of Done, five items:** CI green; behavior covered by a test (regression test for fixes); AI findings triaged at final review; docs and changelog updated when behavior changes; rollback noted for data or deploy changes. No secrets in the diff is covered by secret scanning.
2. **Review:** the sole engineer is both author and final reviewer. Re-read the diff in the PR view after a break; do not run a separate checklist.
3. **Branch protection:** require the CI checks and a PR, with **zero** required approvals. A PR author cannot approve their own PR on GitHub, so requiring one would block every merge. Check that your hosting plan supports branch protection on private repositories.
4. **Cooling-off:** wait 24 hours only for destructive migrations and data deletions. Everything else merges when CI is green and the diff has been read.
5. **Releases and deploys:** only for repos with real users or data (LivroJogo). Not for local tools or research repos.
6. **Roles:** one named owner per repo, no table.
7. **Incidents:** stabilize, roll back, write a five-line note. No review ceremony.

### Triggers to activate the rest

The profile depends on headcount alone: a repo moves from `solo` to `team` when a second engineer joins. Shipping to real users is a separate switch (`ships-to-users`), because a commercial product can have one engineer. Handling personal or financial data applies the security and data-safety guides in full, whatever the profile. (The first draft of this section tied the profile to "paying users", which would have excluded LivroJogo.)

### Rollout Phases

| Phase | When | What | Effort per repo |
|---|---|---|---|
| 0. Hygiene | Week 1 | `.gitignore`, `.env.example`, branch protection, CI with required checks, Dependabot, PR template (short), agent rules file | 1 to 3 hours |
| 1. AI review and conventions | Weeks 2 to 3 | AI review workflow, Conventional Commits, changelog, one-command local check | 1 to 2 hours |
| 2. Release and data safety | Month 2 | Release procedure, pre-migration snapshot, rollback note, runbook (one page) | 2 to 4 hours, only for repos that ship |
| 3. As needed | When triggered | ADRs for costly decisions, restore test, roles, incident process | On demand |

**Automate the rollout.** Put templates, the CI workflow, the review workflow, and the rules file in a template repository (or a copy of R1) so a new repo starts at Phase 1 for free. Setup effort per repo falls sharply from the second repo on.

### Check the Cost After a Month

After four weeks, record per repo: minutes added per PR, rules that were skipped or resented, and defects the process caught. Keep what paid for itself and drop the rest. This applies the evidence discipline of the Benchmarks project to the process itself.

## Part 2. Token Cost of Putting the Text in a Project

### Measured sizes

| Content | Files | Tokens (approx.) | Range |
|---|---|---|---|
| Normative guides | 17 | 15,800 | 12,600 to 21,000 |
| Playbooks | 13 | 4,400 | 3,600 to 5,900 |
| References | 5 | 7,500 | 6,000 to 10,000 |
| Evidence (survey) | 5 | 7,400 | 5,900 to 9,900 |
| **Everything** (including README and outline) | 42 | **about 38,000** | |
| Largest guide (15, AI-assisted development) | 1 | 1,700 | |

For comparison, the files your projects already carry: LivroJogo `.agents/rules/instructions.md` about 1,800 tokens, its `CONTEXT.md` about 3,900, `docs/SDLC.md` about 2,200; MusicMatch `AGENTS.md` about 300, `PROJECT_CONTEXT.md` about 2,000.

### What is actually at risk

Context cost comes from what is **loaded every turn**, not from what exists on disk. A file that sits in the repo and is read only when needed costs nothing until then. Loading all 38,000 tokens into every session would be the wrong design for three reasons: it is paid on every turn (cheaper with prompt caching, but not free), it crowds out the code and the task, and most of it is irrelevant to any given task.

### Design: three layers, loaded differently

| Layer | What | Size target | Loaded |
|---|---|---|---|
| 1. Rules file | `AGENTS.md` (or `CLAUDE.md`) per repo: stack limits, language, git rules, commands, safety rules, pointers to docs | 600 to 900 tokens | Every session |
| 2. Playbooks as skills | The playbooks an agent actually runs: S03, S04, S09, S12, S13 | About 300 to 600 tokens each | Only when invoked. Skills expose just a name and description until used |
| 3. Guides and references | The compendium itself | 15,800 tokens for the guides | On demand, one guide at a time, by path |

Expected steady-state cost: **about 800 tokens per session** for the rules file, plus 300 to 1,700 tokens when a specific playbook or guide is opened. That is roughly 2% of the full set.

### Rules for keeping the rules file small

1. **Never copy guide text into a repo.** Link to it. Keep the compendium in one place, referenced by path or URL, so there is a single source of truth and no per-repo drift.
2. **Include only what the agent cannot infer** and what it would get wrong: forbidden operations, naming and branch patterns, the check command, language rules, where the schema contract lives.
3. **Move enforcement out of prose and into machines.** A rule in CI (lint, types, tests, commit-message check) costs **zero context tokens** and cannot be forgotten. A paragraph in the rules file costs tokens every turn and can be ignored. Prefer a check wherever one is possible.
4. **Let GitHub carry the templates.** The PR template and issue templates are shown to humans by GitHub and do not enter the agent's context unless it opens them.
5. **Short sentences, no examples, no rationale** in the rules file. The rationale lives in the guide the file links to.
6. **Review it quarterly.** If a line has not prevented a mistake, delete it. When an agent repeats a mistake, add one line or a CI check; do not grow the file by habit.

### Two findings about your repos

1. **No `CLAUDE.md` exists, and that is fine.** The projects are used with Antigravity, Codex, and OpenCode as well, so the rules are not tied to one tool. The package uses a root `AGENTS.md` pointer plus `.agents/rules/` (see `docs/ADOPTING.md`).
2. **LivroJogo's rules file is mostly project description.** Its 1,800 tokens include the full topology of three workstations and the Portuguese-language glossary of commands. The topology belongs in an operations doc, linked, not loaded.

### Separate Cost Bucket: the AI Review in CI

The review action's tokens are billed to your OpenRouter key, not to an agent session. They scale with diff size and PR count, not with the compendium. The controls already in the guide are the right ones: skip drafts and bots, exclude lockfiles and binaries, review incrementally, and pin a model whose price you know. Add a **spend limit on the API key** as a hard ceiling.

### Optional: a Template Rules File (about 700 tokens)

A ready skeleton is in R1, section 9. A filled-in slim version for a solo repo has about 25 lines: stack, language, git, commands, safety, docs map.

## Outcome

1. The solo profile was adopted.
2. Rules are tool-agnostic: a root `AGENTS.md` pointer, `.agents/rules/instructions.md` (general) and `.agents/rules/project.md` (per project), no `CLAUDE.md`.
3. The playbooks were converted to `sdlc-*` skills and the whole thing is built into a copy-in package (`package/`).
