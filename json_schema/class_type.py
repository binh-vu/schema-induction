#!/usr/bin/python
# -*- coding: utf-8 -*-

from .type import Type
from .union_type import UnionType


class ClassType(Type):
    """
        Represent dictionary, class or object which could be accessed using string key
    """

    def __init__(self):
        self.props = {}
        self.missing_props = set()

    def get_props(self):
        """
            Get set of property names
            :return: set<str>
        """
        return set(self.props.keys())

    def __contains__(self, key):
        return key in self.props

    def __getitem__(self, key):
        return self.props[key]

    def __setitem__(self, key, value):
        self.props[key] = value

    def __iter__(self):
        return iter(self.props.keys())

    def add_missing_prop(self, prop):
        self.missing_props.add(prop)

    def optimize(self):
        """
            @inherit
        """
        for prop, prop_type in self.props.items():
            self.props[prop] = prop_type.optimize()
        return self

    def merge(self, another):
        if isinstance(another, ClassType):
            for prop_name, prop_type in another.props.items():
                if prop_name not in self.props:
                    self.props[prop_name] = prop_type
                    # prop_name is a missing prop because it's in another but not in self
                    self.missing_props.add(prop_name)
                else:
                    self.props[prop_name] = self.props[prop_name].merge(prop_type)

            # for property appear in another but in self
            # assign missing property to this property
            for prop_name in self.props.keys():
                if prop_name not in another:
                    self.missing_props.add(prop_name)

            self.missing_props = self.missing_props.union(another.missing_props)
            return self

        return UnionType().add(self).add(another)

    def to_string(self, shift=0, indent=0):
        prefix_space = ' ' * shift
        indent_space = ' ' * indent

        props = []
        for s, value in self.props.items():
            if s in self.missing_props:
                props.append('[%s]: %s' % (s, value.to_string(shift + indent, indent)))
            else:
                props.append('%s: %s' % (s, value.to_string(shift + indent, indent)))

        props = [prefix_space + indent_space + x for x in props]

        if len(props) == 0:
            return 'class()'

        text = ',\n'.join(props)
        return 'class(\n' + text + '\n' + prefix_space + ')'
