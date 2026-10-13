# Cross-Project Practices Matrix

Input for Phase 2. Each row is a practice, its status in each project, and the evidence behind it. Status values: **Strong** (documented and visible in the repo), **Partial** (present but incomplete or unenforced), **Absent**, **Unverified** (depends on GitHub or local settings not visible here).

Projects: **LJ** = LivroJogo, **MM** = MusicMatch, **BM** = Vibe Coding Benchmarks.

## 1. Practice Matrix

| # | Practice | LJ | MM | BM | Evidence |
|---|---|---|---|---|---|
| P1 | Protected main, PR-only merges | Strong (documented) / Unverified (settings) | Partial (PR merges in log, no rule file) | Absent (single author, no PRs in log) | LJ `docs/SDLC.md` §1, `.agents/rules/instructions.md`; MM log `Merge pull request #N`; BM 28 commits by one author |
| P2 | Conventional Commits | Strong (types + scopes) | Strong (types + scopes) | Partial (readable, no types) | LJ `docs/SDLC.md` §3; MM log; BM log |
| P3 | Always-on agent rules file | Strong (`.agents/rules/instructions.md`, `always_on`) | Strong (`AGENTS.md`) | Absent | Files as listed |
| P4 | Canonical SDLC / policy doc | Strong (`docs/SDLC.md`) | Partial (`PROJECT_CONTEXT.md`, persona-style) | Partial (`docs/README.md` hub, no process doc) | Files as listed |
| P5 | ADRs | Strong (17) | Strong (13, one changelog claim is stale) | Absent as ADRs; decisions in `docs/` | `docs/adr/` in LJ and MM |
| P6 | Automated tests in CI | Strong (backend, frontend) | Absent (no CI tracked) | Absent (no CI tracked) | `.github/workflows/ci-*.yml` only in LJ |
| P7 | Security scan in CI | Partial (Snyk, silent skip without token) | Absent | Absent | `ci-livrojogo-backend.yml` step 3.2 |
| P8 | AI code review | Strong (path-scoped, incremental, advisory) | Absent | Absent | `ci-livrojogo-codereview.yml`, `.github/ocr-rules.json`, ADR 0017 |
| P9 | Dependency automation | Strong (Dependabot weekly) | Absent | Absent | `.github/dependabot.yml`; 66 bot commits in LJ log |
| P10 | Gated production deploy (branch guard, environment) | Strong | N/A (local app) | N/A (research) | `cd-livrojogo-backend-production-linux.yml` step 0 |
| P11 | Pre-deploy data snapshot and retention | Strong (DB 14, media 7) | N/A | N/A | CD step 4.5 |
| P12 | Automatic rollback with forensic preservation | Strong | N/A | N/A | CD step 8 (`.failed-<timestamp>`) |
| P13 | Healthcheck gate | Strong (local blocking, public warning) | N/A | N/A | CD step 7.5 |
| P14 | Deploy summary for humans | Strong (`GITHUB_STEP_SUMMARY`) | N/A | N/A | CD step 9 |
| P15 | Changelog and SemVer | Partial (module SemVer in SDLC; release notes via `gh release`) | Strong (Keep a Changelog, SemVer) | Absent | MM `CHANGELOG.md`; LJ SDLC §6 |
| P16 | Secrets hygiene | Partial (secrets in GitHub; not reviewed locally) | Strong (`.env` ignored, `.env.example` tracked) | Strong (`.gitignore` covers `results/`, `.work/`) | `.gitignore` in each repo |
| P17 | Pre-specified measurement and decision rules | N/A | N/A | **Strong** | BM `docs/measurement-and-analysis.md` |
| P18 | Missing data handled explicitly | N/A | N/A | **Strong** (missing ≠ zero) | BM same doc |
| P19 | Public/private evidence split with checkable export | N/A | N/A | **Strong** (`--check`, SHA-256) | BM `docs/data/README.md` |
| P20 | Limits stated up front | Partial | Partial (README badges overstate) | **Strong** | BM `README.md` first screen |
| P21 | Frozen intervention protocol | N/A | N/A | **Strong** | BM measurement doc §Nudges |
| P22 | Language policy stated | Strong (`.agents` rule, chat PT / artifacts EN) | Partial (EN-INT rule, legacy PT files remain) | Absent (implicit English) | Files as listed |
| P23 | Hub / index doc for navigation | Partial (`README.md`, `CONTEXT.md`) | Partial | Strong (`docs/README.md`) | Files as listed |
| P24 | Operational topology in docs | Present (SDLC §7, LAN IPs) | Absent | Absent | LJ `docs/SDLC.md` §7 |

