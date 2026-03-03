# Contributing to Maps4FS Locale

<p align="center">
  <a href="#before-you-start">Before You Start</a> •
  <a href="#workflow">Workflow</a> •
  <a href="#pull-request-guidelines">Pull Request Guidelines</a> •
  <a href="#reporting-issues">Reporting Issues</a> •
  <a href="#code-of-conduct">Code of Conduct</a>
</p>

## Before You Start

- Read the [README](README.md) to understand the file structure and naming conventions.
- Open [`languages/en.yml`](languages/en.yml) — this is the **reference file**. Your locale should contain the same keys with translated values.
- You do **not** need Python, Node.js, or any build tools. This repo is plain YAML — a text editor is all you need.

## Workflow

### Option A — Small fix (GitHub web editor)

For fixing a single label or tooltip, you can edit directly on GitHub without cloning anything:

1. Navigate to the file in `languages/` on GitHub.
2. Click the pencil icon (Edit this file).
3. Make your change.
4. Click **Propose changes** — GitHub will automatically fork and open a PR for you.

### Option B — New locale or larger edits

1. **Fork** the repository on GitHub.

2. **Clone** your fork locally:

   ```bash
   git clone https://github.com/<your-username>/maps4fslocale.git
   cd maps4fslocale
   ```

3. **Create a branch** with a descriptive name:

   ```bash
   git checkout -b add-polish-locale
   # or
   git checkout -b fix-german-tooltips
   ```

4. **Make your changes** in `languages/`.

   - New locale: copy `languages/en.yml` to `languages/<code>.yml` (e.g. `pl.yml`) and translate the values.
   - Editing: open the relevant file and make your changes.

5. **Commit and push:**

   ```bash
   git add languages/
   git commit -m "Add Polish locale"
   git push origin add-polish-locale
   ```

6. **Open a Pull Request** on GitHub from your branch to `main`.

## Pull Request Guidelines

- **Title format:** `Add [Language] locale` or `Fix [Language] — <brief description>`
  - Examples: `Add Polish locale`, `Fix German — incorrect tooltip for blur_radius`
- **One language per PR.** Mixing multiple languages in one PR makes review harder.
- **Do not change key names.** Only values (`label:` and `tooltip:`) should differ from `en.yml`.
- **Do not add or remove keys.** The key set must match `en.yml` exactly. Extra keys are silently ignored by the app; missing keys fall back to English.
- If you're adding a new locale, make sure the `meta` block at the top is filled in correctly:

  ```yaml
  meta:
    code: pl           # IETF code — must match the filename
    full: Polish       # English name
    localized: Polski  # Name in its own language
  ```

## Reporting Issues

Found a missing key, a wrong translation in a shipped locale, or a tooltip that's confusing even in English? Please [open an issue](https://github.com/iwatkot/maps4fslocale/issues) with:

- The file and key affected (e.g. `languages/de.yml` → `generation_settings.dem.blur_radius`)
- What it currently says
- What it should say (or what's unclear)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

