import os
import re

import pandas as pd
# Third Party Imports
from xml.etree import ElementTree as et

# Local imports
from geo_mapper import GEO_MAP


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
WEST_BANK_PATH = os.path.join(BASE_PATH, 'data/westbank/westbank.csv')
GAZA_PATH = os.path.join(BASE_PATH, 'data/gaza/gaza.csv')

RDF_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS_NAMESPACE = "http://www.w3.org/2000/01/rdf-schema#"
OSM_NAMESPACE = "https://raw.githubusercontent.com/birzeitknowledgegraph-2019/Ontology/master/osm.rdf#"
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
    'mastercard',
    'FROM AHD',
    'ele',
    'ref',
    'place,',
    'capital',
    'postal_code',
    'admin_level',
    'created_by',
    'accuracy',
    'image',
    'waterway',
    'url',
    'access',
    'artwork_type',
    'official_name',
    'geonames_id',
    'ssid',
    'toilets',
    'kosher',
    'stars',
    'automated',
    'self_service',
    'service',
    'clothes',
    'craft',
    'military',
    'organic',
    'instagram',
    'rooms',
    'buildingpart',
    'civilization',
    'youtube',
    'amenity_old',
    'From Wafaa',
    'addr_country',
    'addr_district',
    'addr_flats',
    'addr_full',
    'addr_interpolation',
    'addr_place',
    'addr_province',
    'addr_subdistrict',
    'addr_suburb',
    'addr_unit',
    'aerialway',
    'aerodrome_relation_type',
    'aeroway',
    'area',
    'artist',
    'artwork',
    'attraction',
    'backcountry',
    'backrest',
    'barrier',
    'bench',
    'bicycle',
    'boat',
    'branch',
    'bridge',
    'building_colour',
    'cairn',
    'capacity_disabled',
    'capital_city',
    'cargo',
    'cash_in',
    'cemetery',
    'charge',
    'check_date',
    'chicha',
    'city_served',
    'climbing',
    'climbing_boulder',
    'closest_town',
    'club',
    'colour',
    'communication_mobile_phone',
    'community',
    'company',
    'condition',
    'construction',
    'contact_email',
    'contact_fax',
    'contact_mobile',
    'contact_phone',
    'contact_website',
    'content',
    'cost',
    'crane_type',
    'crossing',
    'crossing_light',
    'cultural',
    'currency_EGP',
    'dataset',
    'denotation',
    'depth',
    'design',
    'diaper',
    'diplomatic_receiving_country',
    'diplomatic_sending_country',
    'direction',
    'display_digital',
    'District',
    'disused_shop',
    'door',
    'drive_in',
    'education',
    'elevator',
    'embankment',
    'embassy',
    'enforcement',
    'entrance',
    'established',
    'exit',
    'factory',
    'female',
    'ferry',
    'fitness_station',
    'foot',
    'ford',
    'frequency',
    'fuel_diesel',
    'gambling',
    'generator_method',
    'generator_source',
    'geological',
    'guest_house',
    'harbour',
    'height',
    'hiking',
    'history',
    'horse',
    'hotel',
    'hotline',
    'hyperbaric_chamber_diameter',
    'hyperbaric_chamber_length',
    'hyperbaric_chamber_maxpressure',
    'hyperbaric_chamber_places',
    'hyperbaric_chamber_scuba_diving',
    'industrial',
    'inscription',
    'int_ref',
    'intermittent',
    'internet_access_fee',
    'is_capital',
    'is_in_city',
    'is_in_continent',
    'is_in_country',
    'is_in_country_code',
    'is_in_state',
    'junction',
    'kerb',
    'landmark',
    'lanes',
    'layer',
    'leaf_cycle',
    'league',
    'loc_name',
    'local_ref',
    'location',
    'location_transition',
    'man_made',
    'material',
    'maxheight',
    'maxstay',
    'memorial',
    'mooring',
    'motor_vehicle',
    'motorcar',
    'motorcycle',
    'mountain',
    'mountain_pass',
    'network',
    'node',
    'noexit',
    'notice',
    'occupation',
    'oneway',
    'payment_bitcoin',
    'payment_cards',
    'payment_cash',
    'payment_coins',
    'payment_credit_cards',
    'payment_electronic_purses',
    'payment_notes',
    'payment_telephone_cards',
    'payment_visa',
    'platforms',
    'playground',
    'position_accuracy',
    'power',
    'product',
    'prominence',
    'pump',
    'raceway',
    'railway',
    'rank',
    'recycling_cans',
    'recycling_clothes',
    'recycling_paper',
    'reef',
    'relation_type',
    'residents',
    'Resort',
    'resource',
    'roof_height',
    'roof_shape',
    'room',
    'route',
    'ruins',
    'scuba_diving_air_fill',
    'scuba_diving_air_filling',
    'scuba_diving_attraction_biology',
    'scuba_diving_attraction_cave',
    'scuba_diving_attraction_drop_off',
    'scuba_diving_attraction_night',
    'scuba_diving_attraction_reef',
    'scuba_diving_attraction_rocks',
    'scuba_diving_courses',
    'scuba_diving_dangers_ship',
    'scuba_diving_depth',
    'scuba_diving_descent_line',
    'scuba_diving_divespot',
    'scuba_diving_education',
    'scuba_diving_emergency',
    'scuba_diving_entry',
    'scuba_diving_entry_boat',
    'scuba_diving_Equipment',
    'scuba_diving_filling',
    'scuba_diving_maxdepth',
    'scuba_diving_nitrox',
    'scuba_diving_nitrox_filling',
    'scuba_diving_oxygen_filling',
    'scuba_diving_relation_type',
    'scuba_diving_relation_type_cave',
    'scuba_diving_relation_type_drift',
    'scuba_diving_relation_type_lake',
    'scuba_diving_relation_type_sea',
    'scuba_diving_relation_type_wreck',
    'scuba_diving_rental',
    'scuba_diving_repair',
    'scuba_diving_spoken_languages',
    'scuba_diving_surface_brash',
    'scuba_diving_surface_sand',
    'scuba_diving_trimix_filling',
    'sculptor',
    'seamark',
    'seamark_beacon_cardinal_category',
    'seamark_beacon_cardinal_colour',
    'seamark_beacon_cardinal_colour_pattern',
    'seamark_beacon_cardinal_height',
    'seamark_beacon_cardinal_shape',
    'seamark_beacon_lateral_category',
    'seamark_beacon_lateral_colour',
    'seamark_beacon_lateral_colour_pattern',
    'seamark_beacon_lateral_height',
    'seamark_beacon_lateral_shape',
    'seamark_beacon_lateral_system',
    'seamark_beacon_safe_water_colour',
    'seamark_beacon_safe_water_colour_pattern',
    'seamark_beacon_safe_water_shape',
    'seamark_beacon_special_purpose_category',
    'seamark_beacon_special_purpose_colour',
    'seamark_buoy_cardinal_category',
    'seamark_buoy_cardinal_colour',
    'seamark_buoy_cardinal_colour_pattern',
    'seamark_buoy_cardinal_shape',
    'seamark_buoy_isolated_danger_colour',
    'seamark_buoy_isolated_danger_colour_pattern',
    'seamark_buoy_isolated_danger_shape',
    'seamark_buoy_lateral_category',
    'seamark_buoy_lateral_colour',
    'seamark_buoy_lateral_shape',
    'seamark_buoy_lateral_system',
    'seamark_buoy_safe_water_colour',
    'seamark_buoy_safe_water_colour_pattern',
    'seamark_buoy_safe_water_shape',
    'seamark_buoy_special_purpose_category',
    'seamark_buoy_special_purpose_colour',
    'seamark_buoy_special_purpose_shape',
    'seamark_fog_signal_category',
    'seamark_fog_signal_group',
    'seamark_fog_signal_period',
    'seamark_fog_signal_range',
    'seamark_harbour_category',
    'seamark_information',
    'seamark_landmark_category',
    'seamark_landmark_function',
    'seamark_light_1_category',
    'seamark_light_1_character',
    'seamark_light_1_colour',
    'seamark_light_1_group',
    'seamark_light_1_height',
    'seamark_light_1_multiple',
    'seamark_light_1_period',
    'seamark_light_1_range',
    'seamark_light_1_sector_end',
    'seamark_light_1_sector_start',
    'seamark_light_1_sequence',
    'seamark_light_2_category',
    'seamark_light_2_character',
    'seamark_light_2_colour',
    'seamark_light_2_group',
    'seamark_light_2_height',
    'seamark_light_2_period',
    'seamark_light_2_range',
    'seamark_light_2_sector_end',
    'seamark_light_2_sector_start',
    'seamark_light_3_character',
    'seamark_light_3_colour',
    'seamark_light_3_group',
    'seamark_light_3_height',
    'seamark_light_3_period',
    'seamark_light_3_range',
    'seamark_light_3_sector_end',
    'seamark_light_3_sector_start',
    'seamark_light_category',
    'seamark_light_character',
    'seamark_light_colour',
    'seamark_light_float_colour',
    'seamark_light_float_colour_pattern',
    'seamark_light_group',
    'seamark_light_height',
    'seamark_light_multiple',
    'seamark_light_period',
    'seamark_light_range',
    'seamark_light_reference',
    'seamark_light_sequence',
    'seamark_mooring_category',
    'seamark_platform_category',
    'seamark_radar_reflector',
    'seamark_radar_transponder_category',
    'seamark_radar_transponder_group',
    'seamark_radio_station_category',
    'seamark_rock_water_level',
    'seamark_signal_station_traffic_category',
    'seamark_small_craft_facility_category',
    'seamark_topmark_colour',
    'seamark_topmark_shape',
    'seamark_type',
    'seamark_wreck_category',
    'seasonal',
    'service_times',
    'shelter',
    'shisha',
    'shower',
    'signal',
    'source_population',
    'species',
    'sqkm',
    'station',
    'stay',
    'sub_sea',
    'subject',
    'submerged',
    'substation',
    'subway',
    'symbol',
    'tactile_paving',
    'taxi',
    'todo',
    'toilets_disposal',
    'toilets_wheelchair',
    'toll',
    'tomb',
    'tower',
    'tower_construction',
    'tower_type',
    'tracktype',
    'traffic_calming',
    'traffic_sign',
    'traffic_signals',
    'train',
    'tram',
    'travel',
    'tree',
    'trees',
    'trolleybus',
    'tunnel',
    'u-turn',
    'unisex',
    'vending',
    'verified',
    'voltage',
    'wall',
    'water',
    'wheelchair_description',
    'women',
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
    'is_in:city': 'is_in_city',
    'is_in:country': 'is_in_country',
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
    element_aut = et.Element('{https://raw.githubusercontent.com/birzeitknowledgegraph-2019/Ontology/master/osm.rdf#}author')
    element_aut.text = 'Mohammed AbuAisha'
    resource.append(element_aut)

    # Create element ID
    element_id = et.Element('{https://raw.githubusercontent.com/birzeitknowledgegraph-2019/Ontology/master/osm.rdf#}id')
    element_id.text = node_id
    resource.append(element_id)

    element_lat = et.Element('{https://raw.githubusercontent.com/birzeitknowledgegraph-2019/Ontology/master/osm.rdf#}latitude')
    element_lat.text = lat
    resource.append(element_lat)

    element_lon = et.Element('{https://raw.githubusercontent.com/birzeitknowledgegraph-2019/Ontology/master/osm.rdf#}longitude')
    element_lon.text = lon
    resource.append(element_lon)

    geo_resource = GEO_MAP.get(node_id)
    if geo_resource:
        owl_geo = et.Element('{http://www.w3.org/2002/07/owl#}sameAs')
        owl_geo.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource',
                    geo_resource)
        resource.append(owl_geo)

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
                key = '{https://raw.githubusercontent.com/birzeitknowledgegraph-2019/Ontology/master/osm.rdf#}' + key
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
    # generate_owl_ontology(root)
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
