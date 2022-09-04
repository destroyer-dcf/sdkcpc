#!/usr/bin/python
from itertools import count
import sys
import os
import os.path
import sys, os
import configparser


from rich import print
from rich.panel import Panel
from os.path import exists
from tabulate import tabulate
from datetime import datetime
from . import __version__

from configparser import ConfigParser
from rich.console import Console

console = Console(width=80,color_system="windows",force_terminal=True)

# DEFINE VARIABLES

PWD                = os.getcwd() + "/"
MAKEFILE           = "Project.cfg"
FOLDER_PROJECT_NEW = ["ascii","bin","src","obj"] 
FOLDER_PROJECT_8BP = ["8bp_library","ascii","bin","src","obj"] 
MODELS_CPC         = ["464","664","6128"]
BAS_PATH           = PWD + "src"
OBJ_PATH           = PWD + "obj"
LOG_FILE           = "project.log"
APP_PATH           = os.path.dirname(os.path.abspath(__file__))
TEMPLATES          = APP_PATH + "/resources/templates/"
SOFTWARE           = APP_PATH + "/resources/software/"

# Variables for platform
if sys.platform == "darwin":
    DOWNLOAD_IDSK = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-OSX.zip"
    COMMANDO_IDSK  = APP_PATH + "/resources/software/iDSK"
    RETROVIRTUALMACHINE  = APP_PATH + "/resources/software/RetroVirtualMachine"
    URL = "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "win32" or sys.platform == "win64":
    DOWNLOAD_IDSK = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-windows.zip"
    COMMANDO_IDSK  = APP_PATH + "/resources/software/iDSK.exe"
    RETROVIRTUALMACHINE  = APP_PATH + "/resources/software/RetroVirtualMachine.exe"
    URL = "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "linux":
    DOWNLOAD_IDSK = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-linux.zip"
    COMMANDO_IDSK = APP_PATH + "/resources/software/iDSK"
    RETROVIRTUALMACHINE = APP_PATH + "/resources/software/RetroVirtualMachine"
    URL = "https://static.retrovm.org/release/beta1/linux/x64/RetroVirtualMachine.2.0.beta-1.r7.linux.x64.zip"



# Get data project in dict
def Get_data_project_dict():
    config = ConfigParser()
    config.read(MAKEFILE)
    project_dic = dict(config._sections)
    return project_dic


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

def readBuild():
    file_path = SOFTWARE + "/BUILD"

    if os.path.isfile(file_path):
        text_file = open(file_path, "r")
        data = text_file.read()
        text_file.close()
        return data

    return "Could not read the build"

def show_head(info, color):
    print("[*] ------------------------------------------------------------------------")
    if color == "white":
        console.print("[*][white bold] " + info)
    elif color == "red":
        console.print("[*][red bold] " + info)
    elif color == "green":
        console.print("[*][green bold] " + info)
    print("[*] ------------------------------------------------------------------------")


def show_info(info, color):
    print("[*] ------------------------------------------------------------------------")
    if color == "white":
        console.print("[*][white bold] " + info)
    elif color == "red":
        console.print("[*][red bold] " + info)
    elif color == "green":
        console.print("[*][green bold] " + info)
    print("[*] ------------------------------------------------------------------------")

def show_foot(info, color):
    print("[*] ------------------------------------------------------------------------")
    if color == "white":
        console.print("[*][white bold] " + info)
    elif color == "red":
        console.print("[*][red bold] " + info)
    elif color == "green":
        console.print("[*][green bold] " + info)
    print("[*] ------------------------------------------------------------------------")

def developer_info():
    print("\n[white]sdkcpc [green]v"+str(__version__))
    print("[blue]" + sys.platform+ " - [red] Build: [yellow]"+str(readBuild()))
    print("[magenta]©2022 Destroyer\n")