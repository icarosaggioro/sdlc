# Changelog

Changes to the SDLC compendium and its copy-in package. Format: Keep a Changelog. Versioning: the package version in `tools/build_package.py`.

## [Unreleased]

## [1.0.0] - 2026-10-12

### Added
- Compendium: 17 guides, 13 playbooks, 5 references, and the evidence survey of three reference projects.
- Solo and team profiles with the `team-profile` and `ships-to-users` switches (guide 00).
- Copy-in package (`package/`): root `AGENTS.md` pointer, general rules in `.agents/rules/instructions.md`, a project-owned `project.md`, guides, templates, 13 `sdlc-*` skills, a PR template, and an advisory AI review workflow.
- `tools/build_package.py` (generates and validates the package) and `tools/install-package.ps1` (dry run by default).

### Decided
- D13: LivroJogo is the internal name, Lore Vault the commercial name, "LoreVault" is a typo.
- D4: AI review is advisory permanently.
- D12: the final-review engineer triages AI findings at approval time.
- Solo profile adopted.
