# -*- coding: utf-8 -*-

import requests
import geojson

from .config import MOCKAROO_API_URL, MOCKAROO_API_KEY, DATANOVA_API_URL


class MockarooConnector(object):
    """
    Connect to mockaroo API and parse temperature sensor data
    """
    def __init__(self):
        self.api_url = MOCKAROO_API_URL
        self.api_key = MOCKAROO_API_KEY

    def get_data(self):
        headers = {'X-API-Key': self.api_key}
        r = requests.get(self.api_url, headers=headers)
        data = r.json()
        temperatures = []
        for record in data:
            temperature = {
                'api_id': record['id'],
                'timestamp': record['timestamp'],
                'temperature': record['temperature'],
                'lon': record['lon'],
                'lat': record['lat'],
                'country': record['country']
            }
            temperatures.append(temperature)
        return temperatures


class DatanovaConnector(object):
    """
    Connect to datanova API and parse French region geographic limits
    """
    def __init__(self):
        self.api_url = DATANOVA_API_URL

    def get_data(self):
        r = requests.get(self.api_url)
        data = r.json()
        regions = []
        for record in data['records']:
            region = {
                'name': record['fields']['region'],
                'code': record['fields']['new_code'],
                'geo_shape': geojson.dumps(record['fields']['geo_shape'])
            }
            regions.append(region)
        return regions
