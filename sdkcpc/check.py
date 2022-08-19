#!/usr/bin/python
from itertools import count
import sys
import os
import os.path
import ipaddress

from rich import print
from rich.panel import Panel
from os.path import exists
from tabulate import tabulate
from datetime import datetime

from .config import *
from .common import *
from .new import *
from rich.console import Console
console = Console(width=80,color_system="windows",force_terminal=True)

# Chequeamos si la estructura y el archivo makefile
# contienen errores.
def checkProject():
    validateGeneralSection(readProyectSection("general"))
    # Chequeamos que la carpeta sea un proyecto sdkcpc
    validateFolderProject()
    # Chequeamos que la carpeta que la carpeta contenga la estructura del proyecto sdkcpc
    if readProyectKey("general","template").upper() == "BASIC":
        validateStructureProject(FOLDER_PROJECT_NEW)
        # Validamos que los archivos cumplan con 8:3
        validate83FilesinFolders(FOLDER_PROJECT_NEW)
    elif readProyectKey("general","template").upper() == "8BP":
        validateStructureProject(FOLDER_PROJECT_8BP)
        # Validamos que los archivos cumplan con 8:3
        validate83FilesinFolders(FOLDER_PROJECT_8BP)
    else:
       print("[blue bold]["+MAKEFILE+"][red bold]\[general]:template [bold red]key value is not correct. Correct values [green bold][Basic,8BP]")
       sys.exit(1)
    # Validamos que el modelo de cpc sea correcto.
    validateModelCpc("rvm")
    # Validamos el nombre de proyecto
    validateName(readProyectKey("general","name"))
    # validamos la seccion CONFIG
    validateConfigSection(readProyectSection("config"))
    # Validamos que la key IP sea correcta
    IP = readProyectKey("m4","ip")
    if not validateIp(IP):
        print("[blue bold]["+MAKEFILE+"][red bold]\[m4]:ip = [red bold]"+ IP + " --> value is not correct.")
        sys.exit(1)
    # Validamos formato de version
    version = readProyectKey("compilation","version")
    if validateVersion(version) < 3:
        print("[blue bold]["+MAKEFILE+"][red bold]\[compilation]:version = [red bold]"+ version + " --> The version format is not correct. Correct Value [green bold]0.0.0")
        sys.exit(1)        
    # print(readProyectSection("general"))
    # print(readProyectSection("config"))
    print("Validate Project Successfully")


# Valida que la version tenga el formato correcto 0.0.0
def validateVersion(version):
    lst = version.split(".")
    return len(lst)

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


# Validamos la seccion Config
# @Param Array de keys de la seccion
def validateGeneralSection(data):
    # comprobamos que existan todas las keys
    if not "name" in data:
        print("[blue bold]\["+MAKEFILE+"][red bold] name key not exist")
        sys.exit(1)
    if not "description" in data:
        print("[blue bold]\["+MAKEFILE+"][red bold] description key not exist")
        sys.exit(1)
    if not "template" in data:
        print("[blue bold]["+MAKEFILE+"][red bold] template key not exist")
        sys.exit(1)
    if not "authors" in data:
        print("[blue bold]["+MAKEFILE+"][red bold] authors key not exist")
        sys.exit(1)

