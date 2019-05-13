import os
import csv
import re
from difflib import SequenceMatcher

import xml.etree.ElementTree as ET
import pandas as pd
import geopy.distance

from geo_mapper import GEO_MAP
from parser import generate_tags, NAME_REGEX

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
GEO_PATH = os.path.join(BASE_PATH, 'data/geonames/palestine.xml')
WEST_BANK_PATH = os.path.join(BASE_PATH, 'data/westbank/westbank.csv')
GAZA_PATH = os.path.join(BASE_PATH, 'data/gaza/gaza.csv')


def find_name_match(osm_name_str, geo_name):
    percentage = '0'
    seq_match = SequenceMatcher(None, osm_name_str, geo_name)
    name_len = max(len(osm_name_str), len(geo_name))
    match = seq_match.find_longest_match(0,
                                         len(osm_name_str),
                                         0,
                                         len(geo_name))
    if match.size != 0:
        percentage = match.size/name_len * 100
        print("Common Substring ::>", osm_name_str[match.a: match.a + match.size])

    percentage = '{0}%'.format(percentage)
    return percentage


if __name__ == '__main__':
    tree = ET.parse(GEO_PATH)
    root = tree.getroot()

    rows = [['']]
    csv.register_dialect('myDialect',
                         quoting=csv.QUOTE_ALL,
                         skipinitialspace=True)

    inverted_geo = dict(map(reversed, GEO_MAP.items()))
    osm_map = dict()

    for child in root.iter('{http://www.geonames.org/ontology#}Feature'):
        geo_id = child.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']
        if inverted_geo.get(geo_id):
            name = child.find('{http://www.geonames.org/ontology#}name').text
            lat = child.find('{http://www.w3.org/2003/01/geo/wgs84_pos#}lat').text
            lon = child.find('{http://www.w3.org/2003/01/geo/wgs84_pos#}long').text
            osm_id = inverted_geo[geo_id]
            osm_map[osm_id] = {
                'geo_name': name,
                'geo_lat': lat,
                'geo_lon': lon,
            }

    for source_path in [GAZA_PATH, WEST_BANK_PATH]:
        with open(source_path, mode='r') as csv_file:
            data = pd.read_csv(csv_file)
            for _, entry in data.iterrows():
                osm_id = str(entry['id'])
                osm_name = ''
                if osm_map.get(osm_id):
                    tags = generate_tags(entry['tags'])
                    for key, value in tags.items():
                        if re.match(NAME_REGEX, key):
                            osm_name = value

                    osm_data = osm_map[osm_id]
                    osm_data['osm_name'] = osm_name
                    osm_data['osm_lat'] = str(entry['lat'])
                    osm_data['osm_lon'] = str(entry['lon'])

    headers = [['geo_name', 'geo_lat',
                'geo_lon', 'osm_name', 'osm_lat',
                'osm_lon', 'name_match', 'distance']]
    for key, comp_obj in osm_map.items():
        print(key)
        coords_1 = (comp_obj['geo_lat'], comp_obj['geo_lon'])
        coords_2 = (comp_obj['osm_lat'], comp_obj['osm_lon'])
        dis = geopy.distance.vincenty(coords_1, coords_2).m
        dis = '{0}m'.format(dis)

        name_match = find_name_match(comp_obj['osm_name'], comp_obj['geo_name'])
        headers.append([comp_obj['geo_name'],
                        comp_obj['geo_lat'],
                        comp_obj['geo_lon'],
                        comp_obj['osm_name'],
                        comp_obj['osm_lat'],
                        comp_obj['osm_lon'],
                        name_match,
                        dis])

    with open('osm_data_match.csv', 'w') as f:
        writer = csv.writer(f, dialect='myDialect')
        for row in headers:
            writer.writerow(row)
