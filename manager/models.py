# -*- coding: utf-8 -*-

import requests


class SparePart(object):
    """ Manages single spare part data. """

    def __init__(self, name, count=0, arrive=0, mustbe=0):
        self._name = name
        self._count = count
        self._arrive = arrive
        self._mustbe = mustbe

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value:
            self._name = value
        else:
            raise ValueError('Spare part`s name is empty.')

    @property
    def order_quantity(self):
        """ Returns quantity we should order. """
        quantity = self._count + self._arrive
        if self._mustbe > quantity:
            return self._mustbe - quantity
        else:
            return 0

    @property
    def mustbe(self):
        return self._mustbe

    @mustbe.setter
    def mustbe(self, value):
        if value > self._mustbe:
            self._mustbe = value

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    @property
    def arrive(self):
        return self._arrive

    @arrive.setter
    def arrive(self, value):
        self._arrive = value

    def __repr__(self):
        return '{} c:{} a:{} m:{}'.format(self._name, self._count,
                                          self._arrive, self._mustbe)


class SparePartsManager(object):
    """ Gets spare parts data and deals with associated logic. """

    _SPARE_PARTS_URL = 'https://job.firstvds.ru/spares.json'
    _ALTERNATIVES_URL = 'https://job.firstvds.ru/alternatives.json'

    def __init__(self):
        try:
            spare_parts_data = requests.get(self._SPARE_PARTS_URL).json()
            self._parts = list(self._parse_parts_data(spare_parts_data))
            self._alternatives = requests.get(self._ALTERNATIVES_URL).json()
        except requests.exceptions.ConnectionError:
            raise ValueError('Error getting parts data from server.')

    @property
    def parts_grouped(self):
        """ Returns spare parts` dict grouped by alternatives. """
        parts_grouped = {}
        for part in self._parts_grouped():
            parts_grouped.update(self._dict_from_part(part))
        return parts_grouped

    @property
    def parts_for_order(self):
        """ Returns spare parts` dict we should order. """
        parts_for_order = {}
        for part in self._parts_for_order():
            parts_for_order.update(self._order_dict_from_part(part))
        return parts_for_order

    def _parts_grouped(self):
        """ Returns SparePart's` list grouped by alternatives. """
        grouped = []

        for part in self._parts:
            group_name = self._get_part_alternative(part.name)
            if not group_name:
                grouped.append(part)
            else:
                group = self._find_in_parts(group_name, grouped)
                if not group:
                    group = SparePart(group_name)
                    grouped.append(group)
                group.mustbe = part.mustbe
                group.count += part.count
                group.arrive += part.arrive
        return grouped

    def _parts_for_order(self):
        """ Returns SparePart's` list we should order. """
        parts = self._parts_grouped()
        return [part for part in parts if part.order_quantity != 0]

    def _get_part_alternative(self, part_name):
        """Returns alternative name of the spare part. """
        for group_name, group in self._alternatives['alternatives'].items():
            if part_name in group:
                return group_name
        return None

    """ Helpers """

    @staticmethod
    def _find_in_parts(name, parts):
        for part in parts:
            if part.name == name:
                return part
        return None

    @staticmethod
    def _dict_from_part(part):
        d = {}
        d[part.name] = {}
        d[part.name]['count'] = part.count
        d[part.name]['arrive'] = part.arrive
        d[part.name]['mustbe'] = part.mustbe
        return d

    @staticmethod
    def _order_dict_from_part(part):
        d = {}
        d[part.name] = {}
        d[part.name]['quantity'] = part.order_quantity
        return d

    @staticmethod
    def _parse_parts_data(data):
        for name, values in data.items():
            yield SparePart(name,
                            values['count'],
                            values['arrive'],
                            values['mustbe'])
