#!/usr/bin/python3

import lxml.etree as T
import sys
import lxml.builder
import re
import collections as C

E = lxml.builder.ElementMaker()

ns = {'x': 'http://www.opengis.net/kml/2.2'}
mwm = 'https://maps.me'
mwmns = {'mwm': mwm}
google_style_regex = re.compile(r'^#icon-(\d{4})-([0-9A-F]{6})')

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

icon_map = {
    '1602': 'Hotel',
    '1507': 'Animals',
    '1743': 'Animals',
    '1667': 'Buddhism',
    '1668': 'Buddhism',
    '1669': 'Buddhism',
    '1546': 'Building',
    '1548': 'Building',
    '1717': 'Building',
    '1741': 'Building',
    '1603': 'Building',
    '1670': 'Christianity',
    '1540': 'Entertainment',
    '1555': 'Exchange',
    '1534': 'Food',
    '1577': 'Food',
    '1581': 'Gas',
    '1675': 'Judaism',
    '1624': 'Medicine',
    '1634': 'Mountain',
    '1636': 'Museum',
    '1673': 'Islam',
    '1720': 'Park',
    '1644': 'Parking',
    '1684': 'Shop',
    '1685': 'Shop',
    '1598': 'Sights',
    '1701': 'Swim',
    '1703': 'Water',
}


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


def maps_me_icon_style(google_style):
    icon, style = None, google_style
    m = google_style_regex.match(google_style)
    if m and m.group(1) in icon_map:
        icon = icon_map[m.group(1)]
    if m and m.group(2) in style_map:
        style = '#' + style_map[m.group(2)]
    return icon, style


def process(doc):
    for i in doc.xpath('//x:Style | //x:StyleMap', namespaces=ns):
        i.getparent().remove(i)
    for i in doc.xpath('//x:Folder//x:Placemark[x:LineString]', namespaces=ns):
        i.getparent().remove(i)
    for i in doc.xpath('//x:Folder[not(x:Placemark)]', namespaces=ns):
        i.getparent().remove(i)
    for i in doc.xpath('//x:Folder//x:Placemark//x:styleUrl', namespaces=ns):
        icon, i.text = maps_me_icon_style(i.text)
        if icon is not None:
            extended = T.SubElement(i.getparent(), 'ExtendedData', nsmap=mwmns)
            icon_tag = T.SubElement(extended, f'{{{mwm}}}icon')
            icon_tag.text = icon
    unique_styles = C.OrderedDict((v, None) for v in style_map.values())
    for i, name in enumerate(unique_styles):
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
