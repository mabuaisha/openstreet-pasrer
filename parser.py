import os

import pandas as pd
# Third Party Imports
from xml.etree import ElementTree as et


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, 'data.csv')

RDF_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS_NAMESPACE = "http://www.w3.org/2000/01/rdf-schema#"
OSM_NAMESPACE = "http://www.osm-namespace.com/"
XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema-datatypes"
OSM_URL = "https://www.openstreetmap.org/directions#map=19/"

TAGS_AMINTY_MAPPER = {
    'pharmac': 'pharmacy',
    'caf': 'cafe',
    'ban': 'bank',
    'restauran': 'restaurant',
    'schoo': 'school',
    'fue': 'fuel',
    'clini': 'clinic',
    'polic': 'police',
}

IGNORE_KEYS = (
    'name:ar',
    'name:en',
    'name:pl',
    'name:sv',
    'name:de',
    'name:ru',
    'name:fr',
    'name:es',
    'name:it',
    'name:ro',
    'name:nl',
    'name:ja',
    'name:fi',
    'name:hu',
    'name:grc',
    'name:el',
    'name:la',
    'name:zh',
    'name:bg',
    'name:gr',
    'alt_name:de',
    'alt_name:en',
    'alt_name2:ar',
    'alt_name2',
    'fixme',
    'name_1',
    'name:cs',
    'alt_name:cs',
    'short_name:ar',
    'notes:ar',
    'ele',
    'yes',
    'ref',
    'children\'s home',
    'diet:vegetarian',
    'diet:vegan',
    'addr:street:en',
    'addr:street:ar',
    'social_facility:for',
    'community_centre:for',
    'wikipedia_1',
    'ice_cream;cafe',
    'cafe;restaurant',
    'cafe ; billiard',
)


def generate_tags(tags):
    node_tags = dict()
    tags = tags[1: len(tags) - 2].split(',')
    for element in tags:
        values = element.split('=')
        if len(values) > 1:
            node_tags[values[0].lstrip()] = values[1].lstrip()
    return node_tags


def generate_key_using_delimiter(key, delimiter):
    strings = list(map(lambda item: item.strip(''), key.split(delimiter)))
    if len(strings) > 1:
        cap_keys = map(lambda item: item.capitalize(), strings[1:])
        key = '{0}{1}'.format(strings[0], ''.join(cap_keys))
    return key


def generate_rdf_node_resource(node_id, tags, lat, lon):
    resource_uri = '{0}{1}/{2}'.format(OSM_URL, lat, lon)
    resource = et.Element(
        '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description')
    resource.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about',
                 resource_uri)

    # Create element ID
    element_id = et.Element('{http://www.osm-namespace.com/}nodeId')
    element_id.set('rdf:datatype', 'string')
    element_id.text = node_id
    resource.append(element_id)

    for key, value in tags.items():
        if value:
            if key in IGNORE_KEYS:
                continue
            elif key == 'amenity':
                key = 'category'
                value = TAGS_AMINTY_MAPPER.get(tags['amenity'], tags['amenity'])

            # lang_attr = None
            # if 'name:' in key:
            #     key, lang_attr = key.split(':')

            for delimiter in ['_', ':']:
                key = generate_key_using_delimiter(key, delimiter)

            key = '{http://www.osm-namespace.com/}' + key
            element_tag = et.Element(key)
            element_tag.set('rdf:datatype', 'string')
            # if lang_attr:
            #     element_tag.set('xml:lang', lang_attr)
            element_tag.text = value
            resource.append(element_tag)

    return resource


def generate_root_rdf():
    et.register_namespace('osm', OSM_NAMESPACE)
    et.register_namespace('rdf', RDF_NAMESPACE)
    rdf = et.Element('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF')
    rdf.set('xmlns:xsd', XSD_NAMESPACE)
    rdf.set('xmlns:rdfs', RDFS_NAMESPACE)
    return rdf


def generate_rdf_tree(root):
    tree = et.ElementTree(root)
    tree.write('map.xml',
               encoding='utf-8',
               xml_declaration=True,
               method='xml')


def generate_rdf_file():
    root = generate_root_rdf()
    with open(DATA_PATH, mode='r') as csv_file:
        data = pd.read_csv(csv_file)
        for _, entry in data.iterrows():
            tags = generate_tags(entry['tags'])
            resource_node = generate_rdf_node_resource(str(entry['id']),
                                                       tags,
                                                       str(entry['lat']),
                                                       str(entry['lon']))
            root.append(resource_node)
    generate_rdf_tree(root)


if __name__ == '__main__':
    generate_rdf_file()
