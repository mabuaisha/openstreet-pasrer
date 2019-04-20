import os
import re

import pandas as pd
# Third Party Imports
from xml.etree import ElementTree as et


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
WEST_BANK_PATH = os.path.join(BASE_PATH, 'data/westbank/westbank.csv')
GAZA_PATH = os.path.join(BASE_PATH, 'data/gaza/gaza.csv')

RDF_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS_NAMESPACE = "http://www.w3.org/2000/01/rdf-schema#"
OSM_NAMESPACE = "https://www.openstreetmap.org#"
XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema-datatypes"
OWL_NAMESPACE = "http://www.w3.org/2002/07/owl#"
OSM_URL = "https://www.openstreetmap.org/node/{0}"
WIKIDATA_URL = 'https://wikidata.org/entity/{0}'

DATA_SOURCES = (
    WEST_BANK_PATH,
    GAZA_PATH
)

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
    'alt_name2',
    'fixme',
    'name_1',
    'ele',
    'yes',
    'ref',
    'children\'s home',
    'wikipedia_1',
    'ice_cream;cafe',
    'cafe;restaurant',
    'cafe ; billiard',
)

KEYS = (
    'author',
    'id',
    'type',
    'latitude',
    'longitude',
    'uid',
    'name',
    'tourism',
    'wikidata',
    'country_code',
    'housenumber',
    'facebook',
    'phone',
    'wikipedia',
    'street',
    'postcode',
    'website',
    'city',
    'Twitter',
    'amenity',
    'housename',
    'bar',
    'botanical',
    'payment',
    'fax',
    'cash',
    'population',
    'credit_cards',
    'continent',
    'vegetarian',
    'cardboard',
    'municipality_name',
    'inscription_date',
    'warm_meals',
    'levels',
    'country',
    'operator',
    'diameter',
    'position',
    'debit_cards',
    'handwashing',
    'wheelchair',
    'description',
    'acquisition_date',
    'speciality',
    'oil',
    'event_code',
    'floor',
    'quantity',
    'war',
    'google_plus',
    'distance_meter',
    'opening_hours',
    'email',
    'internet_access',
    'smoking',
    'cuisine',
    'shop',
    'delivery',
    'outdoor_seating',
    'religion',
    'takeaway',
    'building',
    'denomination',
    'target',
    'diplomatic',
    'dispensing',
    'healthcare',
    'parking',
    'supervised',
    'surface',
    'fee',
    'lit',
    'capacity',
    'designation',
    'drive_through',
    'atm',
    'is_in',
    'emergency',
    'note',
    'office',
    'start_date',
    'level',
    'highway',
    'int_name',
    'social_facility',
    'historic',
    'mapillary',
    'alt_name',
    'leisure',
    'photo_url',
    'landuse',
    'community_centre',
    'wifi',
    'brand',
    'source',
    'place_of_worship',
    'maxspeed',
    'natural',
    'studio',
    'old_name',
    'comment',
    'sport',
    'information',
    'opened',
    'postmaster',
    'disused',
    'recyclingclothes',
    'recyclingglass',
    'recyclingbatteries',
    'bus',
    'public_transport',
    'boundary',
    'beverage',
    'brewery',
    'indoor',
    'covered',
    'mobile',
    'abandoned',
    'mastercard'
)

OWL_MAP = {
    'addr:country': 'country',
    'addr:housenumber': 'housenumber',
    'contact:phone': 'phone',
    'addr:street': 'street',
    'addr:street:en': 'street',
    'addr:postcode': 'postcode',
    'addr:city': 'city',
    'addr:housename': 'housename',
    'payment:credit_cards': 'credit_cards',
    'payment:debit_cards': 'debit_cards',
    'payment:mastercard': 'mastercard',
    # 'payment:cash': 'payment',
    # 'payment:notes': 'payment',
    # 'payment:visa': 'payment',
    # 'payment:coins': 'payment',
    # 'payment:telephone_cards': 'payment',
    'diet:vegetarian': 'vegetarian',
    'diet:vegan': 'vegetarian',
    'toilets:wheelchair': 'wheelchair',
    'wheelchair:description': 'wheelchair',
    'healthcare:speciality': 'healthcare',
    # 'is_in:city': 'is_in',
    # 'is_in:country': 'is_in',
    'recycling:clothes': 'recyclingclothes',
    'recycling:glass': 'recyclingglass',
    'recycling:batteries': 'recyclingbatteries',
    'phone:mobile': 'mobile'
}

NAME_REGEX = '^(name|notes)[:]+[0-9a-zA-Z]{2}$'
UNDERSCORE_REGEX = '^[0-9a-zA-Z]+[_]+[0-9a-zA-Z]+[:]+[0-9a-zA-Z]{2}$'
ADDRESS_REGEX = '^[0-9a-zA-Z]+[:]+[0-9a-zA-Z]+[:]+[0-9a-zA-Z]{2}$'


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


