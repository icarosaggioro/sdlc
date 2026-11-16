---
name: sdlc-review-tour
description: "Use before reviewing a PR or branch, or before self-reviewing your own. Read the change and write a reading guide for the human reviewer: intent, files in reading order, call sites of changed code, what the tests cover and miss, spots worth a second look, and what to skim. Orients only; it never judges, posts, or approves."
---

# Review Tour

**Trigger:** a human is about to review a PR or a branch (their own or someone else's) and asks for a tour. **Guides:** 02, 04, 15 (in `.agents/guides/`).

The tour makes the human's reading faster and better informed. It is not a review: no verdicts, no "looks good", no findings to fix. For a second opinion, the reviewer asks for one separately.

## Steps

1. **Pin the target.** A PR number, a branch, or a range. Work on a local checkout, ideally a worktree, so the reviewer can follow along in the editor:
   `git worktree add <dir>`, with `<dir>` outside the repository (for example a sibling folder `review-<n>`), then `gh pr checkout <n>` inside it. Find the base: the PR base branch, or the merge base with `main`.
2. **Read the intent.** The PR description and the linked issue with its acceptance criteria. If there is none, say so and infer the intent from the commits, marking it as inferred.
3. **Measure the change.** `git diff --stat -M <base>...HEAD`. If it is over roughly 400 changed lines, say so at the top and suggest how it could have been split (guide 02). Then continue.
4. **Classify every changed file** into one of:
   - **Behavior:** production code whose logic changes.
   - **Tests.**
   - **Mechanical:** renames and moves (`git diff -M --color-moved=dimmed-zebra`), formatting only (empty under `git diff -w`), generated files, lockfiles, snapshots.
   - **Config and infrastructure:** CI, deploy, environment, migrations.
5. **Find the entry point:** where the new behavior starts (route, command, handler, public function, job). The reading order starts there and follows the call path.
6. **Trace the context the diff hides.** For each changed public function, type, or schema: who calls it (search the whole repository, not just the diff) and which callers did **not** change but depend on the old behavior.
7. **Read the tests against the intent.** What each changed test asserts. Which acceptance criteria and failure paths have no test. Flag tests that were deleted, skipped, or weakened (guide 15, "Reviewing AI-Written Code").
8. **Mark the spots worth a second look**, as locations and questions, never verdicts. Guide 04 lists what to look for: failure paths, security, data, operability. Always list anything touching auth, secrets, migrations, deletions, or production config.
9. **Write the tour** in the format below, in the chat language. Use `path:line` references so the reviewer can jump to each one.
10. **Hand control back.** Answer follow-up questions about specific lines. Do not continue into a review unless asked.

## Second Round

When the author pushed changes after a first review, tour only the delta: `git range-diff <base> <old-tip> <new-tip>`. Say which earlier questions the new commits touch and what is new. If the old tip is unknown, ask for it or use the PR's last reviewed commit.

## Tour Format

```
Intent: <two sentences; mark "inferred" if no issue or description>
Size: <files, lines>; <split suggestion if over ~400 lines>

Reading order
1. <path:line>, <one line: what changes here and why it is read first>
2. ...

Context the diff does not show
- <changed symbol>: called from <path:line>, <path:line>; <unchanged caller that depends on old behavior>

Tests
- Covered: <criterion or path> by <test>
- Not covered: <criterion or failure path>
- Changed or removed assertions: <test>, <what changed>

Worth a second look
- <path:line>: <question, not verdict>

Skim
- <mechanical files, grouped: moves, formatting, generated, lockfiles>
```

**Never:** post to the PR, approve, request changes, push commits, or rate the change. Do not run code that writes data or calls external services; reading and searching are enough.

**Stop and ask a human if:** the target or its base is ambiguous, or the checkout fails.
