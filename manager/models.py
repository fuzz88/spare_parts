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

    @property
    def parts_grouped(self):
        if self._parts is None:
            # If there is no parts data then...
            return None  # it will be handled on the level above.

        parts_grouped = {}

        for part, values in self._parts.items():
            # Iterate through the all parts
            group_name = self.get_alternative_group(part)
            # Does the part have an alternatives group?
            if group_name is None:
                parts_grouped[part] = values  # No: keep data unchanged
            else:
                if group_name not in parts_grouped:
                    # Yes: in that case we should make a group, if it's not already exists,
                    values_mockup = {'count': 0, 'arrive': 0, 'mustbe': []}
                    parts_grouped[group_name] = values_mockup
                #  and sum up values
                parts_grouped[group_name]['count'] += values['count']
                parts_grouped[group_name]['arrive'] += values['arrive']
                # There will be list for 'mustbe' values, at first
                parts_grouped[group_name]['mustbe'].append(values['mustbe'])

                # TODO: maybe we would like to save the alternatives for the future, like
                # parts_grouped[group_name]['alt_list'].append(self._parts[part])

        for part in parts_grouped:
            if isinstance(parts_grouped[part]['mustbe'], list):
                max_value = max(parts_grouped[part]['mustbe'])
                del parts_grouped[part]['mustbe']
                # Replace 'mustbe' list with max_value of the list, at second
                parts_grouped[part]['mustbe'] = max_value

        return parts_grouped

    @property
    def parts_for_order(self):
        if self._parts is None:
            return None

        order = {}

        parts = self.parts_grouped

        for part, values in parts.items():
            parts_quantity = values['count'] + values['arrive']
            if values['mustbe'] > parts_quantity:
                order[part] = {'quantity': values['mustbe'] - parts_quantity}

        return order

    def get_alternative_group(self, part_name):
        for group_name, group in self._alternatives['alternatives'].items():
            if part_name in group:
                return group_name
        return None
