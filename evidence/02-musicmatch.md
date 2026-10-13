# Evidence: MusicMatch

Project root: `C:\WebApps\musicmatch`. HEAD `8494ded`. 32 commits from two GitHub handles of the same author (26 + 6).

## 1. Documented Process

| Artifact | What it establishes |
|---|---|
| `AGENTS.md` | Always-on agent rules. Language split: source code, git, and docs in International English (EN-INT). Chat in Portuguese (Brazil). |
| `PROJECT_CONTEXT.md` | Persona and direction for agents. Describes the engineering disciplines in play, the stack (Python 3.14.6, Rust, Pydantic V2, SQLite FTS5), and the target architecture diagram. Written in Portuguese, so it predates the EN-INT rule. |
| `docs/adr/` | **13 ADRs** (0001–0013). |
| `CHANGELOG.md` | Keep a Changelog format and SemVer, in pt-BR. Entries for 0.1.0 and 0.2.0 in progress. |
| `README.md` | Full project README with badges, architecture, stack, getting started, command reference. |
| `docs/` | Research and roadmap docs, including a database-scaling analysis and a yt-dlp technical report. |

## 2. Git Practice

- **Commit style:** Conventional Commits with module scopes: `feat(commands)`, `fix(downloader)`, `refactor(commands)`, `style(ui)`. Subjects are short and imperative.
- **PR flow:** Merge commits reference PR numbers (`Merge pull request #7 from ...`), and several branches follow `feat/`, `fix/`, `refactor/` prefixes. Issue linkage appears in branch names (`model-command-issue-5`).
- **Stale-ish message:** latest commit `Archaitectures definitions to expand library services` does not follow the convention. Minor, but it shows the convention is not enforced.
- **No hooks or commit linting** appear in the repo. *Unverified* whether any exist locally.

## 3. Testing Evidence

- `tests/` holds 20 `test_*.py` modules covering agent structure and execution, CLI, commands, domain models, downloader, harness loop, library and location services, model command, promotion, sanitizer, scanner, search, SQLite repo, staging, and UI renderer.
- **Count conflict:**
  - `README.md` badge and text: **87 tests, 98% coverage.**
  - `CHANGELOG.md` 0.1.0: **73 tests, 98% coverage.**
  - `grep -r "def test_" tests` returns **171** matches. This is a raw grep count and may include helpers or parametrized duplicates, so it is not a test count. *Unverified*, and the three numbers disagree.
- Coverage is reported as a README badge with no visible CI to enforce it. No CI workflow is tracked (see §5).

## 4. Architecture Decision Records

- 13 ADRs in `docs/adr/`. Examples: walking skeleton (0001), CLI REPL orchestrator (0002), didactic incremental evolution (0003), Pydantic domain modeling (0006), SQLite with FTS5 and a service layer (0007), idempotency and stat-cache lifecycle (0009), yt-dlp integration (0010), web-ingestion staging (0011), library governance (0012), library maintenance and deletion safeguards (0013).
- ADR 0009 has a clear structure: **Context → Decision → (consequences)**. Its decision is specific and testable: SHA-256 path-hash identity, stat-cache, soft-delete with `AVAILABLE | MISSING` status, and an explicit statement that the scanner never hard-deletes. This is strong reference material for the ADR template.
- **Drift:** `CHANGELOG.md` 0.2.0 says "ADRs 0001 a 0009". The folder has 13. The changelog is stale.

## 5. CI, CD, and Security Hygiene

- **No CI or CD workflow is tracked.** `git ls-files` finds no `.github/` directory. There is no automated test gate, no lint gate, and no release automation in the repo. The quality gate is the author running tests locally, despite the README claiming them.
- **Secrets:** `.env` is gitignored and not tracked. `.env.example` is tracked and documents `GEMINI_API_KEY`, `GEMINI_MODEL`, and `LOG_LEVEL`. `.gitignore` also covers `*.db`, `*.sqlite3`, `data/*` (except `.gitkeep`), `_MEDIA/`, and `*.local`. Good hygiene.
- **Dependency and runtime metadata:** `pyproject.toml` is PEP 621. `requires-python = ">=3.11"`, but the README badge says Python 3.14+ and the stack section says 3.14.6. This is a documentation/requirement mismatch, not a bug. The tool-config section in `pyproject.toml` is light: no ruff, mypy, or pyright configuration.
- **Version and packaging:** `version = "0.2.0"`, MIT license, a console script entry point (`musicmatch`).

## 6. Language Policy Evolution

This project shows a policy changing over time, which is useful evidence for Phase 2:

- `AGENTS.md` and `PROJECT_CONTEXT.md` §4 say: "from now on", all new docs, ADRs, and code use EN-INT. Existing Portuguese documents remain as historical record.
- The CHANGELOG is still pt-BR. `PROJECT_CONTEXT.md` is still in Portuguese.
- Result: a mixed corpus. The rule is correct, but the policy did not say whether existing docs should be migrated or frozen, and the `CHANGELOG` was not in the list.

## 7. Notable Design Practices

- **Command pattern for the interactive harness:** `CommandRegistry`, slash commands (`/scan`, `/search`, `/model`, `/promote`, `/download`, ...), and a `ConsoleUI` that separates presentation from logic.
- **Stub-first, didactic evolution** (ADR 0001, 0003): the walking-skeleton approach is documented as a decision, not left implicit.
- **Non-destructive data lifecycle** (ADR 0009): an explicit policy against hard deletes, important for a user's real music library.
- **Explicit cost awareness** in agent work: `/model` and the README both say deterministic commands run "without consuming LLM tokens".

## 8. Not Read / Not Verified

- Test suite not executed (to avoid writing caches into the project).
- ADR 0001–0008 and 0010–0013 were not read in full, only listed. ADR 0009 was read for its head.
- `docs/` research files were not read beyond titles.
- No local git hooks or lint configuration was found in the repo.