def generate_rdf_node_resource(node_id, tags, lat, lon, keys):
    resource_uri = OSM_URL.format(node_id)
    resource = et.Element(
        '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description')
    resource.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about',
                 resource_uri)

    element_type = et.Element(
        '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}type')
    resource.append(element_type)
    element_type.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', '#node')

    # Create element ID
    element_aut = et.Element('{https://www.openstreetmap.org#}author')
    element_aut.text = 'Mohammed AbuAisha'
    resource.append(element_aut)

    # Create element ID
    element_id = et.Element('{https://www.openstreetmap.org#}id')
    element_id.text = node_id
    resource.append(element_id)

    element_lat = et.Element('{https://www.openstreetmap.org#}latitude')
    element_lat.text = lat
    resource.append(element_lat)

    element_lon = et.Element('{https://www.openstreetmap.org#}longitude')
    element_lon.text = lon
    resource.append(element_lon)

    for key, value in tags.items():
        if key == 'country':
            tags[key] = 'Palestine'
            break
    else:
        tags['country'] = 'Palestine'

    for key, value in tags.items():
        if value:
            if key not in keys:
                keys.append(key)
            if key in IGNORE_KEYS:
                continue
            elif key == 'amenity':
                value = TAGS_AMINTY_MAPPER.get(tags['amenity'], tags['amenity'])
            elif key == 'wikidata':
                owl_same = et.Element('{http://www.w3.org/2002/07/owl#}sameAs')
                owl_same.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource',
                             WIKIDATA_URL.format(value))
                resource.append(owl_same)

            lang_attr = None
            if re.match(NAME_REGEX, key):
                key, lang_attr = key.split(':')

            if OWL_MAP.get(key):
                key = OWL_MAP[key]

            # for delimiter in ['_', ':']:
            #     key = generate_key_using_delimiter(key, delimiter)
            if key in KEYS:
                key = '{https://www.openstreetmap.org#}' + key
                element_tag = et.Element(key)
                # element_tag.set('rdf:datatype', 'string')
                if lang_attr:
                    element_tag.set('xml:lang', lang_attr)
                element_tag.text = value
                resource.append(element_tag)

    return resource


def generate_root_rdf():

    et.register_namespace('osm', OSM_NAMESPACE)
    et.register_namespace('rdf', RDF_NAMESPACE)
    et.register_namespace('owl', OWL_NAMESPACE)
    et.register_namespace('rdfs', RDFS_NAMESPACE)
    rdf = et.Element('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF')
    rdf.set('xmlns:xsd', XSD_NAMESPACE)
    return rdf


def generate_owl_ontology(root):
    owl = et.Element('{http://www.w3.org/2002/07/owl#}Ontology')
    owl.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', 'osm')
    rdfs = et.Element('{http://www.w3.org/2000/01/rdf-schema#}comment')
    rdfs.text = 'Open Street Map Ontology'
    owl.append(rdfs)

    root.append(owl)

    class_element = et.Element('{http://www.w3.org/2002/07/owl#}Class')
    class_element.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', 'node')
    root.append(class_element)

    for key in KEYS:
        data_type = 'xsd:string'
        if key == 'id':
            data_type = 'xsd:integer'

        element_type = et.Element('{http://www.w3.org/2002/07/owl#}DatatypeProperty')
        element_type.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', key)
        domain = et.Element('{http://www.w3.org/2000/01/rdf-schema#}domain')
        domain.set('{http://www.w3.org/2000/01/rdf-schema#}resource', '#node')
        range_element = et.Element('{http://www.w3.org/2000/01/rdf-schema#}range')
        range_element.set('{http://www.w3.org/2000/01/rdf-schema#}resource', data_type)
        element_type.append(domain)
        element_type.append(range_element)
        root.append(element_type)


def generate_rdf_tree(root, source_path):
    tree = et.ElementTree(root)
    xml_name = os.path.basename(source_path).split('.')[0] + '.xml'
    file_name = '{0}/{1}'.format(os.path.dirname(source_path), xml_name)
    tree.write(file_name,
               encoding='utf-8',
               xml_declaration=True,
               method='xml')


def generate_rdf_file(source_path):
    keys = []
    root = generate_root_rdf()
    generate_owl_ontology(root)
    with open(source_path, mode='r') as csv_file:
        data = pd.read_csv(csv_file)
        for _, entry in data.iterrows():
            tags = generate_tags(entry['tags'])
            resource_node = generate_rdf_node_resource(str(entry['id']),
                                                       tags,
                                                       str(entry['lat']),
                                                       str(entry['lon']),
                                                       keys)
            root.append(resource_node)
    generate_rdf_tree(root, source_path)


if __name__ == '__main__':
    for source in DATA_SOURCES:
        generate_rdf_file(source)
