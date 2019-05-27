#!/usr/bin/python3

import lxml.etree as T
import sys

namespaces = {'x': 'http://www.opengis.net/kml/2.2'}
filename = sys.argv[1]

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
    '#icon-1502-F9A825': '#placemark-orange',
    '#icon-1511-817717': '#placemark-brown',
    '#icon-1517-F57C00': '#placemark-orange',
    '#icon-1517-FBC02D': '#placemark-yellow',
    '#icon-1532-FF5252': '#placemark-pink',
    '#icon-1534-F9A825': '#placemark-orange',
    '#icon-1534-FBC02D': '#placemark-yellow',
    '#icon-1577-F57C00': '#placemark-orange',
    '#icon-1577-F9A825': '#placemark-orange',
    '#icon-1577-FBC02D': '#placemark-yellow',
    '#icon-1577-FFD600': '#placemark-yellow',
    '#icon-1603-880E4F': '#placemark-purple',
    '#icon-1603-9C27B0': '#placemark-purple',
    '#icon-1603-C2185B': '#placemark-red',
    '#icon-1603-FF5252': '#placemark-pink',
    '#icon-1717-FF5252': '#placemark-pink',
    '#icon-1741-FF5252': '#placemark-pink',
    '#icon-1801-817717': '#placemark-brown',
    '#icon-1879-F57C00': '#placemark-orange',
    '#icon-1879-F9A825': '#placemark-orange',
    '#icon-1879-FBC02D': '#placemark-yelow',
    '#icon-1899-0288D1': '#placemark-blue',
    '#icon-1899-097138': '#placemark-green',
    '#icon-1899-558B2F': '#placemark-green',
    '#icon-1899-817717': '#placemark-brown',
    '#icon-1899-880E4F': '#placemark-red',
    '#icon-1899-7CB342': '#placemark-green',
    '#icon-1532-FF5252': '#placemark-pink',
    '#icon-1899-673AB7': '#placemark-blue',
    '#icon-1801-097138': '#placemark-green',
    '#icon-1504-E65100': '#placemark-red',
    '#icon-1602-FF5252': '#placemark-pink',
    '#icon-1502-F9A825-nodesc': '#placemark-orange',
    '#icon-1511-817717-nodesc': '#placemark-brown',
    '#icon-1517-F57C00-nodesc': '#placemark-orange',
    '#icon-1517-FBC02D-nodesc': '#placemark-yellow',
    '#icon-1532-FF5252-nodesc': '#placemark-pink',
    '#icon-1534-F9A825-nodesc': '#placemark-orange',
    '#icon-1534-FBC02D-nodesc': '#placemark-yellow',
    '#icon-1577-F57C00-nodesc': '#placemark-orange',
    '#icon-1577-F9A825-nodesc': '#placemark-orange',
    '#icon-1577-FBC02D-nodesc': '#placemark-yellow',
    '#icon-1577-FFD600-nodesc': '#placemark-yellow',
    '#icon-1603-880E4F-nodesc': '#placemark-purple',
    '#icon-1603-9C27B0-nodesc': '#placemark-purple',
    '#icon-1603-C2185B-nodesc': '#placemark-red',
    '#icon-1603-FF5252-nodesc': '#placemark-pink',
    '#icon-1717-FF5252-nodesc': '#placemark-pink',
    '#icon-1741-FF5252-nodesc': '#placemark-pink',
    '#icon-1801-817717-nodesc': '#placemark-brown',
    '#icon-1879-F57C00-nodesc': '#placemark-orange',
    '#icon-1879-F9A825-nodesc': '#placemark-orange',
    '#icon-1879-FBC02D-nodesc': '#placemark-yelow',
    '#icon-1899-0288D1-nodesc': '#placemark-blue',
    '#icon-1899-097138-nodesc': '#placemark-green',
    '#icon-1899-558B2F-nodesc': '#placemark-green',
    '#icon-1899-817717-nodesc': '#placemark-brown',
    '#icon-1899-880E4F-nodesc': '#placemark-red',
    '#icon-1899-7CB342-nodesc': '#placemark-green',
    '#icon-1532-FF5252-nodesc': '#placemark-pink',
    '#icon-1899-673AB7-nodesc': '#placemark-blue',
    '#icon-1801-097138-nodesc': '#placemark-green',
    '#icon-1504-E65100-nodesc': '#placemark-red',
    '#icon-1602-FF5252-nodesc': '#placemark-pink',
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


def mapsMeStyle(style):
    if style in styleMap:
        return styleMap[style]
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
            style = T.Element('Style', id=name)
            iconStyle = T.SubElement(style, 'IconStyle')
            icon = T.SubElement(iconStyle, 'Icon')
            href = T.SubElement(icon, 'href')
            href.text = ref
            doc.insert(pos, style)
            pos += 1
        indent(root.getroot())
        string = T.tostring(root,
                            pretty_print=True,
                            encoding='UTF-8',
                            xml_declaration=True)
        sys.stdout.buffer.write(string)


process(filename)
