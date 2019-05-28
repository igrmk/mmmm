Google My Maps to MAPS.ME KML converter
=======================================

MAPS.ME just ignores colors and icon images on importing Google My Maps KML.
This simple tool tries to keep them.
They are not the same as in the original KML from Google but they are as close as possible.

Installation
------------

You need Python 3 and lxml installation. On Debian/Ubuntu:

    sudo apt-get install python3-lxml

For MacOS-X choose correct version for your Python interpreter:

    sudo port install py36-lxml

Then just clone this repository:

    git clone https://github.com/igrmk/gmm.git

Usage
-----

    ./gmm.py google-maps.kml > maps-me.kml
