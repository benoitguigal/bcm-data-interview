# -*- coding: utf-8 -*-

from peewee import *

from .config import MYSQL_DB, MYSQL_HOST, MYSQL_HOST, MYSQL_USER, MYSQL_PWD


db = MySQLDatabase(
    MYSQL_DB,
    user=MYSQL_USER,
    password=MYSQL_PWD,
    host=MYSQL_HOST,
    port=3306)


class BaseModel(Model):

    class Meta:
        database = db


class GeometryField(Field):

    field_type = 'geometry'

    def db_value(self, value):
        return fn.ST_GeomFromGeoJSON(value)


class Temperature(BaseModel):

    api_id = CharField(unique=True)
    timestamp = DateTimeField()
    hour = DateTimeField()
    lon = FloatField()
    lat = FloatField()
    point = GeometryField()
    temperature = FloatField()
    country = CharField()


class Region(BaseModel):

    name = CharField()
    code = CharField()
    geo_shape = GeometryField()


class TemperatureWithRegion(BaseModel):

    hour = DateTimeField()
    lon = FloatField()
    lat = FloatField()
    temperature = FloatField()
    region_name = CharField()
    region_code = CharField()


class TemperatureByRegion(BaseModel):

    temperature = FloatField()
    hour = DateTimeField()
    region_name = CharField()
    number_of_points = IntegerField()


db.connect()
db.create_tables([
    Temperature,
    Region,
    TemperatureWithRegion,
    TemperatureByRegion
])
