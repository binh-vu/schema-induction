#!/usr/bin/python
# -*- coding: utf-8 -*-

from .type import Type
from .union_type import UnionType


class ListType(Type):
    """
        Represent the list type and its size if possible
        we interest in empty list, list have only 1 value or (1 or empty) value
    """

    MAX_N_KEEP_VALUE = 7

    def __init__(self):
        self.record_type = None
        """
            This set is used to keep maximum n values, to report maximum n-1
            possible size, e.g:
            for any k, t, p >= 0 and n = 3:
                + [k]: list have exactly k elements
                + [k, t]: have either k or t elements
                + [k, t, p]: we don't any information about size of list
        """
        self.possible_sizes = set([])

    def add(self, rtype):
        """
            Add type of a record

            :param rtype: Type
            :return: ListType
        """
        if self.record_type is None:
            self.record_type = rtype
        else:
            self.record_type = self.record_type.merge(rtype)
        return self

    def set_size(self, size):
        """
            Add size of a instance of ListType to the set of possible sizes
        :param size:
        :return:
        """
        if len(self.possible_sizes) >= ListType.MAX_N_KEEP_VALUE:
            return self

        self.possible_sizes.add(size)
        return self

    def optimize(self):
        """
            @inherit
        """
        if self.record_type is not None:
            self.record_type = self.record_type.optimize()

        return self

    def merge(self, another):
        """
            @inherit
        """
        if isinstance(another, ListType):
            if self.record_type is None:
                self.record_type = another.record_type
            elif another.record_type is not None:
                self.record_type = self.record_type.merge(another.record_type)

            # merge set of possible sizes of 2 list comply to self.possible_sizes's definition
            for n in another.possible_sizes:
                if len(self.possible_sizes) >= ListType.MAX_N_KEEP_VALUE:
                    break
                self.possible_sizes.add(n)

            return self

        return UnionType().add(self).add(another)

    def to_string(self, shift=0, indent=0):
        prefix_space = ' ' * shift
        indent_space = ' ' * indent

        if len(self.possible_sizes) >= ListType.MAX_N_KEEP_VALUE:
            size = ''
        else:
            size = '[%s]' % (','.join(str(x) for x in self.possible_sizes))

        if self.record_type is None:
            text = ''
        else:
            text = self.record_type.to_string(shift + indent, indent)

        # heuristic rules to determine if we could use shorthand
        # if the record type is simple type (primitive type, none type, or union type
        # which only span in one line, then it would be short enough for to represent
        # list type in one line
        if text.find('\n') == -1:
            return 'list%s(%s)' % (size, text)

        # full rendering
        text = prefix_space + indent_space + text
        return 'list%s(\n%s\n%s)' % (size, text, prefix_space)
