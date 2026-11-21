# R6. PR Review Tooling: Options and Recommendation

Status: **proposal, 2026-11-10; D19 decided 2026-11-16** (no subscription tools; `sdlc-review-tour` built). The rest is not adopted yet. Decisions this report asks for are listed in [Part 7](#part-7-decisions-to-record-in-r4). Facts about third-party tools were checked on the date above; vendor numbers are vendor claims, and items marked *unverified* come from secondary sources only.

## Part 1. The Problem

The maintainer's complaint, in three parts, and the root cause behind each:

| Pain | What it feels like | Root cause |
|---|---|---|
| **Hard diffs** | Long, noisy, line-based diffs; moves and reformatting look like rewrites; files shown in alphabetical order, not in the order that explains the change | The diff is rendered by a line-based tool in a web page, and the PR is shaped by the author, not for the reader |
| **Little context** | The diff hunk shows three lines around a change; no callers, no type definitions, no history; jumping to a definition means leaving the review | Reviewing in the GitHub web view, which has no language server and no repository-wide navigation |
| **Little control** | Cannot choose what to look at (one commit, one folder, only what changed since last round); the AI reviewer decides scope and posts whatever it finds | The AI review (Open Code Review in CI) runs on its own schedule, on the whole diff, and the reviewer has no local tool to ask it questions |

The current package (guide 04, skill `sdlc-review-pr`, workflow `ci-codereview.yml`) says **what** to check but nothing about **where and how** to read a PR. That is the gap this report fills.

## Part 2. What Is Already Installed

Inventory of the maintainer's workstation on 2026-11-10:

| Tool | Version | Used for review today? |
|---|---|---|
| Claude Code CLI | 2.1.309 | No review workflow defined |
| VS Code extension `anthropic.claude-code` | installed | No |
| VS Code extension `github.vscode-pull-request-github` (GitHub Pull Requests) | installed | Unknown |
| VS Code extension `github.vscode-github-actions` | installed | CI only |
| GitHub CLI `gh` | 2.100.0 | No extensions installed |
| Git | 2.54.0 | No pager, no external diff tool configured |
| Claude Code plugins | `mattpocock-skills` enabled; official marketplace cached, none of its review plugins enabled | `mattpocock-skills:code-review` exists but reviews against standards and spec, not as a PR reading aid |
| CI | Open Code Review (`alibaba/open-code-review@v1.12.13`) via OpenRouter | Yes, advisory (D4, D11) |

**Conclusion:** most of what is needed is already installed and unused. The cheapest improvement is a defined workflow, not new purchases.

## Part 3. The Options, Layer by Layer

Review quality depends on five layers. Tools at one layer cannot fix a problem at another: a better AI bot does not make a 2,000-line PR readable.

### Layer A. The shape of the PR (upstream of review)

| Option | What it does | Pain addressed | Cost |
|---|---|---|---|
| **Small PRs** (guide 02 already proposes 400 lines) | Less to read | Hard diffs | Discipline only |
| **Stacked PRs** with `gh stack` (`gh extension install github/gh-stack`, needs `gh` 2.90+) | Each PR in a chain targets the branch below it; reviewed and merged as a unit. GitHub previewed it in April 2026; secondary sources report general availability on 2026-10-06 (*unverified against GitHub's changelog*) | Hard diffs, control (review one layer at a time) | Free; learning curve; web "Rebase stack" makes unsigned commits |
| **Reviewable commits** | Author separates "move/rename", "reformat", and "behavior change" into distinct commits; reviewer reads commit by commit | Hard diffs (moves stop polluting the logic diff) | Discipline; conflicts with squash merge only in history, not in review |
| **A review guide in the PR description** | Author (or an agent) lists the files in reading order with one line each: entry point first, tests next, mechanical changes last | Context, control | 2 to 5 minutes per PR, or zero if an agent drafts it |

### Layer B. Where the PR is read

| Option | Context available | Control | Notes |
|---|---|---|---|
| GitHub web view (today) | Diff hunk only; "Expand" for more lines | "Viewed" checkbox, whitespace toggle, file filter | No go-to-definition, no find-references |
| **VS Code + GitHub Pull Requests extension** (installed) | Full checkout: language server, go-to-definition, find-references, run tests | Review tree, per-file "viewed", inline comments and suggestions posted to GitHub, approve or request changes from the editor | Comments land on the PR as if made on the web |
| **Local checkout in a git worktree** (`gh pr checkout` inside `git worktree add`) | Same as above, without disturbing the work in progress | Run, debug, and test the PR branch | Pairs with Claude Code, which can be started in that worktree |
| GitLens (not installed) | Blame, file and line history, Commit Graph inside VS Code | "Review Changes" mode: file checklist, "changed since viewed", AI reading plan | Private repos need Pro for the review features. Studied in [Part 10](#part-10-deep-dive-gitlens) |

### Layer C. How the diff is rendered

| Option | What it does | When to use |
|---|---|---|
| `git diff --color-moved=dimmed-zebra --color-moved-ws=allow-indentation-change` | Built into git. Marks moved blocks so they stop looking like delete plus add | Every refactor; set it once in git config |
| `git diff -w` / GitHub "hide whitespace" | Hides reindentation | Reformatting mixed with logic |
| `git range-diff main old-tip new-tip` | Built into git. Shows what changed **between two versions of a branch** after a force-push or rebase | Second review round: "re-check only what changed" (step 10 of `sdlc-review-pr`) without re-reading everything |
| **difftastic** (`difft`) | Structural diff: parses the code with tree-sitter and diffs syntax, not lines. Ignores formatting-only changes | Refactors and AI-generated code. Slow and memory-hungry on very large diffs; output is not a unified diff, so do not pipe it into scripts |
| **delta** | Pager that renders line diffs side by side with syntax highlighting | Daily `git diff` / `git log -p` reading in the terminal |

difftastic and delta are complementary: delta as the pager, difftastic on demand through an alias (for example `git dft` = `git -c diff.external=difft diff`).

### Layer D. AI assistance at the reviewer's desk (local, on demand)

This is where "control" is won back: the reviewer decides what the AI looks at and when.

| Option | What it does | Scope control | Cost |
|---|---|---|---|
| **Built-in `/code-review`** (alias `/review`) | Correctness review of a diff, running as a background subagent. Levels `low` to `max` trade recall for noise. `--fix` applies findings; `--comment` posts inline comments on the GitHub PR; `--max-findings <n>` caps output | **High.** Target can be the branch, a range (`HEAD~3..HEAD`, `main...feature`), a PR number, or a path (`src/auth`) | Included in the Claude subscription |
| `/code-review ultra` | Multi-agent review in an Anthropic cloud sandbox; each finding independently verified; 5 to 15 minutes; `--post` puts the result on a github.com PR as one comment | PR number or branch | Pro, Max, and Ultra: 3 free runs per account, then usage credits, typically 5 to 25 USD per review. Research preview. Use only when a reviewer explicitly asks for it |
| `/simplify` | Cleanup review (reuse, simplification); applies fixes | Current diff | Subscription |
| `/security-review` | Built-in security pass on pending changes | Current branch | Subscription. Listed in the docs without detail; *behavior not verified* |
| Plugin **`pr-review-toolkit`** (official marketplace) | Six specialist agents: `comment-analyzer`, `pr-test-analyzer`, `silent-failure-hunter`, `type-design-analyzer`, `code-reviewer`, `code-simplifier`. Command `/pr-review-toolkit:review-pr`; agents can also be asked for individually | **High:** pick one aspect ("check the error handling") | Subscription. Local only, posts nothing |
| Plugin **`code-review`** (official marketplace) | Four parallel agents (two for CLAUDE.md compliance, one bug scan, one git-history analysis); confidence score 0 to 100, reports only 80 and above. `--comment` posts to the PR | Current PR | Subscription. This is also the plugin the official GitHub Action example runs |
| Plugin **`security-guidance`** | Warns on dangerous patterns while Claude edits, reviews Claude's diff at the end of a turn, reviews on `git commit` | Prevention, not review | Subscription. Acts on code Claude writes; useful for the author side |
| Plugin **`claude-security`** | Threat model plus verified findings; "Scan changes" mode covers a branch or PR diff | Branch, PR, or commit | Subscription; heavy. For changes in the security or data paths of guide 04 rule 3 |
| **A "PR tour" prompt** (proposed skill, Part 6) | Claude reads the PR in the worktree and writes a reading guide: intent, files in reading order, call sites of changed functions, risky spots, what the tests do and do not cover. It **does not judge**; it orients | **Full:** the reviewer asks follow-up questions in the same session | Subscription |
| Claude Code VS Code extension | Side-by-side diffs for Claude's own edits; `Alt+K` inserts an `@file#L5-10` reference to the selection, so you can ask about exactly the lines you are looking at | Line-level | Subscription |
| CodeRabbit VS Code extension | Reviews uncommitted or committed local changes before a PR exists | Working tree, or all changes | Free with a CodeRabbit account, rate-limited per hour |

Notes:

- Local `/code-review` follows `CLAUDE.md`, not `REVIEW.md`. Projects installed with `--harness claude` already have a `CLAUDE.md` that imports the rules, so the review sees the project's rules.
- `mattpocock-skills:code-review` (already enabled) reviews against coding standards and the originating issue. It is a good complement for "does this match the spec", not a reading aid.

### Layer E. AI review in CI (automatic, advisory)

Decision D4 stays: whatever runs in CI is advisory and never a merge gate.

| Option | Context | Output | Cost | Fit |
|---|---|---|---|---|
| **Open Code Review** (today) | Diff, incremental | Sticky summary plus comments | OpenRouter tokens, pinned model (D11) | Works; keep as baseline |
| **`anthropics/claude-code-action@v1` + `code-review` plugin** | Full checkout: the agent can read any file and the git history | Inline comments via `mcp__github_inline_comment__create_inline_comment`; one summary comment if no inline findings | `ANTHROPIC_API_KEY` (pay per token) or `CLAUDE_CODE_OAUTH_TOKEN` (subscription). Setup: `/install-github-app` | Same engine as the local `/code-review`, so CI findings and desk findings speak the same language. Also answers `@claude` questions in PR threads |
| **Claude Code Review (managed)** | Multi-agent, verification step, severity markers (Important, Nit, Pre-existing), check run that never fails | Inline comments plus summary; `@claude review` commands | **Team and Enterprise plans only** | Not available on an individual plan. Revisit if the organization moves to Team |
| GitHub Copilot code review | Diff only, per secondary sources | Inline comments | Bundled with Copilot seats | Only if Copilot is already paid for |
| CodeRabbit | Diff plus walkthrough; broad platform support | Walkthrough, inline comments, chat | About 24 USD per developer per month (Pro, annual) | Strong walkthrough feature; another vendor and another data processor |
| Greptile | Indexes the whole repository | Inline comments | About 30 USD per seat plus credits | Best cited for cross-file context |
| Qodo | Review plus test generation; on-prem option | Inline comments, suggested tests | Varies | Only if test generation or on-prem matters |

Published benchmarks for these bots conflict and most are run by vendors (CodeRabbit, Qodo, Greptile, and Macroscope each lead their own). Per guide 15, **no general ranking is established**; only a trial on our own PRs would settle it.

## Part 4. Fit Against the Three Pains

Scores: ●●● strong, ●● partial, ● weak, ○ none.

| Option | Hard diffs | Context | Control | Effort to adopt |
|---|---|---|---|---|
| Small PRs and reviewable commits | ●●● | ● | ●● | Habit |
| Stacked PRs (`gh stack`) | ●●● | ● | ●●● | Medium |
| VS Code + GitHub PR extension, local worktree | ●● | ●●● | ●●● | Low (installed) |
| `--color-moved`, `range-diff`, difftastic, delta | ●●● | ○ | ●● | Low |
| Claude "PR tour" (proposed skill) | ●●● | ●●● | ●●● | Low |
| Built-in `/code-review` at a chosen level and path | ● | ●● | ●●● | None (installed) |
| `pr-review-toolkit` specialist agents | ● | ●● | ●●● | One command |
| claude-code-action + `code-review` plugin in CI | ● | ●● | ● | Medium (secrets, workflow) |
| Managed Claude Code Review | ● | ●●● | ● | Blocked by plan |
| CodeRabbit / Greptile / Copilot bots | ●● (walkthroughs) | ●● | ● | Medium; recurring cost |

The pattern is clear: **CI bots address none of the three pains well.** They add findings, but the pains are about **reading**. The high scores sit in the local layers (B, C, D), most of which are already installed.

## Part 5. Recommendation: Local-First Review

Move the review from the browser to the editor, with Claude as a guide first and a critic second.

### The target workflow (one PR)

1. **Check out the PR in its own worktree**, so work in progress is untouched:
   `git worktree add ../review-123` then, inside it, `gh pr checkout 123`.
2. **Open it in VS Code** with the GitHub Pull Requests extension. Comments, suggestions, and the final decision are posted from there.
3. **Ask Claude for a tour** (new skill `sdlc-review-tour`, Part 6) in that worktree. Read the PR in the order the tour gives, using go-to-definition and find-references for context. Ask follow-up questions in the same session, pointing at lines with `Alt+K`.
4. **Read structurally where it helps:** `git dft main...HEAD -- <path>` for refactors; `--color-moved` is on by default in git config.
5. **Ask for a second opinion, scoped by you:** `/code-review medium` on the whole PR, or `/code-review high src/billing` on the risky folder, or one `pr-review-toolkit` agent ("check silent failures in this PR"). Treat findings as hints, as `sdlc-review-pr` step 4 already says for the CI bot.
6. **Triage the CI bot's findings** (Open Code Review, unchanged) as guide 04 requires.
7. **Decide** from VS Code: approve, approve with comments, or request changes.
8. **Second round:** `git range-diff` between the old and new tips, then review only what changed.
9. **Remove the worktree** after merge: `git worktree remove ../review-123`.

In a **solo** repo the same flow is the "re-read the diff after a break" step of guide 04, done with context instead of in the browser. It also covers the author's own self-review before opening the PR: steps 3 to 5 run on the branch before `sdlc-open-pr`.

### What not to do now

- **Do not replace Open Code Review yet.** It works, it is pinned, and switching CI bots does not address the pains. Revisit after the trial in Part 8.
- **Do not buy a review bot** (CodeRabbit, Greptile). Recurring cost, a new data processor, and the same blind spot as every bot: they do not change how the human reads.
- **Do not use `/code-review ultra` routinely.** Three free runs, then paid. Reserve it for high-blast-radius PRs (guide 04 rule 3), and only on an explicit request.

## Part 6. Proposed Changes to the Package

Ordered by value; each is a separate PR to this repository.

| # | Change | Files | Size |
|---|---|---|---|
| 1 | **Done (D19).** **New skill `sdlc-review-tour`**: produce a reading guide for a PR or branch without judging it. Output: intent in two sentences; files in reading order with one line each; changed public functions and their call sites; what the tests cover and what they do not; spots worth a second look; mechanical changes to skim. Stop point: hands control back to the human; never posts to the PR | `package/.agents/skills/sdlc-review-tour/SKILL.md`, README skill list, `check_package.py` count if it is hard-coded | S |
| 2 | **Rewrite `sdlc-review-pr`** around the local-first workflow of Part 5: worktree checkout, tour, scoped second opinion, `range-diff` on later rounds. Keep it tool-neutral (works with Codex, OpenCode, Antigravity); name Claude Code commands only as examples | `package/.agents/skills/sdlc-review-pr/SKILL.md` | S |
| 3 | **Guide 04: add a "How to Read a PR" section**: review in the editor with a checkout, not in the browser, for anything above trivial; reading order; structural diff for refactors; `range-diff` for re-review; author duty to separate mechanical from behavioral commits | `package/.agents/guides/04-code-review.md` | S |
| 4 | **Guide 02: optional review guide in the PR description**, and a pointer to stacked PRs as the scale-up for large changes | `package/.agents/guides/02-commits-and-pull-requests.md`, `package/.github/pull_request_template.md` (optional "Reading order" section) | S |
| 5 | **R1 templates: a recommended git config block** (`diff.colorMoved`, `diff.colorMovedWS`, a `dft` alias, optional delta pager) | `package/.agents/references/R1-templates.md` | XS |
| 6 | **`docs/ADOPTING.md`: Claude Code review setup** for the `claude` harness: which official plugins to enable (`pr-review-toolkit`; optionally `security-guidance`), and that local `/code-review` reads `CLAUDE.md` | `docs/ADOPTING.md` | XS |
| 7 | *(After the trial)* **Optional CI variant** `ci-codereview-claude.yml` using `anthropics/claude-code-action@v1` with the `code-review` plugin, pinned, advisory, skipping drafts and bots like the current workflow | `package/.github/workflows/` | M |

Changes 1 to 6 bump the package to 1.3.0 (minor: new skill, no breaking change). Change 7 is a separate decision.

## Part 7. Decisions to Record in R4

| # | Decision | Proposed default |
|---|---|---|
| D15 | Where PRs are read | Locally, in a worktree, in the editor, for every PR that is not trivial. The browser is fine for typo-level changes |
| D16 | Local AI review tool | The agent's built-in review (Claude Code `/code-review`, with `pr-review-toolkit` agents for scoped questions). Advisory, like D4 |
| D17 | CI review bot | Keep Open Code Review (D11) until the trial in Part 8 is done; then decide between it and claude-code-action with the `code-review` plugin |
| D18 | Paid review services (managed Code Review, `ultra`, third-party bots) | Not adopted. `ultra` only on explicit request for high-blast-radius PRs |
| D19 | Review tools that need a subscription, GitLens included ([Part 10](#part-10-deep-dive-gitlens)) | **Decided 2026-11-16:** none adopted. A subscription is a dependency, however small the price. The tour is a package skill (`sdlc-review-tour`). GitLens Community may be used on a workstation, never required by the package |

## Part 8. How to Know It Worked

Following the evidence discipline of guide 15: state the measure before collecting results.

- **Trial:** the next 10 PRs in LivroJogo, reviewed with the local-first workflow.
- **Record per PR** (one line in a scratch file): lines changed; minutes spent reviewing; issues found by the human, by `/code-review`, and by Open Code Review; for each AI finding, accepted or dismissed.
- **Questions the trial answers:**
  1. Does the tour cut the time to understand a PR? Compare with an impression of the last 10 PRs, and say that the baseline is an impression.
  2. How often do `/code-review` and Open Code Review find the same issue? If almost always, one of them is redundant (input to D17).
  3. Which `/code-review` level gives findings worth keeping without noise? Start at `medium`.
- **Missing is not zero:** if a PR was reviewed the old way, mark it as missing, not as a zero.

## Part 9. Limits and Unverified Items

- The GA date of GitHub stacked PRs comes from secondary sources only.
- The behavior of `/security-review` is not documented in the pages read.
- The GitHub Pull Requests extension's latest features were not checked against its changelog. GitLens limits are in [Part 10.8](#108-unverified-and-conflicting).
- AI review bot benchmarks are vendor-run and contradict each other.
- Pricing (managed Code Review, `ultra` credits, CodeRabbit, Greptile) changes often; re-check before any purchase.
- Local plugin details (`pr-review-toolkit`, `code-review`, `security-guidance`, `claude-security`) were read from the official marketplace copy cached on this machine on 2026-11-10.

## Part 10. Deep Dive: GitLens

Added 2026-11-16 at the maintainer's request. GitLens is GitKraken's Git extension for VS Code (`eamodio.gitlens`), about 54 million installs. Current version: **19.6, released 2026-11-10**.

### 10.1 Why it matters here

GitLens recently added a **Review Changes** mode in its Commit Graph. Two of its functions are things this report had planned to build or to do by hand:

| R6 proposal | GitLens equivalent |
|---|---|
| `sdlc-review-tour` skill (reading guide, Part 6 item 1) | **Orient** (AI): a "Reading plan" that groups the files, gives one line per file, and sets the reading order |
| `git range-diff` for the second round (Part 5 step 8) | Per-file "Viewed" marks with **"changed since viewed"** tags. Marks, findings, and comments carry over through amend and rebase |
| Scoped second opinion with `/code-review` (Part 5 step 5) | **Review Diff** (AI) on the files in the checklist, and **Review in Repo**, which hands the review to a coding agent (Claude Code among them) |

So the question is whether to adopt GitLens for these, or keep building them on the agent side.

### 10.2 Features relevant to review

| Feature | What it does | Pain addressed | Tier |
|---|---|---|---|
| Inline blame, hovers, CodeLens, file and line history, revision navigation | Who changed a line, when, and in which PR, without leaving the file | Context | **Free, every repository** |
| Commit Graph | Visual history; entry point for Review Changes | Context | Free on public and local repos; **Pro on private repos**. Signed out, private repos get a 3-day preview |
| **Review Changes** (non-AI part) | Changed files as a checklist; scope presets "Uncommitted", "Unpushed", "Branch"; "Exclude from Review"; progress ("1 of 3 viewed"); keys for previous file, next file, and "mark viewed and go to next"; "changed since viewed" | Control, hard diffs | Free on public and local; **Pro on private** |
| **Orient** (AI) | Reading plan with groups and per-file notes | Hard diffs, context | Pro or above |
| **Review Diff** (AI) | Findings tagged Critical, Warning, or Suggestion, shown as comment threads on the diff lines; custom instructions through `gitlens.ai.reviewChanges.customInstructions` | Second opinion | Pro or above |
| **Review in Repo** | Starts your coding agent (`gitlens.ai.defaultAgent`), gives it the changes plus existing findings and comments; the agent can build, test, and trace calls; results arrive tagged "Agent" | Context, second opinion | Not stated |
| Start Review / Launchpad | Pick a PR from the host, check it out as a branch or in a new worktree, optionally open an agent; Launchpad lists PRs by state (Needs Your Review, Ready to Merge, Blocked) | Control | Pro. Launchpad is built for teams with many open PRs |
| Worktrees view | Manage worktrees in the UI | Control | Free on public and local; Pro on private. Plain `git worktree` is free everywhere |
| Agent Sessions and GitKraken Hooks | Tracks Claude Code, Codex, Copilot CLI, and OpenCode sessions in the Commit Graph; answers Claude Code permission prompts from the UI | None of the three | Conflicting: Pro, or free on public repos |
| GitKraken MCP | Exposes Start Work, Start Review, Launchpad, and Commit Composer to agents such as Claude Code | None directly | Conflicting: free or Pro |
| Code Suggest | Removed from Launchpad in 19.0 (2026-08-12) | n/a | n/a |

### 10.3 Cost

| Plan | Price (USD, per seat per month, billed annually) | Notes |
|---|---|---|
| Community | Free | No GitKraken AI |
| Pro | about 4.95 (*third-party trackers; the official page did not render prices; trackers disagree*) | Up to 2 seats; 1,000,000 AI credits per week |
| Advanced | 14 from 2026-07-08 (*reseller notice*) | Up to 10 seats; 2,000,000 credits |
| Business | about 18 (216 per year, *reseller notice*) | Up to 100 seats |
| Trial | Free, 14 days, no credit card | 250,000 AI credits per week during the trial |

AI can also run with your own key ("bring your own key": OpenAI, Google, Mistral, Azure, OpenRouter, any OpenAI-compatible API, or local Ollama models). The OpenRouter account already used by the CI review (D11) would fit. With your own key, GitKraken says only usage metadata reaches it. GitHub Copilot can also be the provider, and then the Copilot-capable AI features are free.

### 10.4 Fit with the maintainer's repositories

| Repository | Visibility | What GitLens gives for free |
|---|---|---|
| LivroJogo | **Private** | Blame and history only. Review Changes, Commit Graph, and Worktrees view need Pro |
| MusicMatch | Public | Everything except AI |
| Vibe Coding Benchmarks | Public (not owned) | Everything except AI |
| sagglabs-sdlc | Public | Everything except AI |

LivroJogo is where PRs, CI, and the AI review actually happen. **For the repository that matters most, the review features are paid.**

### 10.5 Strengths

1. **Review state lives in the editor.** The checklist, "viewed" marks, and "changed since viewed" fix the "little control" pain better than anything else in this report except stacked PRs. Carrying marks over a rebase is something neither GitHub's web view nor `range-diff` does as smoothly.
2. **Orient is the tour, already built**, with a UI to follow it.
3. **Agent-neutral.** Review in Repo hands off to Claude Code, so it does not compete with the local-first workflow; it frames it.
4. **Blame and history are free on every repository** and address the "little context" pain on their own.
5. **Cheap to try:** the 14-day trial needs no card.

### 10.6 Weaknesses and risks

1. **Paid where it counts** (private LivroJogo), and the price is not confirmed from an official source.
2. **Its own AI layer.** GitKraken AI is a second AI provider, next to Claude Code and OpenRouter. GitKraken says request content is "never stored or monitored" and not used for training. The same FAQ says it uses Google Gemini, while the release notes list many providers. Using your own key or Review in Repo avoids this.
3. **Moves fast, and features change.** Code Suggest was removed in 19.0; version 19.6 came out six days before this study; the help center menu still says "v18.x".
4. **The documentation contradicts itself.** The study found 13 conflicts between official pages (Part 10.8). Plan for surprises.
5. **Comments may stay local.** The pages do not say whether "Leave a Comment" in Review Changes posts to the GitHub PR. If it does not, comments to the author still go through the GitHub Pull Requests extension or the web. *Unverified; test during the trial.*
6. **Telemetry** is not covered by any page read; no statement that it follows VS Code's `telemetry.telemetryLevel`.
7. **UI weight.** Launchpad, Home, Agent Sessions, Cloud Patches, and Workspaces are aimed at teams; for one engineer most of it is noise and can be hidden.
8. **Vendor lock-in for review state.** Viewed marks and findings live in GitLens, not in the PR.

### 10.7 Decision (D19, 2026-11-16)

**GitLens Pro is not adopted.** On the merits it was the best reading surface found, but its review features are paid on the repository that matters (LivroJogo), and the maintainer ruled out tools that require a subscription: however small the price, it is a recurring cost and a dependency on a vendor whose features and tiers change often.

Consequences:

1. The reading guide is built as a package skill, `sdlc-review-tour` (Part 6 item 1, done). It works with any agent the package supports, needs no account, and has no recurring cost beyond the agent already in use.
2. The functions GitLens offered map to free equivalents:

| GitLens Pro | Free equivalent in the workflow |
|---|---|
| Orient (reading plan) | `sdlc-review-tour` |
| "Changed since viewed" | `git range-diff`, and the second-round mode of `sdlc-review-tour` |
| Viewed checklist | "Viewed" checkbox in the GitHub Pull Requests extension or the GitHub web view |
| Review Diff (AI) | `/code-review` at a chosen level and path, or a `pr-review-toolkit` agent |
| Review in Repo | Claude Code started in the review worktree |
| Start Review in a worktree | `git worktree add` plus `gh pr checkout` |

3. GitLens **Community** (free: blame, hovers, line history on every repository) may be installed on a workstation for context. The package never requires or names it as a dependency.
4. The trial in Part 8 compares the local-first workflow with the tour against the old browser review, without GitLens.

### 10.8 Unverified and conflicting

- USD prices: no official figure rendered; third-party numbers only.
- Whether Review Changes comments post to GitHub.
- Whether a PR can be reviewed in Review Changes without checking out its branch.
- Tier of Review in Repo, the Pull Requests side-bar view, and Search & Compare.
- Telemetry behavior.
- Conflicts between official pages: current version (19.6 vs "v18.x" menu); account needed for Commit Graph on public repos; tier of GitKraken MCP, Agent Sessions, AI Changelog, self-hosted integrations, Bitbucket, and Code Suggest; which tier the trial gives (Pro vs Advanced); "Unlimited" vs "Limited" integrations on Community; whether PRO-tagged features are free on public repos; which models GitKraken AI uses.

GitLens sources (read 2026-11-16):
- [GitLens on the VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)
- [Release notes](https://help.gitkraken.com/gitlens/gitlens-release-notes-current/)
- [Core features](https://help.gitkraken.com/gitlens/gitlens-features/)
- [Review Changes in the Commit Graph](https://help.gitkraken.com/gitlens/gl-review-changes/)
- [Accelerate PR reviews](https://help.gitkraken.com/gitlens/gl-accelerate-pr-reviews/)
- [Agents](https://help.gitkraken.com/gitlens/gl-agents/)
- [GitKraken AI](https://help.gitkraken.com/gitlens/gl-gk-ai/) and [GitKraken AI FAQ](https://help.gitkraken.com/general/gitkraken-ai-faq)
- [Launchpad](https://help.gitkraken.com/gitlens/gl-launchpad/)
- [Community vs Pro](https://help.gitkraken.com/gitlens/gitlens-community-vs-gitlens-pro/)
- [Security](https://help.gitkraken.com/gitlens/gl-security/)
- [GitLens FAQ](https://help.gitkraken.com/gitlens/gitlens-faq/)
- [Pricing](https://www.gitkraken.com/pricing) (prices did not render)
- [GitKraken new list prices (Schneider, reseller)](https://www.schneider.im/lu/gitkraken-new-list-prices-for-new-sales-and-renewals/)
- [GitLens pricing (SoftwareSuggest, third party)](https://www.softwaresuggest.com/gitlens/pricing)
- [Launchpad issue #5863](https://github.com/gitkraken/vscode-gitlens/issues/5863)

## Sources

Claude Code (official documentation, read 2026-11-10):
- [Code Review (managed)](https://code.claude.com/docs/en/code-review)
- [Local code review](https://code.claude.com/docs/en/code-review-local)
- [Ultrareview](https://code.claude.com/docs/en/ultrareview)
- [GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [Discover plugins](https://code.claude.com/docs/en/discover-plugins)
- [VS Code extension](https://code.claude.com/docs/en/vs-code)
- Plugin READMEs in the `claude-plugins-official` marketplace (local cache)

Diff tools and GitHub:
- [GitHub Stacked PRs: a practical guide to gh stack](https://flaviocopes.com/github-stacked-prs/)
- [InfoQ: GitHub stacked PRs](https://infoq.com/news/2026/04/github-stacked-prs)
- [Difftastic, my new favourite diff viewer](https://pawelgrzybek.com/difftastic-my-new-favourite-diff-viewer/)
- [Difftastic review](https://jpk.io/dev-tools/difftastic-structural-diff-review/)
- [Extensions for GitHub pull requests in VS Code (Graphite)](https://graphite.dev/guides/github-pull-request-extensions-vs-code)
- [How to review pull requests in VS Code (2026)](https://dev.to/rahulxsingh/how-to-review-pull-requests-in-vs-code-2026-3fga)

AI review services:
- [CodeRabbit IDE docs](https://docs.coderabbit.ai/ide)
- [AI code review tools compared (Coderbuds)](https://coderbuds.com/blog/ai-code-review-tools-comparison-2026)
- [Greptile vs CodeRabbit vs Qodo (Levelop)](https://levelop.dev/blog/best-ai-code-review-tools-2026-coderabbit-greptile-qodo-compared)
- [Best Greptile alternatives (Macroscope)](https://macroscope.com/content/best-greptile-alternatives-ai-code-review)
- [Anthropic Code Review for Claude Code (DEV Community)](https://dev.to/umesh_malik/anthropic-code-review-for-claude-code-multi-agent-pr-reviews-pricing-setup-and-limits-3o35)
