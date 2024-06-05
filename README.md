Google My Maps to MAPS.ME KML converter
=======================================

<!-- cut -->
[![Version](https://img.shields.io/pypi/v/mmmm.svg)](https://pypi.org/project/mmmm/)
<!-- end -->

This tool adapts KML files from Google My Maps
for use with [Organic Maps](https://organicmaps.app/) (and MAPS.ME),
striving to maintain color and icon accuracy.
Although Organic Maps supports fewer colors and icons,
the tool does its best to match the original as closely as possible.
Input on new icon mappings is appreciated.

Usage
-----

    mmmm google-maps.kml > maps-me.kml

Installation
------------

    pipx install mmmm

Development
-----------

You can create a virtual environment for testing by executing the commands below:

    micromamba env create --prefix ./.venv --file environment.yml
    micromamba activate ./.venv

Then, from the project root directory, you can run the converter with the following command:

    python -m mmmm google-maps.kml

<!-- cut -->
Thanks to
---------
[![JetBrains](https://raw.githubusercontent.com/igrmk/mmmm/master/svg/jetbrains.svg)](https://www.jetbrains.com/?from=mmmm)
<!-- end -->
