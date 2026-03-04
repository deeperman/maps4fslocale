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
    status is 'reference_ok', 'reference_error', 'ok', 'syntax_error', or 'key_mismatch'.
    The first entry is always the reference file (en.yml) itself.
    """
    # Load reference — always the first result entry
    ref_data, ref_err = load_yaml(REFERENCE_FILE)
    if ref_err:
        return [(REFERENCE_FILE, "reference_error", ref_err)]

    ref_paths = set(extract_key_paths(ref_data))
    results = [(REFERENCE_FILE, "reference_ok", None)]

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
    """Print a human-readable report and write a GitHub Job Summary. Returns True if any issues were found."""
    reference_entry = next(
        (r for r in results if r[1] in ("reference_ok", "reference_error")), None
    )
    ref_broken = reference_entry and reference_entry[1] == "reference_error"

    ok = []
    issues = []

    for path, status, details in results:
        if status in ("ok", "reference_ok"):
            ok.append((path, status))
        else:
            issues.append((path, status, details))

    had_issues = len(issues) > 0

    # ── Console output ───────────────────────────────────────────────────────
    print("=" * 60)
    print("LOCALE VALIDATION REPORT")
    print("=" * 60)

    if ok:
        print(f"\n✅  FILES OK ({len(ok)})")
        for path, status in ok:
            note = " (reference)" if status == "reference_ok" else ""
            print(f"    {path.name}{note}")

    if issues:
        print(f"\n❌  FILES WITH ISSUES ({len(issues)})")
        for path, status, details in issues:
            print(f"\n  ── {path.name} ──")
            if status == "reference_error":
                print(
                    f"    [BROKEN REFERENCE] en.yml has invalid syntax — cannot validate other files."
                )
                print(f"    {details}")
            elif status == "syntax_error":
                print(f"    [INVALID YAML] {details}")
            elif status == "key_mismatch":
                if "missing" in details:
                    print(
                        f"    [MISSING KEYS] ({len(details['missing'])} keys missing from en.yml reference):"
                    )
                    for key in details["missing"]:
                        print(f"        - {key}")
                if "extra" in details:
                    print(
                        f"    [EXTRA KEYS] ({len(details['extra'])} keys not present in en.yml):"
                    )
                    for key in details["extra"]:
                        print(f"        + {key}")
    else:
        print("\n✅  All checked files are valid and match the reference.")

    print("\n" + "=" * 60)

    # ── GitHub Job Summary (Markdown) ────────────────────────────────────────
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        lines = []
        overall = (
            "❌ Validation failed" if had_issues else "✅ All locale files are valid"
        )
        lines.append(f"## Locale Validation Report\n")
        lines.append(f"### {overall}\n")

        if ok:
            lines.append(
                f"<details open>\n<summary>✅ Files OK ({len(ok)})</summary>\n"
            )
            lines.append("\n| File | Role |")
            lines.append("| --- | --- |")
            for path, status in ok:
                role = "**reference**" if status == "reference_ok" else "locale"
                lines.append(f"| `{path.name}` | {role} |")
            lines.append("\n</details>\n")

        if issues:
            lines.append(
                f"<details open>\n<summary>❌ Files with issues ({len(issues)})</summary>\n"
            )
            for path, status, details in issues:
                lines.append(f"\n#### `{path.name}`\n")
                if status == "reference_error":
                    lines.append(
                        "> 🔴 **Reference file `en.yml` has invalid YAML syntax — other files cannot be validated.**\n"
                    )
                    lines.append(f"```\n{details}\n```\n")
                elif status == "syntax_error":
                    lines.append(f"> ⚠️ **Invalid YAML syntax**\n")
                    lines.append(f"```\n{details}\n```\n")
                elif status == "key_mismatch":
                    if "missing" in details:
                        lines.append(
                            f"**{len(details['missing'])} missing key(s)** (present in `en.yml` but absent here):\n"
                        )
                        lines.append("| Missing key |")
                        lines.append("| --- |")
                        for key in details["missing"]:
                            lines.append(f"| `{key}` |")
                        lines.append("")
                    if "extra" in details:
                        lines.append(
                            f"**{len(details['extra'])} extra key(s)** (not present in `en.yml`):\n"
                        )
                        lines.append("| Extra key |")
                        lines.append("| --- |")
                        for key in details["extra"]:
                            lines.append(f"| `{key}` |")
                        lines.append("")
            lines.append("</details>\n")

        with open(summary_path, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    return had_issues


def main():
    # Collect files to check
    if len(sys.argv) > 1:
        files_to_check = [Path(f) for f in sys.argv[1:]]
        # Filter out the reference file itself if accidentally passed
        files_to_check = [
            f for f in files_to_check if f.resolve() != REFERENCE_FILE.resolve()
        ]
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

    # If en.yml itself is broken there's nothing more we can do — report and stop
    if results and results[0][1] == "reference_error":
        print_report(results)
        sys.exit(1)

    had_issues = print_report(results)

    sys.exit(1 if had_issues else 0)


if __name__ == "__main__":
    main()
