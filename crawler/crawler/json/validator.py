import json
import os

from fastjsonschema import compile

base_path = os.path.dirname(__file__)
schema_path = os.path.join(base_path, 'schema.json')

with open(schema_path) as file:
    schema_file = json.load(file)

validate = compile(schema_file)
