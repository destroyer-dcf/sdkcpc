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


from configparser import ConfigParser
from rich.console import Console

console = Console(width=80,color_system="windows",force_terminal=True)

# DEFINE VARIABLES

PWD                = os.getcwd() + "/"
MAKEFILE           = "Project.cfg"
FOLDER_PROJECT_NEW = ["ASCII","BIN","BASIC","OBJ"] 
FOLDER_PROJECT_8BP = ["ASM","DSK","MUSIC","OUTPUT_SPEDIT","OUT","ASCII","BIN","BASIC","OBJ"] 
MODELS_CPC         = ["464","664","6128"]
BAS_PATH           = PWD + "BASIC"
OBJ_PATH           = PWD + "OBJ"
LOG_FILE           = "project.log"
APP_PATH           = os.path.dirname(os.path.abspath(__file__))

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
    config.read('Project.cfg')
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


def show_info(info, color):
    print("[*] ------------------------------------------------------------------------")
    if color == "white":
        console.print("[*] [white bold]" + info.upper())
    elif color == "red":
        console.print("[*] [red bold]" + info.upper())
    elif color == "green":
        console.print("[*] [gren bold]" + info.upper())
    print("[*] ------------------------------------------------------------------------")
