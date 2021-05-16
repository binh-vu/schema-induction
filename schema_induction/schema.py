#!/usr/bin/python
# -*- coding: utf-8 -*-

from schema_induction.class_type import ClassType
from schema_induction.list_type import ListType
from schema_induction.primitive_type import PrimitiveType, NoneType
from schema_induction.union_type import UnionType

# DO injection here
UnionType.PrimitiveType = PrimitiveType
UnionType.NoneType = NoneType
UnionType.ListType = ListType
UnionType.ClassType = ClassType


def guess_type(instance):
    if instance is None:
        return NoneType
    if type(instance) is dict:
        return ClassType
    if type(instance) is list:
        return ListType
    return PrimitiveType


def alter_type(instance, instance_type):
    """
        :param instance:
        :param instance_type: ClassType | ListType
        :return: Type
    """
    # guess type of current instance, if it's different to the provided type
    # then the return type would be the union type
    InstanceType = guess_type(instance)

    if InstanceType != instance_type.__class__:
        new_type = alter_type(instance, InstanceType())
        if isinstance(instance_type, UnionType):
            instance_type.add(new_type)
            return instance_type

        return UnionType().add(instance_type).add(new_type)

    if InstanceType == ClassType:
        # create type for each property in $instance, if property doesn't
        # exist in $instance_type, add it to $instance_type, otherwise merge it
        for prop, value in instance.items():
            PropType = guess_type(value)
            if PropType == ClassType:
                prop_type = alter_type(value, ClassType())
            elif PropType == ListType:
                prop_type = alter_type(value, ListType())
            elif PropType == PrimitiveType:
                prop_type = PrimitiveType(type(value).__name__).add_value(value)
            else:
                # PropType is NoneType
                prop_type = NoneType()

            if prop not in instance_type:
                instance_type[prop] = prop_type
            else:
                instance_type[prop] = instance_type[prop].merge(prop_type)

        # for property appear in $type but in $instance
        # assign the "missing" property to this property
        for prop in instance_type:
            if prop not in instance:
                instance_type.add_missing_prop(prop)
    elif InstanceType == ListType:
        # guess all possible value's type in list,
        # so it would be very slow if we have a long list
        instance_type.set_size(len(instance))

        for value in instance:
            PropType = guess_type(value)
            if PropType == ClassType:
                prop_type = alter_type(value, ClassType())
            elif PropType == ListType:
                prop_type = alter_type(value, ListType())
            elif PropType == PrimitiveType:
                prop_type = PrimitiveType(type(value).__name__).add_value(value)
            else:
                # PropType is NoneType
                prop_type = NoneType()

            instance_type.add(prop_type)
    elif InstanceType == NoneType:
        return instance_type
    else:
        assert InstanceType == PrimitiveType
        instance_type = instance_type \
            .set_type(type(instance).__name__) \
            .add_value(instance)

    return instance_type


def generate_schema(objects, max_n_examples: int=7):
    """
        Generate schema from list of dict_objects

        :param objects: list<dict_object>
        :return: Type
    """
    PrimitiveType.MAX_N_KEEP_VALUE = max_n_examples

    schema = None
    for object in objects:
        if schema is None:
            schema = guess_type(object)()
        schema = alter_type(object, schema)

    if schema is not None:
        return schema.optimize()
    return schema


if __name__ == '__main__':
    data = [
        {'haha': 5},
        {'haha': 1}
    ]

    print(generate_schema(data).to_string(indent=4))
