# R3. Evidence Map

For each guide: what in the three reference projects grounds it, and what is **general practice filled in** because the projects have nothing on it. Evidence files are in `../evidence/`.

Legend: **LJ** LivroJogo, **MM** MusicMatch, **BM** Vibe Coding Benchmarks. **Grounded** means observed in at least one project. **General** means not observed; added from common practice.

| Guide | Grounded in | General practice added |
|---|---|---|
| 00 Principles | LJ SDLC principles; BM claims-need-evidence stance; MM language policy | Right-sizing principle, MUST/SHOULD framing |
| 01 Branching | LJ `docs/SDLC.md` §2, `.agents/rules`; MM branch names with issue numbers; LJ remote-only release branch | Tag-based promotion as default; 3-day branch lifetime; branch types aligned to commit types |
| 02 Commits and PRs | LJ and MM Conventional Commits with scopes; LJ PR history with review-fix commits | Squash-merge default; 400-line guideline; `Co-Authored-By` for AI |
| 03 Issues | LJ issue-driven rule, `Fixes #N`; MM issue numbers in branch names | Templates, acceptance criteria format, monthly backlog review |
| 04 Code review | LJ AI review and advisory mode (ADR 0017); LJ history showing findings acted on | One-business-day SLA, comment labels, solo-developer 24-hour rule, reviewer checklist |
| 05 Definition of Done | LJ quality gates and release safeguards | The list itself; none of the projects states a DoD |
| 06 Testing | LJ CI test steps (Django, Vitest); MM and BM large suites; BM "green public tests are insufficient" | Test pyramid, coverage ratchet, flaky-test policy |
| 07 Quality gates and CI | LJ workflows; LJ `ci-livrojogo-codereview.yml`; LJ `scripts/check-all.ps1` (exists, not read) | Pinning policy detail, `permissions`, path-filter pitfall, 10-minute target |
| 08 Dependencies and security | LJ Dependabot and Snyk; MM `.gitignore` and `.env.example`; BM sanitized public data | Secret scanning, typosquat warning, SBOM and signing as scale-up |
| 09 ADRs | LJ 17 ADRs; MM 13 ADRs; MM ADR 0009 as a testable decision | Immutability and supersede rule; keep counts out of other docs |
| 10 Documentation | BM hub and historical labels; MM README and CHANGELOG drift; LJ SDLC mixing topology | README section list, document status headers, doc-type table |
| 11 Versioning and release | LJ independent SemVer, `versionCode`, tags and GitHub Release; MM Keep a Changelog | Automated notes from commit types, pre-release identifiers |
| 12 Deployment and rollback | LJ production CD (ref guard, snapshot, healthcheck, rollback, summary, concurrency) | Alive-versus-ready distinction, blue-green as scale-up |
| 13 Data safety | LJ pre-migration snapshot and forensic copy; MM ADR 0009 and 0013 soft-delete | Quarterly restore test, expand-and-contract migrations, WAL note |
| 14 Operations and incidents | LJ `/api/status/` with 12 subservices | Runbooks, severities, incident procedure, post-incident review (none of the projects has them) |
| 15 AI-assisted development | LJ rules file, go-live skill, ADR 0017; MM `AGENTS.md` and `PROJECT_CONTEXT.md`; BM evidence discipline | Agent permission boundaries, review focus for AI-written code, AI-review measurement and promotion criteria |
| 16 Roles | Nothing; each project has one maintainer | The whole guide |

## Not Supported by Evidence

These statements appear in the guides but are **not** established by the reference projects. Treat them as proposals until tried:

- That path-scoped AI review rules reduce noise (LJ uses them; effect not measured).
- That advisory AI review produces "good results" (reported by the maintainer, not measured here).
- That the 24-hour delay for solo developers is the right length.
- Specific numbers: 400-line PRs, ten-minute CI, one-business-day review, five-day post-incident review.

## Unverified Claims in the Evidence Files

- GitHub branch protection, required checks, and environment reviewers were not visible in the clones.
- Whether any workflow currently passes was not checked.
- Test suites were not executed; the maintainer states they pass.
- The numbers in Benchmarks' README table were not reconciled against `docs/data/matrix-results.json`.
