Run the project verification pipeline and report results.

Execute `python3 verify.py` from the project root. The script runs four checks in order:
1. Import check — all src modules import without errors
2. Lint check — ruff finds no errors in src/ and tests/
3. Test check — pytest passes with 0 failures
4. Coverage check — total coverage meets the 80% threshold

After running, report:
- Which checks passed and which failed
- For any failure, quote the relevant output lines and explain what needs fixing
- If all checks pass, confirm the pipeline is clean
