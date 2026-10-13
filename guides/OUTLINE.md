# Compendium Outline: SDLC Practices for Small and Medium Teams

Status: superseded by the drafted compendium. See `../README.md` for the index. This outline is kept as the planning record.

## Ground Rules for the Compendium

- **Every practice is essential.** Each one has a *minimum form* that a small team can adopt in an afternoon, and a *scale-up note* for when the team grows. Nothing is optional by omission; the minimum form is the bar.
- **Right-size for a team of 1 to 15 people** with one to a few production systems. No heavyweight ceremonies, no mandatory tools beyond Git, a CI service, and a shared issue tracker.
- **Normative text is short.** Each guide states rules as "must" or "should", then gives the reason in one or two sentences, then the procedure.
- **Language:** English for all files, identifiers, branches, and commit messages.
- **Single source of truth.** Counts, versions, and tool names are not repeated across guides; each lives in one place.

## Core Assumption: AI Is Part of Everyday Development

Assume that most code in these projects is written, reviewed, or tested with AI assistance. Every guide must answer one question: *what changes when the author or reviewer is an AI agent?* Concretely:

- AI-authored code gets the same gates, review, and Definition of Done as human code. Authorship does not lower the bar.
- AI review is an extra layer, never a replacement for human review of anything that touches data, security, or releases.
- Agent instructions live in the repo (agent rules file) and are versioned like code.
- Agent output is evaluated by the same metrics as human output: defects found after merge, rework, and review time.

## Automated Code Review in CI (reference case: LivroJogo)

LivroJogo runs Open Code Review (`alibaba/open-code-review`, pinned to `v1.12.13`) on every non-draft PR, through OpenRouter. The guide should codify what works there and what is still open:

**Practices to codify**
- Pin the review action to an exact version, not a branch or `latest`.
- Pin the model through a repository variable, with an explicit fallback. Do not rely on a free-tier default silently.
- Exclude bots (Dependabot), drafts, lockfiles, binaries, and data files, to save budget and reduce noise.
- Scope review rules by path (backend security and validation, frontend typing and hooks, mobile disposal and null-safety). A path-specific rule beats one generic prompt.
- Use incremental review and a single sticky summary so PRs do not fill with duplicate comments.
- Run it non-blocking (`continue-on-error`) while it is calibrated. Record the decision in an ADR (LivroJogo ADR 0017).

**Open items to flag in the guide, not to assert as solved**
- "Good results" is currently a qualitative judgment. The guide should require measuring it: findings accepted versus dismissed, and defects that escaped review despite a clean AI review.
- The advisory mode has no promotion criteria. Define when a specific rule (for example, a security rule) may become blocking.
- The review's quality depends on the model. Changing `OCR_LLM_MODEL` is a behavior change and should be recorded like a dependency upgrade.
- Who triages AI findings, and in what time, is not written down.

## Normative Guides (`guides/`)

| # | Guide | Covers | Minimum form (summary) |
|---|---|---|---|
| 00 | Principles and scope | Purpose, audience, how to read the compendium | One page |
| 01 | Source control and branching | Trunk-based flow, protected main, branch naming | Short-lived branches, PR to main, no direct pushes |
| 02 | Commits and pull requests | Conventional Commits, PR template, size limits | Commit subject rule, PR template, link to issue |
| 03 | Issues and planning | Issue-driven work, acceptance criteria, backlog hygiene | Every change traces to an issue or a stated reason |
| 04 | Code review | Reviewer duties, checklist, self-review for solo work, AI review as advisory | One reviewer per PR; solo teams use a written self-review checklist |
| 05 | Definition of Done | Shared exit criteria for a change | Tests, docs touched, rollback noted, reviewed |
| 06 | Testing strategy | Test layers, what must be tested, regression rule | Every bug fix ships with a regression test |
| 07 | Quality gates and CI | Lint, types, tests, build, required checks, automated AI code review (advisory), pinned tool versions | CI runs the same commands developers run locally; AI review is advisory and version-pinned |
| 08 | Dependencies and security | Dependency updates, secret handling, vulnerability scanning | Secrets never in git; scans fail closed |
| 09 | Architecture decisions | ADR process, when to write one, template | ADR for any decision that is costly to reverse |
| 10 | Documentation | README standard, changelog, language policy, doc lifecycle | Each repo has README, CHANGELOG, and a short agent rules file |
| 11 | Versioning and release | SemVer, release notes, promotion from main | Tagged releases; release notes from commits |
| 12 | Deployment and rollback | Promotion, healthchecks, rollback criteria | Documented rollback step before every deploy |
| 13 | Data safety | Migrations, backups, retention, soft delete | Backup before every migration; restore tested |
| 14 | Operations and incidents | On-call, runbooks, incident handling, post-incident review | Runbook per service; blameless review for major incidents |
| 15 | AI-assisted development | Agent rules, scope, review of AI output, AI code review operations (model pinning, triage, measurement), cost, prompts as artifacts | Agent rules file in every repo; AI output gets the same review as human output; AI review findings are triaged and measured |
| 16 | Roles and responsibilities | Who does what in a small team | A named owner per repo and per release |

## Reference Material (`references/`)

- **R1 Templates:** ADR, pull request, issue, README, changelog entry, runbook, agent rules file, post-incident review.
- **R2 Anti-patterns:** the list from `evidence/04-practices-matrix.md` §3, updated with the three test-count and version-drift findings.
- **R3 Evidence map:** which guide rule is grounded in which project observation (from `evidence/`), and which rules are general practice filled in for gaps.
- **R4 Open decisions:** choices the team must make, with a proposed default for each (for example, coverage ratchet level, whether self-review is accepted for solo work).

## Daily Developer Playbooks (`playbooks/`)

These are the repeatable procedures a developer follows on an ordinary day. Each one is a short checklist.

| # | Playbook | Trigger |
|---|---|---|
| S1 | Start a task | New issue picked up |
| S2 | Implement a change | Work in a branch |
| S3 | Open a pull request | Branch ready for review |
| S4 | Review a pull request | Review requested |
| S5 | Fix a bug | Bug report or failing check |
| S6 | Hotfix production | Critical defect in production |
| S7 | Write an ADR | A costly-to-reverse decision |
| S8 | Update dependencies | Dependabot PR or security alert |
| S9 | Cut a release | Ready to promote main |
| S10 | Roll back a release | Failed healthcheck or regression |
| S11 | Respond to an incident | Alert or user report |
| S12 | Bootstrap a new repo | New project created |
| S13 | Use an AI agent on a task | Agent-assisted work |

## Decisions the Team Must Make (proposed defaults)

1. **Coverage policy:** ratchet to the current level, never let it drop. Default: no absolute target.
2. **Solo-developer review:** accept a written self-review checklist, plus a 24-hour delay before merging anything that touches production data. Default: accepted.
3. **Required CI checks:** lint, types, tests, and dependency scan must pass. Default: all four required.
4. **AI review:** advisory only, never a merge gate. Default: advisory.
5. **Language of commit subjects:** English. Default: English.

## Next Steps

1. Review this outline. Adjust any guide or playbook you want added, merged, or removed.
2. Drafting then starts on the normative guides, followed by the playbooks and references.
