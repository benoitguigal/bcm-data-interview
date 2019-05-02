# -*- coding: utf-8 -*-

from geojson import Point, dumps
from peewee import *

from .utils import get_current_hour
from .connectors import DatanovaConnector, MockarooConnector
from .models import db, Temperature, Region, TemperatureWithRegion, \
    TemperatureByRegion


def filter_country(country, data):
    """ keeps records for a particular country """
    return [record for record in data if record['country'] == country]


def filter_null(data):
    """ remove records with null temperature """
    return [record for record in data if record['temperature'] is not None]


def add_geo_json(data):
    """ add a geojson field to temperature data """
    for record in data:
        point = Point((float(record['lon']), float(record['lat'])))
        record['point'] = dumps(point)
    return data


def add_current_hour(data):
    """ add current hour to records """
    hour = get_current_hour()
    for record in data:
        record['hour'] = hour
    return hour, data


def load_regions():
    """ load regions geographic contour to MySQL """
    connector = DatanovaConnector()
    data = connector.get_data()
    bulk_insert_region(data)


def bulk_insert_temperature(data):
    """ insert temperature data in bulk """
    with db.atomic():
        Temperature.insert_many(data).execute()


def bulk_insert_region(data):
    """ insert region geographic data in bulk """
    with db.atomic():
        Region.insert_many(data).execute()


def join_temperature_with_region(hour):
    """ add region to temperature records based on geoshapes """
    query = (Temperature
             .select(
                Temperature.hour,
                Temperature.temperature,
                Temperature.lon,
                Temperature.lat,
                Region.code,
                Region.name)
             .where(Temperature.hour == hour)
             .join(Region,
                   on=fn.ST_Contains(Region.geo_shape, Temperature.point)))
    for (hour, temperature, lon,
            lat, region_code, region_name) in query.tuples().iterator():
        TemperatureWithRegion.create(
            hour=hour,
            temperature=temperature,
            lon=lon,
            lat=lat,
            region_code=region_code,
            region_name=region_name)


def mean_temperature_by_region(hour):
    query = (TemperatureWithRegion
             .select(
                TemperatureWithRegion.region_name,
                TemperatureWithRegion.hour,
                fn.Avg(TemperatureWithRegion.temperature).alias('temperature'),
                fn.Count(TemperatureWithRegion.id).alias('number_of_points'))
             .where(TemperatureWithRegion.hour == hour)
             .group_by(
                 TemperatureWithRegion.region_name,
                 TemperatureWithRegion.hour))
    for (region_name,
         hour,
         temperature,
         number_of_points) in query.tuples().iterator():
        TemperatureByRegion.create(
            region_name=region_name,
            hour=hour,
            temperature=temperature,
            number_of_points=number_of_points)