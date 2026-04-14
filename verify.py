#!/usr/bin/env python3
"""Verification pipeline for firstbuild.

Runs four checks in order and exits non-zero if any fail:
  1. Import check  — src package imports without errors
  2. Lint check    — ruff finds no errors
  3. Test check    — pytest passes
  4. Coverage check — total coverage meets the threshold

Usage:
    python3 verify.py           # uses default threshold (80%)
    python3 verify.py --min-cov 70
"""

import argparse
import importlib
import subprocess
import sys


PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def check_imports() -> bool:
    """Try importing every src module; report any that fail."""
    modules = ["src", "src.tasks", "src.storage", "src.cli"]
    ok = True
    for mod in modules:
        try:
            importlib.import_module(mod)
        except Exception as e:
            print(f"  import {mod}: {e}")
            ok = False
    return ok


def check_lint() -> bool:
    result = run([sys.executable, "-m", "ruff", "check", "src/", "tests/"])
    if result.returncode != 0:
        print(result.stdout.strip())
    return result.returncode == 0


def check_tests() -> bool:
    result = run([sys.executable, "-m", "pytest", "tests/", "-q", "--tb=short"])
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    return result.returncode == 0


def check_coverage(min_cov: int) -> bool:
    result = run([
        sys.executable, "-m", "pytest", "tests/",
        f"--cov=src",
        "--cov-report=term-missing",
        f"--cov-fail-under={min_cov}",
        "-q",
    ])
    # Print the coverage table portion only
    output = result.stdout
    in_table = False
    for line in output.splitlines():
        if line.startswith("Name") or in_table:
            in_table = True
            print(line)
    return result.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run verification pipeline")
    parser.add_argument(
        "--min-cov", type=int, default=80,
        help="Minimum total coverage percentage (default: 80)",
    )
    args = parser.parse_args()

    checks = [
        ("1. Import check ", check_imports),
        ("2. Lint check   ", check_lint),
        ("3. Test check   ", check_tests),
        ("4. Coverage     ", lambda: check_coverage(args.min_cov)),
    ]

    results = []
    for label, fn in checks:
        passed = fn()
        status = PASS if passed else FAIL
        print(f"\n{label}: {status}")
        results.append(passed)

    print()
    if all(results):
        print("All checks passed.")
        sys.exit(0)
    else:
        failed = [checks[i][0].strip() for i, ok in enumerate(results) if not ok]
        print(f"Failed: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
