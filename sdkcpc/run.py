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

# Ejecuta retro virtual machine con el dsk asociado
def rvm():
    Section_config  = readProyectSection("config")
    section_compilation = readProyectSection("compilation")
    rvm_model = readProyectSection("rvm")
    DSK = PWD + "OUT/" + Section_config["name.dsk.file"]

    if not os.path.exists(CONFIG["path.rvm"]):
        print("[yellow](config sdkcpc)[red bold]\[path.rvm]:El archivo " + CONFIG["path.rvm"] + " does not exist.")
        exit(1)

    head(readProyectKey("rvm","model.cpc"))
    # Depending on the platform we execute
    RVM = getConfigKeyProgram("path.rvm")
    console.print("[yellow]Build   : " + section_compilation["build"])
    console.print("[yellow]Version : " + section_compilation["version"])
    console.print("[yellow]Emulator: Retro Virtual Machine")
    console.print('[yellow]\nRUN"'+Section_config["name.bas.file"])
    if sys.platform == "darwin" or sys.platform == "linux":
        subprocess.Popen([RVM,"-i", DSK,"-b=cpc"+rvm_model["model.cpc"],"-c=RUN\""+Section_config["name.bas.file"]+"\"\n"], stdout=subprocess.DEVNULL)
    elif sys.platform == "win32" or sys.platform == "win64":
        run = ' -c=RUN"'+Section_config["name.bas.file"]
        os.system(r"start " + RVM + " -i "+ DSK +  " -b=cpc"+rvm_model["model.cpc"] + run +"\n\n")
    footer()

# Ejecuta winape con el dsk asociado
def winape():
    Section_config  = readProyectSection("config")
    section_compilation = readProyectSection("compilation")
    rvm_model = readProyectSection("rvm")
    DSK = PWD + "OUT/" + Section_config["name.dsk.file"]
    DSK = "z:"+DSK.replace("/", "\\").lower()

    if not os.path.exists(CONFIG["path.winape"]):
        print("[yellow](config sdkcpc)[red bold]\[path.winape]:El archivo " + CONFIG["path.winape"] + " does not exist.")
        exit(1)

    head(str(rvm_model["model.cpc"]) )
    # Depending on the platform we execute
    WINAPE = getConfigKeyProgram("path.winape")
    console.print("[yellow]Build   : " + section_compilation["build"])
    console.print("[yellow]Version : " + section_compilation["version"])
    console.print("[yellow]Emulator: Winape")
    console.print('[yellow]\nRUN"'+Section_config["name.bas.file"])
    if sys.platform == "darwin" or sys.platform == "linux":
        subprocess.Popen(["wine",WINAPE,DSK,"/A:"+Section_config["name.bas.file"]], stdout=subprocess.DEVNULL)
    elif sys.platform == "win32" or sys.platform == "win64":
        os.system(r"start " + WINAPE +" "+DSK+" "+"/A:"+Section_config["name.bas.file"])
    footer()