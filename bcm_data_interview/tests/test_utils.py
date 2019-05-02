# -*- coding: utf-8 -*-

from unittest import TestCase, mock
from datetime import datetime

from ..utils import get_current_hour


class UtilsTestCase(TestCase):

    @mock.patch('bcm_data_interview.utils.datetime')
    def test_get_current_hour(self, datetime_mock):
        """ it should return current hour """
        datetime_mock.now.return_value = datetime(2019, 5, 2, 16, 23, 10)
        hour = get_current_hour()
        expected = datetime(2019, 5, 2, 16, 0, 0)
        self.assertEqual(hour, expected)
