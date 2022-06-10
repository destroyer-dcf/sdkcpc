#!/usr/bin/python

import os
import os.path
import sys
import subprocess
from .config import *
from .common import *
from .new import *
from rich.console import Console
console = Console(width=80,color_system="windows",force_terminal=True)


def rvm():

    Section_config  = readProyectSection("config")
    Section_general = readProyectSection("general")
    rvm_model = readProyectSection("rvm")
    winape_model = readProyectSection("winape")
    DSK = PWD + "OUT/" + Section_config["name.dsk.file"]
    
    head(str(rvm_model) )
    # Depending on the platform we execute
    RVM = getConfigKeyProgram("rvm.path")
    console.print('[yellow]RUN"'+Section_config["name.bas.file"])
    if sys.platform == "darwin" or sys.platform == "linux":
        subprocess.Popen([RVM,"-i", DSK,"-b=cpc"+rvm_model["model.cpc"],"-c=RUN\""+Section_config["name.bas.file"]+"\"\n"], stdout=subprocess.DEVNULL)
    elif sys.platform == "win32" or sys.platform == "win64":
        run = ' -c=RUN"'+Section_config["name.bas.file"]
        os.system(r"start " + RVM + " -i "+ DSK +  " -b=cpc"+rvm_model["model.cpc"] + run +"\n\n")
    footer()

def winape():
    # Depending on the platform we execute
    print("hgg")