import glob
from rich.console import Console


from .common import *
from .project import *
from .validate import *
import configparser
import os

from rich import print
from rich.table import Table
from rich import box
from rich.table import Column
console = Console(width=100,color_system="windows",force_terminal=True)
contador_files = 0

project_data = Get_data_project_dict()

def info():

    show_head("Information project","white")
    # print("[*] ------------------------------------------------------------------------")
    print("[*] [blue bold]COMPILATION [/]------------------------------------------------------------")
    print("[*]   compilation: " + project_data["compilation"]["build"])
    print("[*]   version: " + project_data["compilation"]["version"])
    print("[*] [blue bold]GENERAL [/]----------------------------------------------------------------")
    print("[*]   name: " + project_data["general"]["name"])
    print("[*]   description: " + project_data["general"]["description"])
    print("[*]   template: " + project_data["general"]["template"])
    print("[*]   authors: " + project_data["general"]["authors"])
    print("[*] [blue bold]CONFIG [/]-----------------------------------------------------------------")
    print("[*]   concatenate.bas.files: " + project_data["config"]["concatenate.bas.files"])
    print("[*]   name.bas.file: " + project_data["config"]["name.bas.file"])
    print("[*] [blue bold]RETRO VIRTUAL MACHINE [/]--------------------------------------------------")
    print("[*]   model.cpc: " + project_data["rvm"]["model.cpc"])
    print("[*] [blue bold]M4 BOARD [/]---------------------------------------------------------------")
    print("[*]   ip: " + project_data["m4"]["ip"])
    print(" ")
