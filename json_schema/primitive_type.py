#!/usr/bin/python
# -*- coding: utf-8 -*-

import StringIO
import unicodecsv as csv
from .type import Type
from .union_type import UnionType


def dump_csv(array, delimiter=','):
    f = StringIO.StringIO()
    writer = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_ALL, encoding='utf-8')
    writer.writerow(array)
    return f.getvalue()[:-2]


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
        self.possible_values = set()

    def set_type(self, type):
        assert type in {'float', 'int', 'str', 'bool', 'unicode'}, type
        self.type = type
        return self

    def add_value(self, value):
        if len(self.possible_values) > PrimitiveType.MAX_N_KEEP_VALUE:
            return self

        self.possible_values.add(value)
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
                for value in another.possible_values:
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
            return '%s{%s}' % (self.type, dump_csv(list(self.possible_values)))
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
