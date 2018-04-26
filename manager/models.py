# -*- coding: utf-8 -*-

import requests


class SparePartsManager(object):
    """ Gets spare parts data and deals with associated logic.
    """
    _SPARE_PARTS_URL = 'https://job.firstvds.ru/spares.json'
    _ALTERNATIVES_URL = 'https://job.firstvds.ru/alternatives.json'

    def __init__(self):
        try:
            self._parts = requests.get(self._SPARE_PARTS_URL).json()
            self._alternatives = requests.get(self._ALTERNATIVES_URL).json()
        except RuntimeError:
            print('BAD NEWS')
            self._parts = None
            self._alternatives = None

    def all_parts(self):
        pass

    def parts_to_order(self):
        pass
