#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import *
from json_schema.schema import generate_schema
from json_schema.primitive_type import PrimitiveType
from json_schema.list_type import ListType


def setup():
    PrimitiveType.MAX_N_KEEP_VALUE = 0
    ListType.MAX_N_KEEP_VALUE = 3


def test_empty_object():
    schema = generate_schema([{}])
    eq_(schema.to_string(indent=4), '''class()''')


def test_object():
    schema = generate_schema([{ 'name': 'Peter', 'age': 50 }])
    eq_(schema.to_string(indent=4), '''class(
    name: str,
    age: int
)''')


def test_list():
    schema = generate_schema([[{'name': 'Peter', 'age': 50}]])
    eq_(schema.to_string(indent=4), '''list[1](
    class(
        name: str,
        age: int
    )
)''')


def test_object_missing_field():
    schema = generate_schema([
        {'name': 'Peter', 'age': 50},
        {'name': 'John'}
    ])
    eq_(schema.to_string(indent=4), '''class(
    name: str,
    [age]: int
)''')


# Union Type
def test_object_union_primitive_field_1():
    schema = generate_schema([
        {'name': 'Peter', 'age': 50},
        {'name': None}
    ])
    eq_(schema.to_string(indent=4), '''class(
    name: null|str,
    [age]: int
)''')


def test_object_union_primitive_field_2():
    schema = generate_schema([
        {'name': 'Peter', 'age': 50},
        {'name': 50, 'age': 5.0}
    ])
    eq_(schema.to_string(indent=4), '''class(
    name: str|int,
    age: float
)''')


def test_object_union_list_class_field():
    schema = generate_schema([
        {'name': u'Peter', 'contacts': ['John', 'Marry']},
        {'contacts': {'name': 'Peter'}}
    ])
    eq_(schema.to_string(indent=4), '''class(
    [name]: str,
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
    [name]: str,
    contacts: union(
        int,
        class(
            [name]: str,
            [age]: int
        ),
        list[2](str)
    )
)''')


def test_list_and_object():
    schema = generate_schema([
        {'name': 'Peter', 'age': 50},
        [
            {'ref': 5}
        ]
    ])
    eq_(schema.to_string(indent=4), '''union(
    class(
        name: str,
        age: int
    ),
    list[1](
        class(
            ref: int
        )
    )
)''')


def test_list_and_object_2():
    schema = generate_schema([
        {'name': 'Peter', 'age': 50},
        [
            {'ref': 5}
        ],
        [
            'address', 'phone', 'name'
        ],
        5,
        {'contacts': ['John']}
    ])
    eq_(schema.to_string(indent=4), '''union(
    int,
    class(
        [name]: str,
        [age]: int,
        [contacts]: list[1](str)
    ),
    list[1,3](
        union(
            str,
            class(
                ref: int
            )
        )
    )
)''')


def test_list_and_object_3():
    schema = generate_schema([
        {'name': 'Peter', 'age': 50},
        [
            {'ref': 5}
        ],
        [
            'address', 'phone', 'name'
        ],
        5,
        {'contacts': ['John']},
        None
    ])
    eq_(schema.to_string(indent=4), '''union(
    null,
    int,
    class(
        [name]: str,
        [age]: int,
        [contacts]: list[1](str)
    ),
    list[1,3](
        union(
            str,
            class(
                ref: int
            )
        )
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
    [name]: str,
    contacts: list(str)
)''')


def test_object_list_field_2():
    schema = generate_schema([
        {'name': u'Peter', 'contacts': [{'name': 'John'}, {'name': 'Marry'}]},
        {'contacts': [{'name': 'Peter'}]}
    ])
    eq_(schema.to_string(indent=4), '''class(
    [name]: str,
    contacts: list[1,2](
        class(
            name: str
        )
    )
)''')


def test_object_list_field_3():
    PrimitiveType.MAX_N_KEEP_VALUE = 4
    schema = generate_schema([
        {'name': u'Péter', 'contacts': ['John']},
        {'contacts': [u'Péter']},
        {'contacts': ['Marry']},
        {'contacts': []},
    ])
    eq_(schema.to_string(indent=4), u'''class(
    [name]: str{"Péter"},
    contacts: list[0,1](str{"Marry","John","Péter"})
)''')
    PrimitiveType.MAX_N_KEEP_VALUE = 0


def test_object_list_field_4():
    schema = generate_schema([
        {'name': u'Peter', 'contacts': ['John']},
        {'contacts': ['Peter']}
    ])
    eq_(schema.to_string(indent=4), '''class(
    [name]: str,
    contacts: list[1](str)
)''')


def test_object_empty_list():
    schema = generate_schema([
        {'name': u'Peter', 'contacts': []}
    ])
    eq_(schema.to_string(indent=4), '''class(
    name: str,
    contacts: list[0]()
)''')


def test_object_list_union_field():
    schema = generate_schema([
        {'name': u'Péter', 'contacts': ['John', 'Marry']},
        {'contacts': [{'name': 'Peter'}]}
    ])
    eq_(schema.to_string(indent=4), '''class(
    [name]: str,
    contacts: list[1,2](
        union(
            str,
            class(
                name: str
            )
        )
    )
)''')


def test_utf8():
    PrimitiveType.MAX_N_KEEP_VALUE = 7
    schema = generate_schema([{
        '@id': u'http://en.wikipedia.org/wiki/L\u2019amour_de_loin',
        '@type': [u'http://xmlns.com/foaf/0.1/Document'],
        'http://purl.org/dc/elements/1.1/language': [{u'@value': u'en'}],
        'http://xmlns.com/foaf/0.1/primaryTopic': [{u'@id': u'http://dbpedia.org/resource/L\u2019amour_de_loin'}]
    }])

    eq_(schema.to_string(indent=4), u'''class(
    @id: str{"http://en.wikipedia.org/wiki/L\u2019amour_de_loin"},
    @type: list[1](str{"http://xmlns.com/foaf/0.1/Document"}),
    http://purl.org/dc/elements/1.1/language: list[1](
        class(
            @value: str{"en"}
        )
    ),
    http://xmlns.com/foaf/0.1/primaryTopic: list[1](
        class(
            @id: str{"http://dbpedia.org/resource/L\u2019amour_de_loin"}
        )
    )
)''')
    PrimitiveType.MAX_N_KEEP_VALUE = 0
