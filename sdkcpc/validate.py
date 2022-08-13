#!/usr/bin/python
import yaml
from cerberus import Validator


def load_doc_project():
    with open('./project.yaml', 'r') as stream:
        try:
            return yaml.full_load(stream)
        except yaml.YAMLError as exception:
            raise exception

schema = eval(open('./schema.py', 'r').read())
v = Validator(schema)
doc = load_doc_project() 
if not v.validate(doc, schema):
    x = str(v.errors).replace("{", "")
    x = x.replace("}", "")
    x = x.replace("[", "")
    x = x.replace("]", "")
    x = x.replace("'", "")
    x = x.replace(":", " >")
    print("ERROR: "+ x)