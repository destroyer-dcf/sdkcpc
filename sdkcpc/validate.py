#!/usr/bin/python
import yaml
import re
import os, sys
from cerberus import Validator
import os.path
from os import path
from .common import *
from .info import *
from rich import print
from rich.console import Console
console = Console(width=80,color_system="windows",force_terminal=True)

COMPILATION = {}
GENERAL = {}
CONFIG = {}
RVM = {}
M4 = {}

def conversions_error(error):

    show_info(MAKEFILE+" Validation","white")
    for line in error.splitlines():
        
        # check sections
        if "compilation > required field" in line:
            print("[red bold]\[*] [yellow bold]COMPILATION [red bold]This section not exist.")
        elif "config > required field" in line:
            print("[red bold]\[ERROR][yellow bold] \[config] -> [red bold]This section not exist.")
        elif "general > required field" in line:
            print("[red bold]\[ERROR][yellow bold] \[general] -> [red bold]This section not exist.")
        elif "rvm > required field" in line:
            print("[red bold]\[ERROR][yellow bold] \[rvm] -> [red bold]This section not exist.")
        elif "m4 > required field" in line:
            print("[red bold]\[ERROR][yellow bold] \[m4] -> [red bold]This section not exist.")

        if "build >" in line:
            COMPILATION["build"] = "This key must exist and cannot be blank."
        elif "version >" in line:
            COMPILATION["version"]="This key does not contain version 0.0.0 format."
        elif "name >" in line:
            GENERAL["name"] = "This key must exist and can only have a maximum of 8 characters." 
        elif "description >" in line:
            GENERAL["description"] = "This key must exist."
        elif "template >" in line:
            GENERAL["template"] = "This key must exist. Supported values ​​are: Basic or 8BP."
        elif "authors >" in line:
            GENERAL["authors"] = "This key must exist and cannot be blank."
        elif "concatenate.bas.files >" in line:
            CONFIG["concatenate.bas.files"] = "This key must exist. Supported values ​​are: Yes or No."
        elif "config > name.bas.file >" in line:
            CONFIG["name.bas.file"] ="This key must exist and the value must comply with the 8:3 format, with extension '.bas'."
        elif "model.cpc >" in line:
            RVM["model.cpc"] = "This key must exist. Supported values ​​are: 464,664 or 6128."
        elif "ip >" in line:
            M4["ip"] = "This key must exist and the value must comply with the IP format (0.0.0.0)."
    
    show_specific_key_error ("COMPILATION",COMPILATION)
    show_specific_key_error ("GENERAL",GENERAL)
    show_specific_key_error ("CONFIG",CONFIG)
    show_specific_key_error ("RVM",RVM)
    show_specific_key_error ("M4",M4) 

    
def show_specific_key_error(section,diccionary):
    if len(diccionary) > 0:
        print("[*] [blue bold]"+ section +" [/]")
        for key in diccionary:
            print("[red bold]\[*]   [yellow bold]" + key + ": [red bold]" + diccionary[key])
 
def show_error_validate(error):
    new_error = re.sub('[^a-zA-Z0-9:, \n\.]', '', error)
    new_error = new_error.replace(":", " >")
    new_error = new_error.replace(",", "\n")
    conversions_error(new_error)

def validate_data_project():
    validate_Folder_Project()
    
    schema = eval(open(APP_PATH + "/schema.py", 'r').read())
    v = Validator(schema)
    doc = Get_data_project_dict()

    if not v.validate(doc, schema):
        show_error_validate(str(v.errors))
        show_foot("Validation ERROR","red")
        print()
        sys.exit(1)


    show_head(MAKEFILE + "","white")
    print("[*] [blue bold]COMPILATION [/]")
    print("[*]   compilation: " + project_data["compilation"]["build"]+ " [green bold][OK]")
    print("[*]   version: " + project_data["compilation"]["version"]+ " [green bold][OK]")
    print("[*] [blue bold]GENERAL [/]")
    print("[*]   name: " + project_data["general"]["name"]+ " [green bold][OK]")
    print("[*]   description: " + project_data["general"]["description"]+ " [green bold][OK]")
    print("[*]   template: " + project_data["general"]["template"]+ " [green bold][OK]")
    print("[*]   authors: " + project_data["general"]["authors"]+ " [green bold][OK]")
    print("[*] [blue bold]CONFIG [/]")
    print("[*]   concatenate.bas.files: " + project_data["config"]["concatenate.bas.files"]+ " [green bold][OK]")
    print("[*]   name.bas.file: " + project_data["config"]["name.bas.file"]+ " [green bold][OK]")
    print("[*] [blue bold]RETRO VIRTUAL MACHINE [/]")
    print("[*]   model.cpc: " + project_data["rvm"]["model.cpc"]+ " [green bold][OK]")
    print("[*] [blue bold]M4 BOARD [/]")
    print("[*]   ip: " + project_data["m4"]["ip"] + " [green bold][OK]")
    show_foot(MAKEFILE + " Successfull","green")
    
    if project_data["general"]["template"] == "8BP":
        validate_Project_structure(FOLDER_PROJECT_8BP)
        validate_83(FOLDER_PROJECT_8BP)
    elif project_data["general"]["template"] == "BASIC":
        validate_Project_structure(FOLDER_PROJECT_NEW)
        validate_83(FOLDER_PROJECT_NEW)
    
    
# validate folder is poject
def validate_Folder_Project():
    if not os.path.exists(PWD + MAKEFILE):
        print("\n[red bold]This folder does not contain sdkcpc project.\n")
        sys.exit(1)

# Validamos que existan todas las carpetas del proyecto
#   @Param: array carpetas 
def validate_Project_structure(estructura):
    show_head("Project Structure Validation","white")
    print("[+] [blue bold]FOLDERS [/]")
    for i in estructura:
        if not os.path.isdir(PWD + i):
            print("[red bold][+]   " + i + " : Folder not exist in this project.")
            show_foot("Structure error","red")
            sys.exit(1)
        else:
            print("[+]   " + i + " [green bold][OK]")

    show_foot("Structure Successfull","green")


def validate_83(estructura):
    show_head("Validate 8:3 Files","white")
    for i in estructura:
        print("[+] [blue bold]"+ i + " [/]")
        arr = next(os.walk(PWD + i))[2]
        if len(arr) == 0: print("[+]   No files in folder [yellow bold][WARNING]")
        for x in range(0,len(arr)):
            if len(os.path.splitext(arr[x])[1]) != 4 or len(os.path.splitext(arr[x])[0]) > 8:
                print("[red bold][+]   " + arr[x] + " : does not conform to 8:3 file format.")
                sys.exit(1)
            else:
                print("[+]   " + arr[x]  + " [green bold][OK]")
    show_foot("8:3 Files Successfull","green")