#!/usr/bin/env python3
"""
Validate locale YAML files against en.yml reference.

Usage:
    python validate_locales.py [file1.yml file2.yml ...]

If no files are given, all .yml files in languages/ are validated.
The script always skips en.yml itself (it IS the reference).
Exit code 0 = all OK, exit code 1 = issues found.
"""

import sys
import os
import glob
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Run: pip install pyyaml")
    sys.exit(2)

LANGUAGES_DIR = Path(__file__).parent.parent.parent / "languages"
REFERENCE_FILE = LANGUAGES_DIR / "en.yml"


def extract_key_paths(obj, prefix=""):
    """Recursively yield all dotted key paths in a nested dict."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            full_key = f"{prefix}.{key}" if prefix else key
            yield full_key
            yield from extract_key_paths(value, full_key)


def load_yaml(path):
    """Return (data, error_message). data is None on failure."""
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            return None, "File parsed but root is not a YAML mapping."
        return data, None
    except yaml.YAMLError as exc:
        return None, f"YAML syntax error: {exc}"
    except OSError as exc:
        return None, f"Cannot read file: {exc}"


def compare_keys(reference_paths, candidate_paths):
    """Return (missing, extra) key sets."""
    missing = reference_paths - candidate_paths
    extra = candidate_paths - reference_paths
    return missing, extra


def validate_files(files_to_check):
    """
    Validate each file.  Returns a list of (path, status, details) tuples.
    status is 'ok', 'syntax_error', or 'key_mismatch'.
    """
    # Load reference
    ref_data, ref_err = load_yaml(REFERENCE_FILE)
    if ref_err:
        print(f"FATAL: Cannot load reference file {REFERENCE_FILE}: {ref_err}")
        sys.exit(2)

    ref_paths = set(extract_key_paths(ref_data))
    results = []

    for path in files_to_check:
        path = Path(path)
        data, err = load_yaml(path)
        if err:
            results.append((path, "syntax_error", err))
            continue

        candidate_paths = set(extract_key_paths(data))
        missing, extra = compare_keys(ref_paths, candidate_paths)

        if missing or extra:
            details = {}
            if missing:
                details["missing"] = sorted(missing)
            if extra:
                details["extra"] = sorted(extra)
            results.append((path, "key_mismatch", details))
        else:
            results.append((path, "ok", None))

    return results


def print_report(results):
    """Print a human-readable report. Returns True if any issues were found."""
    ok = []
    issues = []

    for path, status, details in results:
        if status == "ok":
            ok.append(path)
        else:
            issues.append((path, status, details))

    # ── OK files ────────────────────────────────────────────────────────────
    print("=" * 60)
    print("LOCALE VALIDATION REPORT")
    print("=" * 60)

    if ok:
        print(f"\n✅  FILES OK ({len(ok)})")
        for path in ok:
            print(f"    {path.name}")

    # ── Issue files ──────────────────────────────────────────────────────────
    if issues:
        print(f"\n❌  FILES WITH ISSUES ({len(issues)})")
        for path, status, details in issues:
            print(f"\n  ── {path.name} ──")
            if status == "syntax_error":
                print(f"    [INVALID YAML] {details}")
            elif status == "key_mismatch":
                if "missing" in details:
                    print(f"    [MISSING KEYS] ({len(details['missing'])} keys missing from en.yml reference):")
                    for key in details["missing"]:
                        print(f"        - {key}")
                if "extra" in details:
                    print(f"    [EXTRA KEYS] ({len(details['extra'])} keys not present in en.yml):")
                    for key in details["extra"]:
                        print(f"        + {key}")
    else:
        print("\n✅  All checked files are valid and match the reference.")

    print("\n" + "=" * 60)
    return len(issues) > 0


def main():
    # Collect files to check
    if len(sys.argv) > 1:
        files_to_check = [Path(f) for f in sys.argv[1:]]
        # Filter out the reference file itself if accidentally passed
        files_to_check = [f for f in files_to_check if f.resolve() != REFERENCE_FILE.resolve()]
        if not files_to_check:
            print("No files to validate (only en.yml was passed — skipping).")
            sys.exit(0)
    else:
        # Default: all yml files in languages/ except en.yml
        all_yml = sorted(LANGUAGES_DIR.glob("*.yml"))
        files_to_check = [f for f in all_yml if f.resolve() != REFERENCE_FILE.resolve()]
        if not files_to_check:
            print("No locale files found to validate.")
            sys.exit(0)

    print(f"Reference: {REFERENCE_FILE}")
    print(f"Checking:  {', '.join(f.name for f in files_to_check)}\n")

    results = validate_files(files_to_check)
    had_issues = print_report(results)

    sys.exit(1 if had_issues else 0)


if __name__ == "__main__":
    main()