## 2. Candidate Practices for the Guide

Ranked by how much they transfer to a general SDLC standard, not by how impressive they are.

**Tier 1: transfer to any project**

1. **Single canonical SDLC doc + an always-on agent rules file that links to it** (LJ P3/P4). The rules file is short and points to the spec, so there is one source of truth.
2. **Conventional Commits with module scopes** (LJ, MM). Already in both.
3. **Explicit "never on main" + feature-branch workflow with a named pattern** (LJ P1, MM branches).
4. **Pre-declared outcomes, denominators, and missing-data rules** (BM P17/P18). Transfers to any metric-driven work, not only research.
5. **Limits stated first** (BM P20). Put limitations on the first screen of every README and report.
6. **ADRs with Context → Decision → Consequences** (LJ P5, MM P5).
7. **Snapshot, gate, rollback, forensic preservation for any data-bearing deploy** (LJ P11–P13). Transfers to any project that persists user data.

**Tier 2: transfer with adaptation**

8. **Advisory AI review, path-scoped, incremental, cost-aware, excluding bots** (LJ P8). Strong, but it depends on paid model access. The ADR should record the cost model.
9. **Public/private evidence split with a checkable export** (BM P19). Strong for research or public reporting; overkill for an internal app.
10. **Frozen intervention or policy text** (BM P21). Useful when agents are steered by prompts that must not drift between runs.
11. **Keep a Changelog + SemVer** (MM P15) for libraries and tools.

**Tier 3: keep out of the guide or move to reference**

- Operational topology with IPs and hostnames (LJ P24). Keep this in an infrastructure doc, not in the SDLC spec.
- Project-specific stack constraints (for example, the LJ rule forbidding anything except Django, React, and Flutter).
- Named models and provider costs. These go stale quickly.

## 3. Anti-Patterns to Avoid

1. **Security gates that silently pass.** LJ's Snyk step passes when the token is missing. Make missing configuration fail, or label it explicitly.
2. **Stale numbers in docs.** MM has three different test counts (README 87, CHANGELOG 73, grep 171) and an ADR count that disagrees with the changelog (9 vs 13). Generate counts from the source, or leave them out.
3. **Version drift across the stack.** LJ has Python 3.13 in CI and 3.14 in CD. MM has `>=3.11` in `pyproject.toml` and "3.14+" in the README. Pin one version in a single place and reference it.
4. **Two names for one product.** LJ uses `livrojogo`, "Lore Vault", and "LoreVault" interchangeably.
5. **Policy docs that are not updated when the policy changes.** MM's language rule says "from now on" but the changelog and persona doc still follow the old one. State whether legacy docs are migrated, frozen, or deleted.
6. **Documentation sprawl without a hub.** BM has about 45 files in `docs/` with heavy overlap. The hub helps, but supersession should be marked on each file, not only in the hub.
7. **No CI for a test suite that is claimed to pass.** MM's README badges claim 87 passing tests with 98% coverage, and no CI enforces it. Badges without a gate are claims, not evidence.
8. **Operational data in policy docs** (LJ §7). It goes stale and buries the policy.

## 4. Gaps Not Covered by Any of the Three

These are real SDLC concerns none of the projects documents well. Phase 2 may want to fill them from general practice, marked as such, not as lessons from these repos:

- **Test pyramid and coverage thresholds** with an enforced minimum.
- **Lint and type-check gates** as a consistent standard. LJ uses `tsc --noEmit` only in the SDLC text. MM has no lint config in `pyproject.toml`.
- **Review rules for single-author repos.** BM and MM show that PR-based review is not always practiced. The guide needs a rule for when self-review is acceptable.
- **Rollback and migration policy for SQLite-backed apps** beyond LJ's CD. Only LJ has one.
- **Definition of done**, which none of the three states explicitly.

## 5. Open Questions for You (before Phase 2)

1. **Which practices are mandatory vs. recommended** for your future projects? The matrix above assumes everything is a candidate.
2. **Language of the final guides.** The evidence is in English. Your chat is in Portuguese. Should the guides be in English (for agents, matching the repos) or Portuguese (for you), or both?
3. **Where should the guides live?** Suggested: `C:\WebApps\sagglabs-sdlc\guides\` for normative docs, `C:\WebApps\sagglabs-sdlc\references\` for supporting material.
4. **Should Phase 2 include a verification pass** that runs the three test suites in a scratch copy outside the project folders, so counts can be confirmed without touching them?
