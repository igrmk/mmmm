Gammon — Google My Maps to Organic Maps KML converter
=====================================================

<!-- cut -->
[![Version](https://img.shields.io/pypi/v/gammon-im.svg)](https://pypi.org/project/gammon-im/)
<!-- end -->

This tool adapts KML and KMZ files from Google My Maps
for use with [Organic Maps](https://organicmaps.app/) (and MAPS.ME),
striving to maintain color and icon accuracy.
Although Organic Maps supports fewer colors and icons,
the tool does its best to match the original as closely as possible.
Input on new icon mappings is appreciated.

Formerly published as `mmmm`; now installed as `gammon-im` and run as `gammon` (online at
[gammon.im](https://gammon.im)).
If you installed the old package, migrate with `pipx uninstall mmmm && pipx install gammon-im`.

Usage
-----

    gammon google-maps.kml > organic-maps.kml

Or go to [Gammon](https://gammon.im) and convert your KML online.

Installation
------------

    pipx install gammon-im

Development
-----------

Install [uv](https://docs.astral.sh/uv/), then sync the environment and run the converter or the linter:

    uv sync
    uv run gammon google-maps.kml > organic-maps.kml
    uv run ruff check

<!-- cut -->
Thanks to
---------
[![JetBrains](https://raw.githubusercontent.com/igrmk/gammon/master/svg/jetbrains.svg)](https://www.jetbrains.com/?from=gammon)
<!-- end -->
