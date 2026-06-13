# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Conventions

Keep every line in this repository — code, Markdown (including this file), and config — to a maximum of 120
characters. The Python lint config (`setup.cfg`) already enforces 120; apply the same limit everywhere by
hard-wrapping prose.

Write each commit message as a single Conventional Commits line — `type(scope): summary`, with no body —
where type is one of `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, or `chore` (scope
optional). This is a solo project: commit directly to `master`; do not create feature branches.

## What this is

`gammon` — short for "Google My Maps to OrgaNIc Maps", as in the domain `gammon.im` — is a single-purpose CLI
that converts Google My Maps KML exports into KML that Organic Maps / MAPS.ME can import, preserving placemark
colors and icons as closely as the smaller Organic Maps style set allows. Published to PyPI as `gammon`; also
runs the backend of https://gammon.im.

## Commands

Set up the dev environment (micromamba/conda):

    micromamba env create --prefix ./.venv --file environment.yml
    micromamba activate ./.venv

Run the converter against a KML file (writes result to stdout):

    python -m gammon google-maps.kml > organic-maps.kml

Useful flags:
- `--verbose` — log Google styles whose icon has no mapping (drives new `icon_map` entries).
- `--only-unsupported-styles` — inverse mode: keep *only* placemarks whose style is recognized-but-unmapped,
  to surface gaps in the mapping tables.

Lint (config in `setup.cfg`, max line length 120):

    flake8 gammon
    pycodestyle gammon

There is **no test suite** in this repo; verify changes by running the converter on a sample KML.

## Architecture

Effectively all logic lives in `gammon/_main.py`. The rest of the package is thin: `__main__.py` calls `_main()`,
`__init__.py` re-exports the public API (`convert`, `ConversionError`, `__version__`), and `__version__.py`
resolves the installed distribution version.

`convert(input_file, output_file, verbose, only_unsupported)` is the entry point used by both the CLI and the
web backend. It parses the KML with `lxml`, finds the `<Document>` element, runs the transform pipeline, then
re-indents and serializes. All KML lookups use the OpenGIS namespace via the `ns` / `x:` prefix; MAPS.ME's
custom `<mwm:icon>` extension uses the `mwm` namespace (`https://maps.me`). Organic Maps reads this same
MAPS.ME-format KML, so the `maps.me` namespace and `placemark-*` style names in the code are deliberate
format references, not project branding — do not rename them.

The default pipeline is `process()`, a fixed sequence of XPath-based mutations on the `<Document>`:
1. `remove_old_styles` — strip Google's `<Style>`/`<StyleMap>`.
2. `remove_lines` — drop `LineString` placemarks (only point placemarks are converted).
3. `remove_empty_folders`.
4. `add_organic_maps_styles` — insert one `<Style>` per unique placemark color at the top of the document.
5. `google_to_organic_maps_icons` — rewrite each placemark's `<styleUrl>` and attach a `<mwm:icon>` element.

### The mapping tables (most common change)

Conversion accuracy is driven by two dicts at the top of `_main.py`:
- `style_map`: Google hex color → MAPS.ME `placemark-<color>` style name.
- `icon_map`: Google 4-digit icon number → MAPS.ME icon name (e.g. `Hotel`, `Food`). The value `'None'` means
  "recognized, but emit no icon".

`google_style_regex` parses Google `styleUrl`s of the form `#icon-1602-C2185B`, where group 1 is the icon
number (looked up in `icon_map`) and group 2 is the hex color (looked up in `style_map`).
`google_to_organic_maps_icon_and_style()` performs both lookups. Adding support for new Google icons/colors almost
always means adding entries to these two dicts — use `--verbose` to find unmapped icons.

## Versioning & release

`describe-version` is a bash script that derives a version string from git tags following the Go modules
pseudo-version rules (tag `vX.Y.Z` on HEAD → `X.Y.Z`; otherwise a dev pseudo-version). `setup.py` shells out
to it at build time, so the package version is never hardcoded. Pushing a `v*` tag triggers
`.github/workflows/publish.yml`, which builds the sdist/wheel and publishes to PyPI.
