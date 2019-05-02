# -*- coding: utf-8 -*-

from .connectors import MockarooConnector
from .recipes import filter_country, filter_null, \
    add_geo_json, add_current_hour, bulk_insert_temperature, \
    join_temperature_with_region, mean_temperature_by_region


def run():

    connector = MockarooConnector()
    temperatures = connector.get_data()

    # keep only france records
    temperatures = filter_country('France', temperatures)

    # filter null records
    temperatures = filter_null(temperatures)

    # add geojson field
    temperatures = add_geo_json(temperatures)

    # add current hour
    hour, temperatures = add_current_hour(temperatures)

    # append data to MySQL table
    bulk_insert_temperature(temperatures)

    # join temperature with region
    join_temperature_with_region(hour)

    # compute mean temperature by region
    mean_temperature_by_region(hour)


if __name__ == '__main__':
    run()
