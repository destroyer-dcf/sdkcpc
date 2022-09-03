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

           

    # print("[*] [blue bold]COMPILATION [/]------------------------------------------------------------")
    # print("[*] - compilation: " + errors["compilation"]["build"])
    # print("[*] - version: " + errors["compilation"]["version"])
    # print("[*] [blue bold]GENERAL [/]----------------------------------------------------------------")
    # print("[*] - name: " + errors["general"]["name"])
    # print("[*] - description: " + errors["general"]["description"])
    # print("[*] - template: " + errors["general"]["template"])
    # print("[*] - authors: " + errors["general"]["authors"])
    # print("[*] [blue bold]CONFIG [/]-----------------------------------------------------------------")
    # print("[*] - concatenate.bas.files: " + errors["config"]["concatenate.bas.files"])
    # print("[*] - name.bas.file: " + errors["config"]["name.bas.file"])
    # print("[*] [blue bold]RETRO VIRTUAL MACHINE [/]--------------------------------------------------")
    # print("[*] - model.cpc: " + errors["rvm"]["model.cpc"])
    # print("[*] [blue bold]M4 BOARD [/]---------------------------------------------------------------")
    # print("[*] - ip: " + errors["m4"]["ip"])
    # print(" ")            
    # for line in error.splitlines():
    #     if "build >" in line:
    #         print("[red bold]\[ERROR][yellow bold] compilation -> build = [red bold]This key must exist and cannot be blank.")
    #     elif "version >" in error:
    #         print("[red bold]\[ERROR][yellow bold] compilation -> version = [red bold]This key does not contain version 0.0.0 format.")
    #     elif "name >" in error:
    #         print("[red bold]\[ERROR][yellow bold] general -> name = [red bold]This field must exist and can only have a maximum of 8 characters.") 
    #     elif "description >" in error:
    #         print("[red bold]\[ERROR][yellow bold] general -> description = [red bold]This key must exist.")
    #     elif "template >" in error:
    #         print("[red bold]\[ERROR][yellow bold] general -> template = [red bold]This key must exist. Supported values ​​are: Basic or 8BP.")
    #     elif "authors >" in error:
    #         print("[red bold]\[ERROR][yellow bold] general -> authors = [red bold]This key must exist and cannot be blank.")
    #     elif "concatenate.bas.files >" in error:
    #         print("[red bold]\[ERROR][yellow bold] config -> concatenate.bas.files = [red bold]This key must exist. Supported values ​​are: Yes or No.")
    #     elif "config > name.bas.file >" in error:
    #         print("[red bold]\[ERROR][yellow bold] config -> name.bas.file = [red bold]This field must exist and the value must comply with the 8:3 format, with extension '.bas'.")
    #     elif "model.cpc >" in error:
    #         print("[red bold]\[ERROR][yellow bold] rvm -> model.cpc = [red bold]This key must exist. Supported values ​​are: 464,664 or 6128.")
    #     elif "ip >" in error:
    #         print("[red bold]\[ERROR][yellow bold] m4 -> ip = [red bold]This field must exist and the value must comply with the IP format (0.0.0.0).")
    #     # check sections
    #     elif "compilation > required field" in error:
    #         print("[red bold]\[ERROR][yellow bold] \[compilation] -> [red bold]This section not exist.")
    #     elif "config > required field" in error:
    #         print("[red bold]\[ERROR][yellow bold] \[config] -> [red bold]This section not exist.")
    #     elif "general > required field" in error:
    #         print("[red bold]\[ERROR][yellow bold] \[general] -> [red bold]This section not exist.")
    #     elif "rvm > required field" in error:
    #         print("[red bold]\[ERROR][yellow bold] \[rvm] -> [red bold]This section not exist.")
    #     elif "m4 > required field" in error:
    #         print("[red bold]\[ERROR][yellow bold] \[m4] -> [red bold]This section not exist.")


            
def show_error_validate(error):
    new_error = re.sub('[^a-zA-Z0-9:, \n\.]', '', error)
    new_error = new_error.replace(":", " >")
    new_error = new_error.replace(",", "\n")
    conversions_error(new_error)

    # print ("[red bold]\nValidation " + MAKEFILE + " Error:\n " + new_error)


def validate_data_project():
    validate_Folder_Project()
    validate_Project_structure()
    schema = eval(open(APP_PATH + "/schema.py", 'r').read())
    v = Validator(schema)
    doc = Get_data_project_dict()

    if not v.validate(doc, schema):
        show_error_validate(str(v.errors))
        show_foot("Validation ERROR","red")
        print()
        sys.exit(1)


    show_head("PROJECT.CFG VALIDATION","white")
    # print("[*] ------------------------------------------------------------------------")
    print("[green bold][OK][/] [blue bold]COMPILATION [/]")
    print("[green bold][OK][/]   compilation: " + project_data["compilation"]["build"])
    print("[green bold][OK][/]   version: " + project_data["compilation"]["version"])
    print("[green bold][OK][/] [blue bold]GENERAL [/]")
    print("[green bold][OK][/]   name: " + project_data["general"]["name"])
    print("[green bold][OK][/]   description: " + project_data["general"]["description"])
    print("[green bold][OK][/]   template: " + project_data["general"]["template"])
    print("[green bold][OK][/]   authors: " + project_data["general"]["authors"])
    print("[green bold][OK][/] [blue bold]CONFIG [/]")
    print("[green bold][OK][/]   concatenate.bas.files: " + project_data["config"]["concatenate.bas.files"])
    print("[green bold][OK][/]   name.bas.file: " + project_data["config"]["name.bas.file"])
    print("[green bold][OK][/] [blue bold]RETRO VIRTUAL MACHINE [/]")
    print("[green bold][OK][/]   model.cpc: " + project_data["rvm"]["model.cpc"])
    print("[green bold][OK][/] [blue bold]M4 BOARD [/]")
    print("[green bold][OK][/]   ip: " + project_data["m4"]["ip"])
    show_foot("Validation Successfull","green")
    
    
    
# validate folder is poject
def validate_Folder_Project():
    if not os.path.exists(PWD + MAKEFILE):
        print("\n[red bold]This folder does not contain sdkcpc project.\n")
        sys.exit(1)

# Get data project in dict
def Get_data_project_dict():
    config = ConfigParser()
    config.read("/home/destroyer/Documentos/Github/sdkcpc/pepep/Project.cfg")
    project_dic = dict(config._sections)
    return project_dic

# Validamos que existan todas las carpetas del proyecto
#   @Param: array carpetas 
def validate_Project_structure():
    estructura = FOLDER_PROJECT_8BP
    for i in estructura:
        if not os.path.isdir(PWD + i):
            print("\n[red bold]" + i + " Folder not exist in this project.\n")
            sys.exit(1)


# Validamos formato 8:3 en todos los archivos del proyecto
# @Param Array de carpetas (Basic/8BP)
def validate83FilesinFolders(Folder):
    busca = Folder
    for y in range(0,len(busca)):
        if os.path.exists(PWD + busca[y]):
            arr = next(os.walk(PWD + busca[y]))[2]
            for x in range(0,len(arr)):
                if len(os.path.splitext(arr[x])[1]) != 4 or len(os.path.splitext(arr[x])[0]) > 8:
                    print("El archivo " + arr[x] + " does not conform to 8:3 format.")
                    print("[blue bold]\["+busca[y]+"] \[red bold]El archivo " + arr[x] + " does not conform to 8:3 format.")
                    exit(1)