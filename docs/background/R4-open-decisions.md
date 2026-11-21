# R4. Open Decisions

Choices the organization must make. Each has a proposed default, which the guides already assume. Change the default here and in the affected guides if you decide otherwise.

| # | Decision | Proposed default | Affects | Revisit when |
|---|---|---|---|---|
| D1 | Coverage policy | Team profile: ratchet, never drop below the current level, no absolute target. Solo profile: CI reports coverage | 06 | A critical module shows low coverage, or coverage tooling is in place for all repos |
| D2 | Solo-developer review | **Decided (solo profile):** the sole engineer is author and final reviewer, AI review is the second pair of eyes, 24-hour wait only for destructive migrations and data deletions, outside reviewer for high blast radius | 04, 16 | A second engineer joins |
| D3 | Required CI checks | Lint, types, tests, build, dependency scan | 07 | A check proves too flaky or slow |
| D4 | AI review status | **Decided:** advisory permanently, pinned action and model. It never becomes a merge gate, because the overhead on individuals outweighs the benefit | 04, 07, 15 | Only if the overhead concern changes |
| D5 | Commit and PR language | English | 00, 02 | Never expected to change |
| D6 | Merge method | Squash | 02 | History of individual commits becomes valuable |
| D7 | Production promotion pattern | Tag-based, with ref guard in the pipeline | 01, 12 | A release-branch flow is already in use (LivroJogo) and works |
| D8 | Review SLA | One business day | 04 | The team grows or becomes distributed |
| D9 | Post-incident review window | Five working days for Sev 1 and Sev 2 | 14 | After the first real incident |
| D10 | Backup retention | 14 database snapshots, 7 media snapshots | 13 | Storage cost or compliance needs change |
| D11 | AI review model and provider | A pinned model through OpenRouter, as in LivroJogo | 07, 15 | Cost, quality, or provider terms change |
| D12 | Who triages AI review findings | **Decided:** the review runs automatically when a PR is marked ready. Findings wait on the PR until an engineer is assigned for the final review; that engineer triages them and approves. No separate SLA | 04, 15 | The team grows enough that PRs wait too long for assignment |
| D13 | Canonical product naming | **Decided:** `LivroJogo` is the internal project and repository name; `Lore Vault` is the commercial product name; the spelling `LoreVault` is accidental and should be corrected. Lowercase compound identifiers (domain, branch and environment names) are fine | 10 | Never expected to change |
| D14 | Handling of legacy-language documents | Migrate on next edit; mark `Status: legacy` until then | 10 | Backlog of legacy files grows |

## Decision Log

Record each decision here when made:

| Date | Decision | Chosen | Who | Notes |
|---|---|---|---|---|
| 2026-10-12 | D13 naming | LivroJogo (internal), Lore Vault (commercial), "LoreVault" is a typo | Maintainer | Fix the display string in `X-Title` of the review workflow and any docs |
| 2026-10-12 | D4 AI review status | Advisory permanently, never a gate | Maintainer | Reason: overhead on individuals |
| 2026-10-12 | Solo profile | Adopted, with `team-profile` and `ships-to-users` as independent switches | Maintainer | Overhead concern for one-engineer projects |
| 2026-10-12 | D12 triage | Final-review engineer triages at approval time | Maintainer | Review runs automatically on ready-for-review |
| 2026-11-16 | D19 review tooling | No review tool that needs a subscription. Build the review tour as a package skill (`sdlc-review-tour`) instead of adopting GitLens Pro. GitLens Community stays optional on a workstation, never required by the package | Maintainer | A subscription is a dependency, however small the price. See R6 Part 10 |

## Still Open

D3, D5 to D11, and D14 keep their proposed defaults. D15 to D18 (review tooling) are proposed in [R6](R6-pr-review-tooling.md#part-7-decisions-to-record-in-r4). For the solo profile and its effect on D1 and D2, see [R5](R5-rollout-and-context-strategy.md).
