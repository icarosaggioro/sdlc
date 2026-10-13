# Evidence: LivroJogo / Lore Vault

Project root: `C:\WebApps\livrojogo`. HEAD `b7dc1e7`. 471 commits: 260 by one author, 145 by a second GitHub handle of the same person, 66 by `dependabot[bot]`.

## 1. Documented Process

| Artifact | What it establishes |
|---|---|
| `docs/SDLC.md` | Canonical SDLC spec: main-branch inviolability, issue-driven work, quality gates, branch patterns, Conventional Commits with module scopes, CD guarantees, release promotion. |
| `.agents/rules/instructions.md` | Always-on agent rules: stack constraints, language split (chat in Portuguese; code, docs, commits, PR bodies in English), mandatory feature-branch workflow, go-live procedure. |
| `docs/adr/` | 17 ADRs (0001–0017). ADR 0017 records the automated AI code review decision. |
| `.agents/skills/go-live/SKILL.md` | Release procedure packaged as a reusable agent skill. |
| `.agents/references/` | Reference notes for mobile emulator setup and store assets. |
| `PRD.md`, `CONTEXT.md` | Product requirements and a ubiquitous-language glossary. |

## 2. CI (pull requests to `main`, path-filtered)

- **`ci-livrojogo-backend.yml`:** Python 3.13; `pip install -r requirements.txt`; Snyk scan at `--severity-threshold=high`; `python manage.py test`.
  - *Gap:* if `CI_SNYK_TOKEN` is absent, the Snyk step prints a message and **passes**. A security gate that silently skips is not a gate.
- **`ci-livrojogo-frontend.yml`:** `npm ci`; Snyk step; `npm run test` (Vitest); `npm run build` (Vite). `package.json` confirms `"test": "vitest run"` and `"build": "vite build"`. The SDLC also mentions `tsc --noEmit`, but the workflow steps read do not show a separate typecheck step. *Unverified* whether `build` covers it.
- **`ci-livrojogo-mobile.yml`:** present; not read in detail. SDLC states `flutter analyze` and `flutter test`.

## 3. Automated AI Code Review

- **`ci-livrojogo-codereview.yml`:** runs on `opened`, `synchronize`, `reopened`, `ready_for_review`.
  - Skips drafts, `user.type == 'Bot'`, and `dependabot[bot]` / any `[bot]` actor. The SDLC and ADR 0017 justify this as preserving token budget.
  - `concurrency` cancels superseded runs per PR.
  - Uses `alibaba/open-code-review@v1.12.13` through OpenRouter. The model is set by `vars.OCR_LLM_MODEL` with a free-tier fallback.
  - `continue-on-error: true`, so it is advisory and never blocks a merge. ADR 0017 says this is deliberate during calibration.
  - Rules in `.github/ocr-rules.json` scope review by path: backend focus on security, validation, N+1 queries, and DRF practices; frontend focus on Strict Mode, no `any`, hook dependency arrays; Dart focus on null-safety and disposal. Lockfiles, binaries, media, and SQLite files are excluded.
- **Evidence of use:** recent commits such as `fix(core): address code review feedback on PR #170` and `refactor(frontend): resolve review findings on ...` show review findings being acted on.

## 4. CD and Production Release

- **`cd-livrojogo-backend-production-linux.yml`:** `workflow_dispatch` only, on a self-hosted Linux runner, with a GitHub Environment (`Production-lorevault.com.br`). Timeout 30 min.
  - **Branch guard:** the first step rejects any ref other than `refs/heads/release/lorevault-publish`.
  - **Pre-migration snapshot:** SQLite `.backup` plus a compressed media tarball, with retention of 14 DB and 7 media snapshots.
  - **Migrations and static files** run after the snapshot.
  - **Healthcheck gate:** up to 6 attempts × 3 s against `/api/status/` on localhost, requiring `status == operational`. Public endpoint check is a *warning only*.
  - **Failure rollback:** `if: failure()` moves the failed DB to `.failed-<timestamp>` for forensics, restores the snapshot, and restarts services.
  - **Step summary:** writes a Markdown table of versions, snapshot paths, gate results, and rollback status to `$GITHUB_STEP_SUMMARY`.
- **Frontend and mobile CD:** `cd-livrojogo-frontend-production-linux.yml` and `cd-livrojogo-mobile-production-android.yml` exist; not read in detail.
- **Release promotion:** `git push origin main:release/lorevault-publish` (fast-forward, remote-only branch). The SDLC forbids creating the release branch locally.
- **Dependabot:** weekly for `/backend` (pip) and `/frontend` (npm), `open-pull-requests-limit: 5`.

## 5. Inconsistencies Found

1. **Python version drift.** SDLC §4.1 and the backend CI use Python 3.13. The production CD builds its venv with `python3.14`. One of the two is stale or the mismatch is intentional and undocumented.
2. **Project naming.** The repo is `livrojogo`, the docs say "Lore Vault" and `lorevault.com.br`, and the review workflow header says "LoreVault". *Maintainer clarification (2026-10-12):* LivroJogo is the internal project name, Lore Vault is the commercial product name, and "LoreVault" is accidental. Only the stray spelling needs fixing.
3. **Silent Snyk skip** (see §2). The gate passes when the secret is missing.
4. **Operational data in the policy doc.** `docs/SDLC.md` §7 contains LAN IP addresses, host names, and port maps. That is operational topology, not policy. It is useful reference material but it will go stale and should live elsewhere.
5. **Commit language.** `.agents/rules` allows Portuguese or English for commit descriptions if consistent within a PR. The actual history is English, so the rule is looser than practice.

## 6. Strengths Worth Extracting

- Explicit, enforceable rules written for both humans and agents (`always_on` rules file plus a canonical SDLC spec that the rules file links to).
- Release safety that treats data as the critical asset: pre-migration snapshot, rollback that preserves forensic evidence, and a healthcheck gate.
- Advisory AI review that is path-scoped, incremental, and cost-aware, with a recorded ADR.
- Consistent PR-based history: `Merge pull request #N` plus follow-up `resolve review findings` commits show the review loop in the log.
- Release gating by ref: production can only deploy from the release branch.

## 7. Not Read / Not Verified

- Frontend and mobile CD workflows, mobile CI body, `.github/ocr-rules.json` beyond the summary above.
- GitHub branch protection, required checks, environment reviewers, and secrets. These are not in the repo.
- Whether any workflow currently passes.
