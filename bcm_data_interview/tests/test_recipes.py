# -*- coding: utf-8 -*-

from unittest import TestCase
from ..recipes import filter_country, filter_null, add_geo_json


class RecipesTestCase(TestCase):

    def test_filter_country(self):
        """ it should filter data based on country """
        data = [
            {'id': 1, 'country': 'France'},
            {'id': 2, 'country': 'Spain'},
            {'id': 3, 'country': 'Germany'},
            {'id': 4, 'country': 'France'}
        ]
        filtered = filter_country('France', data)
        expected = [
            {'id': 1, 'country': 'France'},
            {'id': 4, 'country': 'France'}
        ]
        self.assertEqual(filtered, expected)

    def test_filter_null(self):
        """ it should remove null temperatures """
        data = [
            {id: 1, 'temperature': 27.81},
            {id: 2, 'temperature': None},
            {id: 3, 'temperature': 28.98}
        ]
        filtered = filter_null(data)
        expected = [
            {id: 1, 'temperature': 27.81},
            {id: 3, 'temperature': 28.98}
        ]
        self.assertEqual(filtered, expected)

    def test_add_geojson(self):
        """ it should add geojosn field based on lat/lon"""
        data = [
            {id: 1, 'lat': 1, 'lon': 2},
        ]
        data = add_geo_json(data)
        record = data[0]
        expected = '{"type": "Point", "coordinates": [2.0, 1.0]}'
        self.assertEqual(record['point'], expected)
