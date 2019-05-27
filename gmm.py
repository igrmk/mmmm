#!/usr/bin/python3

import lxml.etree as T
import sys
import lxml.builder
import re

E = lxml.builder.ElementMaker()

namespaces = {'x': 'http://www.opengis.net/kml/2.2'}

mapsMeStyles = {
    'placemark-red':    'http://maps.me/placemarks/placemark-red.png',
    'placemark-blue':   'http://maps.me/placemarks/placemark-blue.png',
    'placemark-purple': 'http://maps.me/placemarks/placemark-purple.png',
    'placemark-yellow': 'http://maps.me/placemarks/placemark-yellow.png',
    'placemark-pink':   'http://maps.me/placemarks/placemark-pink.png',
    'placemark-brown':  'http://maps.me/placemarks/placemark-brown.png',
    'placemark-green':  'http://maps.me/placemarks/placemark-green.png',
    'placemark-orange': 'http://maps.me/placemarks/placemark-orange.png'
}

styleMap = {
    '0288D1': '#placemark-blue',
    '097138': '#placemark-green',
    '558B2F': '#placemark-green',
    '673AB7': '#placemark-blue',
    '7CB342': '#placemark-green',
    '817717': '#placemark-brown',
    '880E4F': '#placemark-purple',
    '9C27B0': '#placemark-purple',
    'C2185B': '#placemark-red',
    'E65100': '#placemark-orange',
    'F57C00': '#placemark-orange',
    'F9A825': '#placemark-orange',
    'FBC02D': '#placemark-yellow',
    'FF5252': '#placemark-pink',
    'FFD600': '#placemark-yellow',
}


def indent(elem, level=0):
    i = '\n' + level * '  '
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


rex = re.compile('^#icon-\d{4}-([0-9A-F]{6})')
def mapsMeStyle(style):
    m = rex.match(style)
    if m and m.group(1) in styleMap:
        return styleMap[m.group(1)]
    return style


def process(filename):
    with open(filename, 'r') as f:
        root = T.parse(f)
        doc = root.find('x:Document', namespaces=namespaces)
        if doc is None:
            return
        for elem in doc.xpath('//x:Style | //x:StyleMap', namespaces=namespaces):
            elem.getparent().remove(elem)
        for elem in doc.xpath('//x:Folder//x:Placemark//x:styleUrl', namespaces=namespaces):
            elem.text = mapsMeStyle(elem.text)
        pos = 0
        for name, ref in mapsMeStyles.items():
            style = E.Style(E.IconStyle(E.Icon(E.href(ref))), id=name)
            doc.insert(pos, style)
            pos += 1
        indent(root.getroot())
        string = T.tostring(root,
                            pretty_print=True,
                            encoding='UTF-8',
                            xml_declaration=True)
        sys.stdout.buffer.write(string)

if __name__== "__main__":
    if len(sys.argv) != 2:
        print('usage: gmm <kml>')
        sys.exit(1)
    process(sys.argv[1])
