# Evidence: Vibe Coding Benchmarks

Project root: `C:\WebApps\akita-vibe-coding-benchmarks\vibe-coding-benchmarks`. HEAD `286c245`. 28 commits, all by one author.

This is a research repo, not a product. Its SDLC lessons are about how it handles **evidence, reproducibility, and claims**, which is a different axis from the two application repos.

## 1. Documented Process

| Artifact | What it establishes |
|---|---|
| `README.md` | Entry point. Summarizes the completed ledger experiment and the queue experiment. States limits in the first screen. |
| `docs/README.md` | Documentation hub. Says where to start and lists supporting docs by question. |
| `docs/benchmark-design.md`, `docs/difficulty-audit.md`, `docs/task-catalog.md` | Experimental design, difficulty audit, task catalog. |
| `docs/measurement-and-analysis.md` | **Pre-specified measurement plan** (see §3). Status line: "proposed … freeze before confirmatory data." |
| `docs/setup.md` | Tutorial. Says to follow it before launching a matrix. |
| `docs/data/README.md` | Explains what is published, what is excluded, and how to recompute the public export. |
| `docs/*-audit.md`, `docs/*-validation.md` | Many audits: effort traces, semantic failures, artifact retention, matrix operational audits. |
| `AGENTS.md`, ADRs | **Not present.** No agent rules file, no ADR folder. |
| `.github/` | **Not tracked.** No CI workflows. |

## 2. Testing and Automation

- `tests/` holds about 30 modules and **287** `def test_` matches by grep. Coverage includes harness, batch, matrix, subscriptions for Claude and Codex, ledger oracles across Python, TypeScript, C#, Kotlin, Ruby, Rust, and Haskell, queue scenarios, public results export, packaging, and effort reporting. *Count is a raw grep, unverified by execution.*
- `pyproject.toml` declares `requires-python`, and dependencies. No lint or type-check configuration was found in the grep.
- **No CI.** Nothing runs the tests automatically. Quality rests on the author running them, plus the documented validation steps.
- `.gitignore` excludes `results/`, `.work/`, `.venv/`, and build trees, so raw experiment output stays out of git. The published dataset is separate (`docs/data/`).

## 3. Evidence Discipline (the core strength)

These are the practices that most distinguish this repo:

1. **Pre-declared outcomes and decision rules.** `docs/measurement-and-analysis.md` lists four primary outcomes (verified success, success under budget, total effort per launched attempt, critical failure rate), each with a denominator and reporting rule. It also says success is not determined by "the compiler exit code nor the agent's completion claim", and that "a green public test suite is also insufficient".
2. **Missing is not zero.** "Record fields as missing when absent, not zero." Missingness is reported by condition. Token efficiency is not ranked from success-only telemetry.
3. **Versioned, auditable parsers.** Raw events are preserved and parsed by a versioned parser. Provider definitions stay attached to each record. Token semantics (reasoning vs. output, cached vs. uncached) are defined before any total is computed, and the doc says to leave totals "unresolved" when semantics are unverified.
4. **Explicit anti-inference rules.** "Never infer unreported reasoning from wall time." "Ten compiler messages can arise from one bug; ten thousand failing generated cases are not ten thousand bugs."
5. **Frozen intervention protocol.** Nudge policy is fixed, independent of hidden grading, with frozen suggested texts (N1, N2) and a cap of two messages. Regressions caused by nudging successful runs are reported alongside rescues.
6. **Public / private split with a checkable export.** `docs/data/README.md` lists what is excluded (prompts, response bodies, account IDs, credentials, local paths, candidate source, logs). The export runs with a `--check` mode against closed reports, and source report SHA-256 hashes are preserved. Recompute path needs no Docker or subscriptions.
7. **Honest result framing.** `README.md`: "**No general language ranking is established.**" Limits are stated in the first screen, not buried. `docs/README.md` says the results are "exploratory" and "not a confirmed typing hierarchy."
8. **Reconciliation as a named activity.** Commit `Publish benchmark tutorial, reconciled results and sanitized measurements` shows that reconciling numbers across reports was a deliberate step.
9. **Preserving historical documents.** Superseded plans are kept but labelled: "historical," "not current collection status," "superseded by later instructions." The `docs/README.md` ends with an explicit supersession note.

## 4. Commit Practice

- Imperative, descriptive subjects with evidence-oriented verbs: "Report", "Separate", "Reject", "Serialize", "Qualify", "Explain", "Plan". Example: `Separate unsent allowance checks from Claude inference accounting`.
- Mostly Conventional-Commit-like in spirit but **without type prefixes**. The subjects are readable and specific, and they name what changed in measurement semantics. Strong for a research log, weaker for automated changelogs.

## 5. Documentation Volume

- `docs/` has roughly 45 files. Many are dated follow-ups (`followup-*`, `later-model-*`, `subscription-*`, `seven-language-*`, `scalability-*`), and the hub explains the order.
- **Risk:** overlap is high. The same campaigns are described in several files, and the reader needs the hub to navigate. Good hubs are an antidote, but the sprawl itself makes it hard to know which file is authoritative. The hub's "Start here" line helps.

## 6. Gaps

- **No CI and no lint/type gate** in the tracked files.
- **Reproducibility is conditional.** Grading needs a qualified Docker runtime; live collection needs pinned CLIs and subscriptions. The repo says so, which is honest, but it means most claims can be re-derived from published JSON only.
- **Single author, no review trail.** All 28 commits are by one person, so there is no evidence of an independent review step. Not a criticism of the work; it is a process fact that matters for what "reviewed" means here.
- **Language:** the docs are consistently English and there is no language policy file, so the convention is implicit. Only the chat with the maintainer is in Portuguese, and that is outside the repo.

## 7. Not Read / Not Verified

- Tests not executed.
- Most `docs/*-audit.md` and follow-up files were listed, not read. The measurement plan and the README/docs hubs were read in full or in part.
- `docs/data/matrix-results.json` was not parsed. Its numbers were taken from the README table, which should be re-checked against it before reuse.
