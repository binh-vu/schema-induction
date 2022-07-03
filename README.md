Inducing schema of list of JSON/dictionary objects

# Installation

```bash
pip install schema_induction
```

# Usages

```python
from schema_induction import generate_schema

# list of objects that you wish to find their schema
records = []
print(generate_schema(records))
```

# Examples

1. List of objects with optional fields

```python
>>> schema = generate_schema([
        {'name': 'Peter', 'age': 50},
        {'name': 'John'}
    ])
>>> print(schema.to_string(indent=4))
class(
    name: str,
    [age]: int
)
```

2. Union types with nested dictionaries, list, etc.

```python
>>> schema = generate_schema([
        {'name': u'Peter', 'contacts': ['John', 'Marry']},
        {'contacts': {'name': 'Peter'}},
        {'contacts': 5},
        {'contacts': {'age': 50}},
    ])
>>> print(schema.to_string(indent=4))
class(
[name]: str,
contacts: union(
    int,
    class(
        [name]: str,
        [age]: int
    ),
    list[2](str)
)
```

3. Detecting enum

```python
>>> PrimitiveType.MAX_N_KEEP_VALUE = 4
>>> schema = generate_schema([
        {'name': u'Péter', 'contacts': ['John']},
        {'contacts': [u'Péter']},
        {'contacts': ['Marry']},
        {'contacts': []},
    ])
>>> print(schema.to_string(indent=4))
class(
    [name]: str{"Péter"},
    contacts: list[0,1](str{"Marry","John","Péter"})
)
```

More examples: [schema_test.py](https://github.com/binh-vu/schema-induction/blob/master/tests/schema_test.py)
