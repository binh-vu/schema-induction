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