#!/usr/bin/python
# -*- coding: utf-8 -*-

from .type import Type


class UnionType(Type):

    PrimitiveType = None # type: schema.primitive_type.PrimitiveType
    NoneType = None # type: schema.primitive_type.NoneType
    ListType = None # type: schema.list_type.ListType
    ClassType = None # type: schema.class_type.ClassType

    def __init__(self):
        self.none_type = None # type: schema.primitive_type.NoneType
        self.primitive_types = [] # type: List[schema.primitive_type.PrimitiveType]
        self.list_type = None
        self.class_type = None

    def optimize(self):
        nhas_prim = len(self.primitive_types) == 0
        nhas_none = self.none_type is None
        nhas_list = self.list_type is None
        nhas_clas = self.class_type is None

        if not nhas_list:
            self.list_type = self.list_type.optimize()

        if not nhas_clas:
            self.class_type = self.class_type.optimize()

        if not nhas_none and nhas_prim and nhas_list and nhas_clas:
            return self.none_type

        if nhas_none and len(self.primitive_types) == 1 and nhas_list and nhas_clas:
            return self.primitive_types[0]

        if nhas_none and nhas_prim and not nhas_list and nhas_clas:
            return self.list_type

        if nhas_none and nhas_prim and nhas_list and not nhas_clas:
            return self.class_type

        return self

    def add(self, type):
        if type is None:
            return self

        if isinstance(type, UnionType.PrimitiveType):
            for i, ptype in enumerate(self.primitive_types):
                if ptype.is_mergeable(type):
                    self.primitive_types[i] = ptype.merge(type)
                    return self

            self.primitive_types.append(type)
            return self

        if isinstance(type, UnionType.NoneType):
            self.none_type = type
            return self

        if isinstance(type, UnionType.ListType):
            if self.list_type is None:
                self.list_type = type
            else:
                self.list_type = self.list_type.merge(type)
            return self

        if isinstance(type, UnionType.ClassType):
            if self.class_type is None:
                self.class_type = type
            else:
                self.class_type = self.class_type.merge(type)
            return self

        assert isinstance(type, UnionType)
        return self.merge(type)

    def merge(self, another):
        if isinstance(another, UnionType):
            self.add(another.none_type)
            for ptype in another.primitive_types:
                self.add(ptype)
            self.add(another.list_type)
            self.add(another.class_type)
            return self

        # merge another type to union type is adding
        return self.add(another)

    def to_string(self, shift=0, indent=0):
        prefix_space = ' ' * shift
        indent_space = ' ' * indent

        types = []

        if self.none_type is not None:
            types.append(self.none_type.to_string())

        if len(self.primitive_types) > 0:
            types += [ptype.to_string() for ptype in self.primitive_types]

        if self.class_type is not None:
            types.append(self.class_type.to_string(shift + indent, indent))
        if self.list_type is not None:
            types.append(self.list_type.to_string(shift + indent, indent))

        # heuristic rules to determine if we could use shorthand for this union class (readability)
        # if only primitive or none type, then use shorthand
        if self.class_type is None and self.list_type is None:
            return '|'.join(types)

        # full rendering
        text = ',\n'.join([prefix_space + indent_space + x for x in types])
        return 'union(\n' + text + '\n' + prefix_space + ')'