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

# Chequeamos si la estructura y el archivo project.cfg 
# contienen errores.
def checkProject():



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
       print("[yellow][Project.cfg][red]\[general]:template [bold red blink]key value is not correct. Correct values [green][Basic,8BP]")
       sys.exit(1)
    # Validamos que el modelo de cpc sea correcto.
    validateModelCpc("rvm")
    validateModelCpc("winape")
    # Validamos el nombre de proyecto
    validateName(readProyectKey("general","name"))
    # validamos la seccion CONFIG
    validateConfigSection(readProyectSection("config"))
    # Validamos que la key IP sea correcta
    IP = readProyectKey("m4","ip")
    if not validateIp(IP):
        print("[yellow][Project.cfg][red]\[m4]:ip = [red]"+ IP + " --> value is not correct.")
        sys.exit(1)
    # Validamos formato de version
    version = readProyectKey("compilation","version")
    if validateVersion(version) < 3:
        print("[yellow][Project.cfg][red]\[compilation]:version = [red]"+ version + " --> The version format is not correct. Correct Value [green]0.0.0")
        sys.exit(1)        
    # print(readProyectSection("general"))
    # print(readProyectSection("config"))
    print("[Project.cfg][green]: Is correct!!")


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
                    print("[yellow](Project Folder)[red]\["+busca[y]+"]:El archivo " + arr[x] + " does not conform to 8:3 format.")
                    sys.exit()

# Validamos la seccion Config
# @Param Array de keys de la seccion
def validateConfigSection(data):
    # Validamos si el dato es correcto
    while data["concatenate.files"].upper() not in ["YES","NO"]:
        print("[yellow][Project.cfg][red]\[config]:concatenate = [red]"+ data["concatenate.files"] + " --> value is not correct. Correct values [green][Yes,No]")
        sys.exit(1)
    # Validamos si el dato es correcto
    while data["validate.83.files"].upper() not in ["YES","NO"]:
        print("[yellow][Project.cfg][bold red blink]\[config]:validate83 = [red]"+ data["validate.83.files"] + " --> value is not correct. Correct values [green][Yes,No]")
        sys.exit(1)
    # Validamos si el dato contiene espacios
    if data["name.bas.file"].find(' ') != -1:
        print("[yellow][Project.cfg][red]\[config]:name.bas.file = [red]"+ data["name.bas.file"] + " --> value is not correct. The name contain spaces")
        sys.exit(1)
    if exists(PWD + "BASIC/"+data["name.bas.file"]) == False:
        print ("[red][ERROR]: BASIC/"+data["name.bas.file"] +" not exist.")
        sys.exit(1)

    # Validamos si el dato contiene espacios
    if data["name.dsk.file"].find(' ') != -1:
        print("[yellow][Project.cfg][red]\[config]:name.bas.file = [red]"+ data["name.dsk.file"] + " --> value is not correct. The name contain spaces")
        sys.exit(1)
    # Si activado formato 8:3 comprobamos que se cumpla en name.bas.file/name.dsk.file
    if data["validate.83.files"].upper() == "YES":
        if len(os.path.splitext(data["name.bas.file"])[1]) != 4:
            print("[yellow][Project.cfg][bold red blink]\[config]:name.bas.file = "+data["name.dsk.file"]+" --> File extension must have 3 characters!")
            sys.exit(1)
        if os.path.splitext(data["name.bas.file"])[1].lower() != ".bas":
            print("[yellow][Project.cfg][red]\[config]:name.bas.file = "+data["name.dsk.file"]+" --> File extension must have 3 characters!")
            sys.exit(1)
        if len(os.path.splitext(data["name.bas.file"])[0]) > 8:
            print("[yellow][Project.cfg][red]\[config]:name.bas.file = "+data["name.dsk.file"]+" --> File name cannot be longer than 8 characters!")
            sys.exit(1)
        if len(os.path.splitext(data["name.dsk.file"])[1]) != 4:
            print("[yellow][Project.cfg][red]\[config]:name.dsk.file = "+data["name.dsk.file"]+" --> File extension must have 3 characters!")
            sys.exit(1)
        if os.path.splitext(data["name.dsk.file"])[1].lower() != ".dsk":
            print("[yellow][Project.cfg][red]\[config]:name.dsk.file = "+data["name.dsk.file"]+" --> File extension must have 3 characters!")
            sys.exit(1)
        if len(os.path.splitext(data["name.dsk.file"])[0]) > 8:
            print("[yellow][Project.cfg][red]\[config]:name.dsk.file = "+data["name.dsk.file"]+" --> File name cannot be longer than 8 characters!")
            sys.exit(1)

# Validamos que existan todas las carpetas del proyecto
#   @Param: array carpetas 
def validateStructureProject(Folders):
    for x in range(0,len(Folders)):
        if not path.exists(PWD + Folders[x]):
            print("[red]The folder "+ Folders[x] +" does not exist in the project")

# Valida que el modelo de cpc sea correcto
#   @Param: seccion
def validateModelCpc(section):
    val = readProyectKey(section,"model.cpc")
    if val not in MODELS_CPC: 
        print("[red]\["+section+"]:model.cpc = [red]"+ val + " --> value is not correct. Correct values [gree][464,664,6128]")
        sys.exit(1)

# Valida que el nombre de proyecto no este vacio
#   @Param: nombre proyecto
def validateName(name):
    if name == "": 
        print("[red]\[general]:name [red]key value cannot be empty.")
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
        print("[red]This folder does not contain sdkcpc project.")
        sys.exit(1)