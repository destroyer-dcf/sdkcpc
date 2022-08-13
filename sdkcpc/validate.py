#!/usr/bin/python
import yaml
import re
import os, sys
from cerberus import Validator

PWD                = os.getcwd() + "/"
MAKEFILE           = "Project.yaml"
# CONFIG             = loadConfigData()
FOLDER_PROJECT_NEW = ["OUT","ASCII","BIN","BASIC","OBJ"] 
FOLDER_PROJECT_8BP = ["ASM","DSK","MUSIC","OUTPUT_SPEDIT","OUT","ASCII","BIN","BASIC","OBJ"] 


def show_error_validate(error):
    new_error = re.sub('[^a-zA-Z0-9:, \n\.]', '', error)
    new_error = new_error.replace(":", " >")
    new_error = new_error.replace(",", "\n")
    print ("ERROR List:\n " + new_error)

def load_doc_project():
    with open('./project.yaml', 'r') as stream:
        try:
            return yaml.full_load(stream)
        except yaml.YAMLError as exception:
            raise exception

def validate_data():
    schema = eval(open('./schema.py', 'r').read())
    v = Validator(schema)
    doc = load_doc_project() 

    if not v.validate(doc, schema):
        show_error_validate(str(v.errors))
        sys.exit(1)
