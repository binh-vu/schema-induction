#!/usr/bin/python
# -*- coding: utf-8 -*-

import io

import unicodecsv as csv

from schema_induction.type import Type
from schema_induction.union_type import UnionType


def dump_csv(array, delimiter=','):
    f = io.BytesIO()
    writer = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_ALL)
    writer.writerow(array)
    return f.getvalue()[:-2].decode('utf-8')


class PrimitiveType(Type):
    """
        Represent primitive type such as string, float, int
    """

    MAX_N_KEEP_VALUE = 7

    def __init__(self, type=None):
        if type is None:
            self.type = None
        else:
            self.set_type(type)
        # implement using dictionary so we can keep the order
        self.possible_values = {}

    def set_type(self, type):
        assert type in {'float', 'int', 'str', 'bool'}, type
        self.type = type
        return self

    def add_value(self, value):
        if len(self.possible_values) > PrimitiveType.MAX_N_KEEP_VALUE:
            return self

        if value not in self.possible_values:
            self.possible_values[value] = 1
        return self

    def is_mergeable(self, another):
        """
            test if two PRIMITIVE TYPEs can be merged

            :param another: PrimitiveType
            :return: bool
        """
        if not isinstance(another, PrimitiveType):
            return False

        return self.type == another.type or {self.type, another.type} == {'float', 'int'}

    def optimize(self):
        """
            @inherit
        """
        return self

    def merge(self, another):
        """
            @inherit
        """
        if isinstance(another, PrimitiveType):
            if self.type == another.type:
                for value in another.possible_values.keys():
                    self.add_value(value)
                return self

            if {self.type, another.type} == {'float', 'int'}:
                self.type = 'float'
                return self

        return UnionType().add(self).add(another)

    def to_string(self, shift=0, indent=0):
        """
            @inherit
        """
        if len(self.possible_values) < PrimitiveType.MAX_N_KEEP_VALUE:
            string = '%s{%s}' % (self.type, dump_csv(list(self.possible_values.keys())))
            return string
        else:
            return self.type


class NoneType(Type):
    """
        Represent null
    """

    def optimize(self):
        """
            @inherit
        """
        return self

    def merge(self, another):
        """
            @inherit
        """
        if isinstance(another, NoneType):
            return self
        return another.merge(self)

    def to_string(self, shift=0, indent=0):
        """
            @inherit
        """
        return "null"
