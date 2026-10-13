# SDLC Evidence Survey: Index and Method

Survey date: 2026-10-12. This is the record of Phase 1 (evidence gathering). Phase 2, the consolidation into guides, skills, and references, is the `package/` folder at the repository root.

## Scope

| # | Project | Path | Repo HEAD at survey | Commits |
|---|---------|------|---------------------|---------|
| 1 | LivroJogo / Lore Vault | `C:\WebApps\livrojogo` | `b7dc1e7` | 471 |
| 2 | MusicMatch | `C:\WebApps\musicmatch` | `8494ded` | 32 |
| 3 | Vibe Coding Benchmarks | `C:\WebApps\akita-vibe-coding-benchmarks\vibe-coding-benchmarks` | `286c245` | 28 |

Working trees were clean (`git status --short` empty) when surveyed.

## Method and Constraints

- **Read-only on projects.** Only `ls`, `find`, `git log`, `git ls-files`, `git status`, `cat`, `head`, `grep`, and `wc` were used against the project folders. No tests, builds, installs, or formatters were run, because they write caches or artifacts inside the projects. Test counts below come from grepping source, not from executing suites.
- **Writes only here.** All outputs were written under this repository (this folder is `docs/background/evidence/`).
- **Evidence is cited by file path** relative to each project root. Claims marked *unverified* were read from docs and not confirmed in code or CI execution.
- **Language.** These files are in English, following the EN-INT convention that two of the three projects already use for technical documents. Chat stays in Portuguese.

## Files

- [01-livrojogo.md](01-livrojogo.md): CI, CD, code review, agent rules, release process.
- [02-musicmatch.md](02-musicmatch.md): agent steering, ADRs, changelog, language policy, secret hygiene.
- [03-vibe-coding-benchmarks.md](03-vibe-coding-benchmarks.md): evidence and measurement discipline for a research repo.
- [04-practices-matrix.md](04-practices-matrix.md): cross-project comparison, candidate practices, and anti-patterns. Input for Phase 2.

## Limits of This Survey

- Branch protection, required status checks, and environment reviewers live in GitHub settings and are not visible from the local clone. Claims about them are *unverified*.
- Workflows were read, not executed. Whether they pass today is unknown.
- Samples were read, not exhaustively audited. Each file lists what was and was not opened.
