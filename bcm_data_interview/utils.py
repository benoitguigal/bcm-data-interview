# -*- coding: utf-8 -*-

from datetime import datetime
from pytz import timezone


def get_current_hour():
    return datetime.now(timezone('Europe/Paris')).replace(
        microsecond=0,
        second=0,
        minute=0)
