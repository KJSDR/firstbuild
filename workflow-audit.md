# Workflow Audit — Claude Code in Action

---

## Context Management Audit

### Current CLAUDE.md strengths
The CLAUDE.md is pretty detailed compared to what I had at the start of the project. It has the project structure, the task JSON schema, the CLI command table, testing conventions, and a "Known AI Hallucination Patterns" section I built up over time as I caught the model doing wrong things. The course said your CLAUDE.md should act like onboarding docs for a new developer — I think mine does that reasonably well for the scope of this project.

The testing section is specific enough to actually be useful. It says "never mock the filesystem, use real temp files" and explains why (we got burned by mock/prod divergence in class). That kind of project-specific rule is exactly what the course said belongs in CLAUDE.md.

### Gaps / what I'd change
The course emphasized keeping CLAUDE.md concise and not letting it become a wall of text that the model ignores. Mine is getting a bit long. I'd probably split the hallucination patterns into a separate reference file and just link to it, so the main CLAUDE.md stays focused on conventions and quick rules.

I also don't have anything about the git workflow — the red/green commit pattern I was using never got documented, so if I came back to this project fresh I'd have to dig through the git log to figure out the pattern. Should've added that.

---

## Command Inventory

### Features used in firstbuild (before this tutorial)
- `CLAUDE.md` — project context and conventions
- `/verify` — custom slash command for running the full verification pipeline (imports, lint, tests, coverage)
- Plan Mode — used when I moved from Level 1 to Level 2 (multi-file changes) to plan before writing code
- `@` file mentions — referencing `spec.md` and specific source files when prompting

### Features from the course not yet used (before this tutorial)
- Hooks (adding now)
- `/hallucination-check` custom command (adding now)
- MCP integration
- GitHub PR workflows via `gh` CLI
- `/init` command — I wrote CLAUDE.md manually instead
- Compact conversation mode

---

## Workflow Replay

### Task chosen
Adding the verification pipeline (`verify.py` + `/verify` custom command) — commit `6ea2173`.

### How I approached it then
I basically just described what I wanted in a long prompt: "create a verify.py that runs imports, lint, tests, and coverage in sequence and reports pass/fail for each." It worked on the first try for the most part, but then I had to do a second round to fix lint errors the model introduced (unused imports in test files). I wasn't running tests between edits, so by the time I ran `/verify` at the end there were a few things broken that had to be cleaned up.

I also wrote the `/verify` command after the fact, separately from the main task.

### How I'd approach it now
I'd use a hook from the start so tests run automatically after every file edit so that way the lint errors would have surfaced immediately instead of stacking up. I'd also scope the task better upfront: write the custom command as part of the same task, not as an afterthought. The course's point about "keep instructions durable" made me realize I was treating CLAUDE.md as something I updated after mistakes instead of before starting. I'd write the conventions first, then implement.

---

## New Techniques Applied (Part 3)

### 1. Custom Command — `/hallucination-check`

**What it does:** Scans `git diff` against the known AI hallucination patterns documented in `CLAUDE.md`. Checks for deprecated `typing` imports, bare `None` types, dead utility functions, subprocess test coverage gaps, and spec/CLAUDE.md drift.

**File:** `.claude/commands/hallucination-check.md`

**How to use:** Type `/hallucination-check` in Claude Code after making changes. Claude reads the diff and reports PASS/FAIL for each pattern.

**Did it improve the workflow?**
For /hallucination-check:
Ran clean because the last change was a markdown file deletion — no real patterns to catch. 
Would be more useful after the next feature addition.

---

### 2. Hook — Auto-test on file edit

**What it does:** Runs `pytest -q` automatically after every `Edit` or `Write` tool call. Shows the last 10 lines of output so test failures surface immediately without waiting to ask Claude to run tests.

**File:** `.claude/settings.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "cd /Users/killiand/Desktop/Ecole/ACSQ8/ACS4220/firstbuild && pytest -q 2>&1 | tail -10"
          }
        ]
      }
    ]
  }
}
```

**Did it improve the workflow?**

For Auto-test hook:
Mostly yes, though it runs even on non-Python edits like markdown files which is a bit noisy.
Would probably add a filter for .py files only in a real project. For a small codebase like this the overhead was fine.

