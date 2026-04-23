Scan the current working changes for known AI hallucination patterns documented in this project's CLAUDE.md.

Steps:
1. Run `git diff HEAD` to get all uncommitted changes. If nothing, run `git diff HEAD~1` to check the last commit.
2. Read the "Known AI Hallucination Patterns" section of CLAUDE.md.
3. For each documented pattern, check whether the diff contains an instance of it.

Patterns to check:
- **Deprecated type aliases**: imports from `typing` using `Dict`, `List`, `Optional` instead of built-in `dict`, `list`, `str | None`
- **Bare None typing**: function parameters typed as `def f(x: list = None)` instead of `def f(x: list | None = None)`
- **Dead utility functions**: functions that are defined and tested but never called from the CLI layer (check both definition and call sites)
- **subprocess tests hiding coverage**: CLI tests that only use `subprocess.run` with no in-process unit tests for `cmd_*` functions or `build_parser()`
- **Spec vs CLAUDE.md drift**: any behavior described in the diff that contradicts either `spec.md` or `CLAUDE.md`

Report format:
- For each pattern: PASS (not found) or FAIL (found, with file:line and the offending snippet)
- Summary line at the end: how many patterns passed / total
