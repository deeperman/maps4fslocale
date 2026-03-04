<div align="center" markdown>

[![Maps4FS](https://img.shields.io/badge/maps4fs-gray?style=for-the-badge)](https://github.com/iwatkot/maps4fs)
[![Maps4FS](https://img.shields.io/badge/atlasfs-green?style=for-the-badge)](https://github.com/iwatkot/atlasfs)
[![Maps4FS](https://img.shields.io/badge/maps4fs-windows-purple?style=for-the-badge)](https://github.com/iwatkot/maps4fswindows)
[![PYDTMDL](https://img.shields.io/badge/pydtmdl-blue?style=for-the-badge)](https://github.com/iwatkot/pydtmdl)
[![PYGDMDL](https://img.shields.io/badge/pygmdl-teal?style=for-the-badge)](https://github.com/iwatkot/pygmdl)  
[![Maps4FS API](https://img.shields.io/badge/maps4fs-api-green?style=for-the-badge)](https://github.com/iwatkot/maps4fsapi)
[![Maps4FS UI](https://img.shields.io/badge/maps4fs-ui-blue?style=for-the-badge)](https://github.com/iwatkot/maps4fsui)
[![Maps4FS Data](https://img.shields.io/badge/maps4fs-data-orange?style=for-the-badge)](https://github.com/iwatkot/maps4fsdata)
[![Maps4FS ChromaDocs](https://img.shields.io/badge/maps4fs-chromadocs-orange?style=for-the-badge)](https://github.com/iwatkot/maps4fschromadocs)  
[![Maps4FS Upgrader](https://img.shields.io/badge/maps4fs-upgrader-yellow?style=for-the-badge)](https://github.com/iwatkot/maps4fsupgrader)
[![Maps4FS Stats](https://img.shields.io/badge/maps4fs-stats-red?style=for-the-badge)](https://github.com/iwatkot/maps4fsstats)
[![Maps4FS Bot](https://img.shields.io/badge/maps4fs-bot-teal?style=for-the-badge)](https://github.com/iwatkot/maps4fsbot)
[![Maps4FS Locale](https://img.shields.io/badge/maps4fs-locale-purple?style=for-the-badge)](https://github.com/iwatkot/maps4fslocale)

</div>

<div align="center" markdown>
<img src="https://github.com/iwatkot/maps4fslocale/releases/download/0.0.1/locale-1280-640.png">

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#available-locales">Available Locales</a> •
  <a href="#file-structure">File Structure</a> •
  <a href="#adding-a-new-locale">Adding a New Locale</a> •
  <a href="#editing-an-existing-locale">Editing an Existing Locale</a>
</p>

[![Join Discord](https://img.shields.io/badge/join-discord-blue)](https://discord.gg/wemVfUUFRA)
[![GitHub issues](https://img.shields.io/github/issues/iwatkot/maps4fslocale)](https://github.com/iwatkot/maps4fslocale/issues)
[![GitHub Repo stars](https://img.shields.io/github/stars/iwatkot/maps4fslocale)](https://github.com/iwatkot/maps4fslocale/stargazers)
[![Check Status](https://github.com/iwatkot/maps4fslocale/actions/workflows/validate-locales-push.yml/badge.svg)](https://github.com/iwatkot/maps4fslocale/actions)

</div>

## Overview

This is the **community localization repository** for [Maps4FS](https://github.com/iwatkot/maps4fs) — a map generator for Farming Simulator.

All UI labels and tooltips for both the **Docker (web)** version and the **Windows app** live here as simple YAML files. Anyone can contribute — whether that means adding a brand new language, improving an existing translation, or even correcting a tooltip in English.

> **English is not sacred.** If you spot an unclear or incorrect tooltip in `en.yml`, feel free to open a PR to improve it. The English file is the source of truth only because it's the most complete — not because it's immune to changes.

## Available Locales

| File | Language | Native name |
|------|----------|-------------|
| `languages/en.yml` | English | English |
| `languages/de.yml` | German | Deutsch |
| `languages/fr.yml` | French | Français |
| `languages/it.yml` | Italian | Italiano |
| `languages/sr.yml` | Serbian | Srpski |

## File Structure

Each locale lives in `languages/<code>.yml`. The structure mirrors the Maps4FS UI layout:

```yaml
meta:
  code: en          # IETF language code used by the app
  full: English     # English name of the language
  localized: English  # Name in its own language (e.g. Deutsch, Français)

main_settings:
  label: Main Settings
  tooltip: Core parameters for map generation
  fields:
    game:
      label: Game
      tooltip: "Target FS version."
    # ... more fields

generation_settings:
  # Nested sections: dem, background, grle, i3d, texture, satellite, building
  dem:
    label: DEM
    fields:
      blur_radius:
        label: Blur Radius
        tooltip: "Smooths terrain by blurring elevation data."

windows:
  # Labels and tooltips specific to the Windows desktop app

docker:
  # Labels and tooltips specific to the Docker/web version
```

Every entry has at minimum a `label`. A `tooltip` is optional but strongly encouraged — it's what appears on hover in the UI and is the main way users understand what a setting does.

> **Reference file:** Always use [`languages/en.yml`](languages/en.yml) as your reference. It is the most up-to-date file and contains every key currently used by the app.

## Adding a New Locale

1. **Fork** this repository and clone it locally.

2. **Copy** `languages/en.yml` to a new file named after the [IETF language code](https://en.wikipedia.org/wiki/IETF_language_tag) of your language:

   ```
   languages/pl.yml   # Polish
   languages/cs.yml   # Czech
   languages/pt.yml   # Portuguese
   ```

   Use simple codes (`pl`, `de`, `fr`) unless you need to distinguish regional variants (`pt-BR` vs `pt-PT`). When in doubt, use the simple code.

3. **Update the `meta` block** at the top of the file:

   ```yaml
   meta:
     code: pl
     full: Polish
     localized: Polski
   ```

4. **Translate every `label` and `tooltip`** value. Keep all YAML keys in English — only translate the values.

   ```yaml
   # ✅ Correct
   blur_radius:
     label: Promień rozmycia
     tooltip: "Wygładza teren poprzez rozmycie danych wysokościowych."

   # ❌ Wrong — never translate the key
   promień_rozmycia:
     label: Promień rozmycia
   ```

5. **Keep technical terms as-is.** Things like `DTM`, `DEM`, `OSM`, `i3d`, `Giants Editor`, `smallDenseMix`, and in-game asset names should not be translated — users encounter them in English in the app and game UI.

6. **Open a Pull Request** with the title `Add [Language] locale` (e.g. `Add Polish locale`).

## Editing an Existing Locale

Editing is just as welcome as adding new ones. Common reasons to edit:

- **Improve a tooltip** — make it clearer, shorter, or more accurate
- **Fix a translation** — correct grammar, wording, or terminology
- **Add missing keys** — if a key exists in `en.yml` but is missing from another locale
- **Fix the English** — if a label or tooltip in `en.yml` itself is wrong or confusing

The process is the same: fork → edit → pull request.

For small fixes (a single label or tooltip), editing directly on GitHub via the web editor is perfectly fine.

## Guidelines

- **Keep tooltips concise.** One or two sentences is ideal. Only go longer if the setting has a genuine gotcha (e.g. a warning about crashing Giants Editor).
- **Preserve YAML formatting.** Use quotes around values that contain `:`, `#`, or special characters.
- **Do not add or remove keys.** The key structure must stay identical to `en.yml`. The app uses keys to look up strings — extra or missing keys will be silently ignored or cause fallback to English.
- **One language per PR.** Keeps review clean and focused.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution workflow.