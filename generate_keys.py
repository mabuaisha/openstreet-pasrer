import csv
import os
from xml.etree import ElementTree as et
import pandas as pd

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
WEST_BANK_PATH = os.path.join(BASE_PATH, 'data/westbank/westbank.csv')
GAZA_PATH = os.path.join(BASE_PATH, 'data/gaza/gaza.csv')

if __name__ == '__main__':
    headers = [['osm_id', 'lat', 'long']]
    csv.register_dialect('myDialect',
                         quoting=csv.QUOTE_ALL,
                         skipinitialspace=True)
    for source_path in [GAZA_PATH, WEST_BANK_PATH]:
        with open(source_path, mode='r') as csv_file:
            data = pd.read_csv(csv_file)
            for _, entry in data.iterrows():
                headers.append([str(entry['id']), str(entry['lat']), str(entry['lon'])])

    with open('osm_data.csv', 'w') as f:
        writer = csv.writer(f, dialect='myDialect')
        for row in headers:
            writer.writerow(row)
