# Changelog

Changes to the SDLC compendium and its copy-in package. Format: Keep a Changelog. Versioning: the package version in `package/.agents/SDLC_VERSION`.

## [Unreleased]

## [1.1.0] - 2026-10-13

### Added
- `tools/install_package.py`: cross-platform installer (Windows, Linux, macOS), standard library only. Dry run by default, never overwrites `project.md` or `.github/*`, saves conflicts as `.bak`, writes the version marker only when no conflict is pending, ignores CRLF versus LF.
- `tools/check_package.py`: validates guides, skills, referenced paths, leftovers, and that `SDLC_VERSION` matches this changelog.
- `.gitattributes` to keep LF line endings on every platform.

### Changed
- `package/` is now the single source of truth and the payload; there is no build step.
- The survey, evidence map, decisions log, and rollout analysis moved to `docs/background/`.
- The check-command example in guide 07 and `sdlc-bootstrap-repo` is OS-neutral (`scripts/check`).
- The package README documents the installer.
- `README.md` and `docs/ADOPTING.md` rewritten for the new layout.

### Removed
- `tools/build_package.py`, `tools/install-package.ps1`, `package-src/`, and the duplicated `guides/`, `playbooks/`, and `references/` sources. Nothing had been installed from 1.0.0 yet, so there is no migration.

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
