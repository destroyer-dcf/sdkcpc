#!/usr/bin/python
import yaml
import re
import os, sys
from cerberus import Validator
import os.path
from os import path
from .common import *
from rich import print
from rich.console import Console
console = Console(width=80,color_system="windows",force_terminal=True)


def show_error_validate(error):
    new_error = re.sub('[^a-zA-Z0-9:, \n\.]', '', error)
    new_error = new_error.replace(":", " >")
    new_error = new_error.replace(",", "\n")
    print ("[red bold]\nValidation "+ MAKEFILE +" Error:\n " + new_error)

def load_doc_project():
    validate_Folder_Project()
    with open(PWD + "/" + MAKEFILE, 'r') as stream:
        try:
            return yaml.full_load(stream)
        except yaml.YAMLError as exception:
            raise exception

def validate_data():
    # schema = eval(open('./schema.py', 'r').read())
    schema = eval(open(APP_PATH + "/schema.py", 'r').read())
    v = Validator(schema)
    doc = load_doc_project() 

    if not v.validate(doc, schema):
        show_error_validate(str(v.errors))
        sys.exit(1)

# Valida si la carpeta es de proyecto
def validate_Folder_Project():
    if not os.path.exists(PWD + MAKEFILE):
        print("][red bold] This folder does not contain sdkcpc project.")
        sys.exit(1)