# Validamos la seccion Config
# @Param Array de keys de la seccion
def validateConfigSection(data):
    # comprobamos que existan todas las keys
    if not "validate.83.files" in data:
        print("[blue bold]["+MAKEFILE+"][red bold] validate.83.files key not exist")
        sys.exit(1)
    if not "concatenate.files" in data:
        print("[blue bold]["+MAKEFILE+"][red bold] concatenate.files key not exist")
        sys.exit(1)
    if not "name.bas.file" in data:
        print("[blue bold]["+MAKEFILE+"][red bold] name.bas.file key not exist")
        sys.exit(1)
    if not "name.dsk.file" in data:
        print("[blue bold]["+MAKEFILE+"][red bold] name.dsk.file key not exist")
        sys.exit(1)

    # Validamos si el dato es correcto
    while data["concatenate.files"].upper() not in ["YES","NO"]:
        print("[blue bold]["+MAKEFILE+"][red bold] concatenate.files = "+ data["concatenate.files"] + " value is not correct. Correct values [green bold][Yes,No]")
        sys.exit(1)
    # Validamos si el dato es correcto
    while data["validate.83.files"].upper() not in ["YES","NO"]:
        print("[blue bold]["+MAKEFILE+"][bold red] validate.83.files = "+ data["validate.83.files"] + " value is not correct. Correct values [green bold][Yes,No]")
        sys.exit(1)
    # Validamos si el dato contiene espacios
    if data["name.bas.file"].find(' ') != -1:
        print("[blue bold]["+MAKEFILE+"][red bold] name.bas.file = "+ data["name.bas.file"] + " value is not correct. The name contain spaces")
        sys.exit(1)
    if exists(PWD + "BASIC/"+data["name.bas.file"]) == False:
        print ("[red bold][["+MAKEFILE+"] BASIC/"+data["name.bas.file"] +" not exist.")
        sys.exit(1)

    # Validamos si el dato contiene espacios
    if data["name.dsk.file"].find(' ') != -1:
        print("[yellow]["+MAKEFILE+"][red bold] name.bas.file = "+ data["name.dsk.file"] + " value is not correct. The name contain spaces")
        sys.exit(1)
    # Si activado formato 8:3 comprobamos que se cumpla en name.bas.file/name.dsk.file
    if data["validate.83.files"].upper() == "YES":
        if len(os.path.splitext(data["name.bas.file"])[1]) != 4:
            print("[blue bold]["+MAKEFILE+"][bold red] name.bas.file = "+data["name.dsk.file"]+" File extension must have 3 characters!")
            sys.exit(1)
        if os.path.splitext(data["name.bas.file"])[1].lower() != ".bas":
            print("[blue bold]["+MAKEFILE+"][red bold] name.bas.file = "+data["name.dsk.file"]+" File extension must have 3 characters!")
            sys.exit(1)
        if len(os.path.splitext(data["name.bas.file"])[0]) > 8:
            print("[blue bold]["+MAKEFILE+"][red bold] name.bas.file = "+data["name.dsk.file"]+" File name cannot be longer than 8 characters!")
            sys.exit(1)
        if len(os.path.splitext(data["name.dsk.file"])[1]) != 4:
            print("[blue bold]["+MAKEFILE+"][red bold] name.dsk.file = "+data["name.dsk.file"]+" File extension must have 3 characters!")
            sys.exit(1)
        if os.path.splitext(data["name.dsk.file"])[1].lower() != ".dsk":
            print("[blue bold]["+MAKEFILE+"][red bold] name.dsk.file = "+data["name.dsk.file"]+" File extension must have 3 characters!")
            sys.exit(1)
        if len(os.path.splitext(data["name.dsk.file"])[0]) > 8:
            print("[blue bold]["+MAKEFILE+"][red bold] name.dsk.file = "+data["name.dsk.file"]+" File name cannot be longer than 8 characters!")
            sys.exit(1)

# Validamos que existan todas las carpetas del proyecto
#   @Param: array carpetas 
def validateStructureProject(Folders):
    for x in range(0,len(Folders)):
        if not path.exists(PWD + Folders[x]):
            print("[blue bold]\["+Folders[x]+"][red bold]The folder does not exist in the project")

# Valida que el modelo de cpc sea correcto
#   @Param: seccion
def validateModelCpc(section):
    val = readProyectKey(section,"model.cpc")
    if val not in MODELS_CPC: 
        print("[blue bold]\["+MAKEFILE+"][red bold] model.cpc = "+ val + " value is not correct. Correct values [green bold][464,664,6128]")
        sys.exit(1)

# Valida que el nombre de proyecto no este vacio
#   @Param: nombre proyecto
def validateName(name):
    if name == "": 
        print("[blue bold]\["+MAKEFILE+"][red bold] name key value cannot be empty.")
        sys.exit(1)

# Validate IP addrees
#   @Param IP
def validateIp(ip_address):
    try:
        ip = ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False

# Valida si la carpeta es de proyecto
def validateFolderProject():
    if not os.path.exists(PWD + MAKEFILE):
        print("[red bold] This folder does not contain sdkcpc project.")
        sys.exit(1)