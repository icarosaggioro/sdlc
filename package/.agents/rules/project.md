---
trigger: always_on
---

# Project Rules

Project-owned. The SDLC package never overwrites this file. Fill in the fields; delete what does not apply.

- Name: <internal name> (commercial: <product name, if different>)
- team-profile: solo
- ships-to-users: no
- Stack and forbidden choices: <for example: Django + DRF + SQLite; no other backend frameworks>
- Commit scopes: <for example: backend, frontend, mobile, ci, docs>
- Release pattern: none | tag | release-branch (<name>)

## Commands
- install: <command>
- check: <one command that runs lint, types, tests, and build>

## Data contracts and safety
- <schema file to validate against; operations forbidden in this project>

## Docs map
- Requirements: <path>
- Glossary: <path>
- ADRs: `docs/adr/`
- Environments and topology: <path>
