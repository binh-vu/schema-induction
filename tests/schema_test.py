#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import *
from schema.schema import generate_schema
from schema.type import Type


def setup():
    Type.MAX_N_KEEP_VALUE = 0


@raises(AssertionError)
def test_all_records_is_dict():
    schema = generate_schema([
        [],
        {'contacts': {'name': 'Peter'}},
    ])


@raises(AssertionError)
def test_all_records_is_dict_2():
    schema = generate_schema([
        'fdsfds',
        {'contacts': {'name': 'Peter'}},
    ])


@raises(AssertionError)
def test_all_records_is_dict_3():
    schema = generate_schema([
        5,
        {'contacts': {'name': 'Peter'}},
    ])


def test_object():
    schema = generate_schema([{ 'name': 'Peter', 'age': 50 }])
    eq_(schema.to_string(indent=4), '''class(
    age: int,
    name: str
)''')


def test_object_missing_field():
    schema = generate_schema([
        {'name': 'Peter', 'age': 50},
        {'name': 'John'}
    ])
    eq_(schema.to_string(indent=4), '''class(
    [age]: int,
    name: str
)''')


# Union Type
def test_object_union_primitive_field_1():
    schema = generate_schema([
        {'name': 'Peter', 'age': 50},
        {'name': None}
    ])
    eq_(schema.to_string(indent=4), '''class(
    [age]: int,
    name: null|str
)''')


def test_object_union_primitive_field_2():
    schema = generate_schema([
        {'name': 'Peter', 'age': 50},
        {'name': 50, 'age': 5.0}
    ])
    eq_(schema.to_string(indent=4), '''class(
    age: float,
    name: str|int
)''')


def test_object_union_list_class_field():
    schema = generate_schema([
        {'name': u'Peter', 'contacts': ['John', 'Marry']},
        {'contacts': {'name': 'Peter'}}
    ])
    eq_(schema.to_string(indent=4), '''class(
    [name]: unicode,
    contacts: union(
        class(
            name: str
        ),
        list[2](str)
    )
)''')


def test_object_union_list_class_field_2():
    schema = generate_schema([
        {'name': u'Peter', 'contacts': ['John', 'Marry']},
        {'contacts': {'name': 'Peter'}},
        {'contacts': 5},
        {'contacts': {'age': 50}},
    ])
    eq_(schema.to_string(indent=4), '''class(
    [name]: unicode,
    contacts: union(
        int,
        class(
            [age]: int,
            [name]: str
        ),
        list[2](str)
    )
)''')


# list type
def test_object_list_field_1():
    schema = generate_schema([
        {'name': u'Peter', 'contacts': ['John', 'Marry']},
        {'contacts': ['Peter']},
        {'contacts': []}
    ])
    eq_(schema.to_string(indent=4), '''class(
    [name]: unicode,
    contacts: list(str)
)''')


def test_object_list_field_2():
    schema = generate_schema([
        {'name': u'Peter', 'contacts': [{'name': 'John'}, {'name': 'Marry'}]},
        {'contacts': [{'name': 'Peter'}]}
    ])
    eq_(schema.to_string(indent=4), '''class(
    [name]: unicode,
    contacts: list[1,2](
        class(
            name: str
        )
    )
)''')


def test_object_list_field_3():
    Type.MAX_N_KEEP_VALUE = 4
    schema = generate_schema([
        {'name': u'Peter', 'contacts': ['John']},
        {'contacts': ['Peter']},
        {'contacts': ['Marry']},
        {'contacts': []},
    ])
    eq_(schema.to_string(indent=4), '''class(
    [name]: unicode{Peter},
    contacts: list[0,1](str{Marry,John,Peter})
)''')
    Type.MAX_N_KEEP_VALUE = 0


def test_object_list_field_4():
    schema = generate_schema([
        {'name': u'Peter', 'contacts': ['John']},
        {'contacts': ['Peter']}
    ])
    eq_(schema.to_string(indent=4), '''class(
    [name]: unicode,
    contacts: list[1](str)
)''')


def test_object_list_union_field():
    schema = generate_schema([
        {'name': u'Peter', 'contacts': ['John', 'Marry']},
        {'contacts': [{'name': 'Peter'}]}
    ])
    eq_(schema.to_string(indent=4), '''class(
    [name]: unicode,
    contacts: list[1,2](
        union(
            str,
            class(
                name: str
            )
        )
    )
)''')