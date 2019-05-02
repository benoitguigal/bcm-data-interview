# -*- coding: utf-8 -*-

import os

# TEMPERATURE API CONFIGURATION

MOCKAROO_API_URL = 'https://my.api.mockaroo.com/sensor/temperatures'

MOCKAROO_API_KEY = os.environ['MOCKAROO_API_KEY']

# DATANOVA API CONFIGURATION

DATANOVA_API_URL = 'https://datanova.laposte.fr/api/records/1.0/search/?' + \
                    'dataset=contours-geographiques-des-nouvelles-regions-' + \
                    'metropole&facet=region'

# MYSQL CONFIGURATION

MYSQL_DB = 'benoit'

MYSQL_HOST = os.environ['MYSQL_HOST']

MYSQL_USER = 'benoit'

MYSQL_PWD = os.environ['MYSQL_PWD']
