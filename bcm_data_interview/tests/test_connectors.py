# -*- coding: utf-8 -*-

from unittest import TestCase, mock
import geojson

from ..connectors import MockarooConnector, DatanovaConnector


class MockarooConnectorTestCase(TestCase):

    @mock.patch('bcm_data_interview.connectors.requests')
    def test_get_data(self, mock_requests):
        """ it should retrieve and parse mockaroo temperature data """
        connector = MockarooConnector()
        mock_response = mock.Mock()
        mock_response.json.return_value = [
            {
                'id': '95393b44-aa13-4271-a3c1-a1dedcbda410',
                'timestamp': '2019-05-01 10:49:43',
                'lat': 48.8493975,
                'lon': 2.4751086,
                'temperature': 24.8781,
                'country': 'France'
            },
            {
                'id': 'f299490a-d24a-48cc-9fbc-846676826b95',
                'timestamp': '2019-05-01 10:49:43',
                'lat': 48.8478808,
                'lon': 2.5525914,
                'temperature': 32.7554,
                'country': 'France'
            }
        ]
        mock_requests.get.return_value = mock_response
        temperatures = connector.get_data()
        self.assertEqual(len(temperatures), 2)
        temperature = temperatures[0]
        expected_keys = [
            'api_id',
            'timestamp',
            'lon',
            'lat',
            'temperature',
            'country']
        for key in expected_keys:
            self.assertIn(key, temperature.keys())


class DatanovaConnectorTestCase(TestCase):

    @mock.patch('bcm_data_interview.connectors.requests')
    def test_get_data(self, mock_requests):
        """ it should retrieve and parse regions geographic limits """
        connector = DatanovaConnector()
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            'records': [
                {
                    'fields': {
                        'geo_shape': {
                            'type': 'Polygon',
                            'coordinates': [
                                [
                                    5.443531596727628,
                                    47.40702721709622
                                ]
                            ]
                        },
                        'region': 'Bourgogne-France-Compté',
                        'new_code': '27'
                    }
                }
            ]
        }
        mock_requests.get.return_value = mock_response
        regions = connector.get_data()
        self.assertEqual(len(regions), 1)
        region = regions[0]
        expected_keys = ['name', 'code', 'geo_shape']
        for key in expected_keys:
            self.assertIn(key, region)
