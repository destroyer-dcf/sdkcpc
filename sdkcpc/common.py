#!/usr/bin/python
from itertools import count
import sys
import os
import os.path
import configparser
import glob
import datetime
import ipaddress
import pathlib

from rich import print
from rich.panel import Panel
from os.path import exists
from tabulate import tabulate
from datetime import datetime

from .config import *

from rich.console import Console

console = Console(width=80,color_system="windows",force_terminal=True)

# DEFINE VARIABLES

PWD                = os.getcwd() + "/"
MAKEFILE           = "Project.cfg"
CONFIG             = loadConfigData()
FOLDER_PROJECT_NEW = ["OUT","ASCII","BIN","BASIC","OBJ"] 
FOLDER_PROJECT_8BP = ["ASM","DSK","MUSIC","OUTPUT_SPEDIT","OUT","ASCII","BIN","BASIC","OBJ"] 
MODELS_CPC         = ["464","664","6128"]


CONFIG_FILE    = "sdkcpc.yml"
PATH_TOOLS     = os.path.split(os.path.abspath(__file__))
PARENT_DIR     = os.path.dirname(os.path.dirname(__file__))
LOG_FILE       = "project.log"


# Create Build de la compilacion
def createBuild():
    now = datetime.now()
    return now


# Leer propiedad del proyecto
#   @Param Seccion
#   @Param Value
def readProyectKey(section,key):
    try:
        config = configparser.RawConfigParser()
        config.read(PWD + MAKEFILE)
        
    except:
        console.print("[red bold]\[ERROR]: Key not exist in "+MAKEFILE)
        sys.exit(1)
    return config.get(section, key)

# Leer todas las keys de una seccion
#   @Param Seccion
def readProyectSection(section):
    try:
        config = configparser.RawConfigParser()
        config.read(PWD + MAKEFILE)
        return dict(config.items(section))
    except:
        print("[red bold]\[ERROR]: Section " + section + " not exist in "+MAKEFILE)
        sys.exit(1)

# Modifica un valor de "+MAKEFILE+"
#   @Param Nombre de la Seccion donde esta la key a modificar
#   @Param nombre de la key a modificar
#   @Param nuevo valor
def setProjectKeyValue(section, key, value):

    try:
        config = configparser.RawConfigParser()
        config.read(PWD + MAKEFILE)
        config.set(section, key, value)
        with open(PWD + MAKEFILE, 'w') as configfile:
            config.write(configfile)
    except:
        console.print("[red bold]\[ERROR]: Section " + section + " or key " + key + " not exist in "+MAKEFILE)
        sys.exit(1)


# get version cpcpy
def  version():
    try:
        # print(PATH_TOOLS[0] + '/VERSION')
        # print(PARENT_DIR)
        # print(pathlib.Path(__file__).parent.absolute())
        # print(os.path.abspath(os.getcwd()))
        with open(PATH_TOOLS[0] + '/VERSION', 'r') as file:
            return file.read().rstrip()
    except IOError:
        return "12.0.0"


def infoLog(recurso,informacion):
    print("[blue bold]\["+recurso+"][yellow bold] "+informacion+" [green bold]\[OK]")

def warningLog(recurso,informacion):
    print("[blue bold]\["+recurso+"][yellow bold] "+informacion+" [yellow bold]\[WARNING]")

def errorLog(recurso,informacion):
    print("[blue bold]\["+recurso+"][yellow bold] "+informacion+" [red bold]\[ERROR]")