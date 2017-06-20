#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import *
from json_schema.schema import generate_schema
from json_schema.primitive_type import PrimitiveType


def setup():
    PrimitiveType.MAX_N_KEEP_VALUE = 2


def test_to_string():
    schema = generate_schema([{ 'name': 'Peter' }, { 'name': 'John' }])
    eq_(schema.to_string(indent=4), '''class(
    name: str
)''')


def test_to_string_ascii():
    schema = generate_schema([{ 'name': 'Peter' }])
    eq_(schema.to_string(indent=4), '''class(
    name: str{"Peter"}
)''')


def test_to_string_utf8():
    schema = generate_schema([{ 'name': u'Péter' }])
    eq_(schema.to_string(indent=4), u'''class(
    name: str{"Péter"}
)''')
