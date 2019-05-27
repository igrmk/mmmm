#!/usr/bin/python3

import lxml.etree as T
import sys
import lxml.builder
import re
import collections as C

E = lxml.builder.ElementMaker()

ns = {'x': 'http://www.opengis.net/kml/2.2'}
google_style_regex = re.compile(r'^#icon-\d{4}-([0-9A-F]{6})')

style_map = {
    'C2185B': 'placemark-red',
    'A52714': 'placemark-red',
    '0288D1': 'placemark-blue',
    '673AB7': 'placemark-blue',
    '006064': 'placemark-blue',
    '01579B': 'placemark-blue',
    '1A237E': 'placemark-blue',
    '0097A7': 'placemark-blue',
    '3949AB': 'placemark-blue',
    '880E4F': 'placemark-purple',
    '9C27B0': 'placemark-purple',
    'FBC02D': 'placemark-yellow',
    'FFD600': 'placemark-yellow',
    'FFEA00': 'placemark-yellow',
    'FF5252': 'placemark-pink',
    '817717': 'placemark-brown',
    '4E342E': 'placemark-brown',
    'AFB42B': 'placemark-brown',
    '795548': 'placemark-brown',
    '424242': 'placemark-brown',
    '000000': 'placemark-brown',
    '757575': 'placemark-brown',
    '097138': 'placemark-green',
    '558B2F': 'placemark-green',
    '7CB342': 'placemark-green',
    '0F9D58': 'placemark-green',
    'E65100': 'placemark-orange',
    'F57C00': 'placemark-orange',
    'F9A825': 'placemark-orange',
    'BDBDBD': 'placemark-orange',
}


def unique_styles():
    return C.OrderedDict(zip(style_map.values(), [None] * len(style_map)))


def indent(elem, level=0):
    i = '\n' + level * '  '
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def maps_me_style(style):
    m = google_style_regex.match(style)
    if m and m.group(1) in style_map:
        return '#' + style_map[m.group(1)]
    return style


def process(doc):
    for i in doc.xpath('//x:Style | //x:StyleMap', namespaces=ns):
        i.getparent().remove(i)
    for i in doc.xpath('//x:Folder//x:Placemark//x:LineString', namespaces=ns):
        i = i.getparent()
        i.getparent().remove(i)
    for i in doc.xpath('//x:Folder[not(x:Placemark)]', namespaces=ns):
        i.getparent().remove(i)
    for i in doc.xpath('//x:Folder//x:Placemark//x:styleUrl', namespaces=ns):
        i.text = maps_me_style(i.text)
    for i, name in enumerate(unique_styles()):
        ref = f'http://maps.me/placemarks/{name}.png'
        style = E.Style(E.IconStyle(E.Icon(E.href(ref))), id=name)
        doc.insert(i, style)


def main(filename):
    with open(filename, 'r') as f:
        root = T.parse(f)
        doc = root.find('x:Document', ns)
        if doc is None:
            return
        process(doc)
        indent(root.getroot())
        string = T.tostring(root,
                            pretty_print=True,
                            encoding='UTF-8',
                            xml_declaration=True)
        sys.stdout.buffer.write(string)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('usage: gmm <kml>')
        sys.exit(1)
    main(sys.argv[1])
