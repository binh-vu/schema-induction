#!/usr/bin/python
# -*- coding: utf-8 -*-


class Type(object):

    def optimize(self):
        """
            Optimize the type
        """
        raise Exception('Not implemented')

    def merge(self, another):
        """
            Merge 2 types together to a new type

            @param another Type
            @return Type
        """
        raise Exception('Not implemented')

    def to_string(self, shift=0, indent=0):
        """
            Get a human readable string of this type.

            @param shift int: if this type spans to multiple lines, shift the text from the second line to `shift` space.
            @param indent int: indentation for readable purpose.
            @return str
        """
        raise Exception('Not implemented')
