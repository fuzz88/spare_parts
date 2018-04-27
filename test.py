#!/usr/bin/env python
# -*- coding: utf-8 -*-
from manager.models import SparePartsManager
import unittest
from unittest.mock import patch
from types import SimpleNamespace


class SparePartsManagerTestCase(unittest.TestCase):
    """ Sample test case
    """

    def urls(url):
        """ Patch side_effect, that pretends to be requests.get
        """
        _SPARE_PARTS_URL = 'https://job.firstvds.ru/spares.json'
        _ALTERNATIVES_URL = 'https://job.firstvds.ru/alternatives.json'

        def spare_parts():
            return {'part100': {'count': 1, 'mustbe': 3, 'arrive': 0},
                    'part101': {'count': 2, 'mustbe': 0, 'arrive': 0},
                    'part200': {'count': 5, 'mustbe': 8, 'arrive': 3},
                    'part300': {'count': 1, 'mustbe': 0, 'arrive': 1},
                    'part301': {'count': 1, 'mustbe': 4, 'arrive': 0}}

        def alternatives():
            return {'alternatives': {'part1xx': ['part100', 'part101'],
                                     'part3xx': ['part300', 'part301']}}

        if url == _SPARE_PARTS_URL:
            return SimpleNamespace(**{'json': spare_parts})
        if url == _ALTERNATIVES_URL:
            return SimpleNamespace(**{'json': alternatives})
        raise NotImplementedError

    @patch('requests.get', side_effect=urls)
    def setUp(self, requests_get_patched):
        self.manager = SparePartsManager()

    """ TESTS
    """
    def test_parts_grouped(self):
        self.assertDictEqual(self.manager.parts_grouped,
                             {'part1xx': {'count': 3, 'mustbe': 3, 'arrive': 0},
                              'part200': {'count': 5, 'mustbe': 8, 'arrive': 3},
                              'part3xx': {'count': 2, 'mustbe': 4, 'arrive': 1}})

    def test_parts_for_order(self):
        self.assertDictEqual(self.manager.parts_for_order,
                             {'part3xx': {'quantity': 1}})


if __name__ == '__main__':
    unittest.main()
