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
        print("[blue bold][SDKCPC][red bold] path.rvm: " + CONFIG["path.rvm"] + " File does not exist.")
        exit(1)

    head(readProyectKey("rvm","model.cpc"))
    # Depending on the platform we execute
    RVM = getConfigKeyProgram("path.rvm")
    console.print("[blue bold][Build   ][yellow] " + section_compilation["build"])
    console.print("[blue bold][Version ][yellow] " + section_compilation["version"])
    console.print("[blue bold][Emulator][yellow] Retro Virtual Machine")
    console.print('[blue bold][DSK File][yellow] ' + Section_config["name.dsk.file"])
    console.print('[blue bold][BAS File][yellow] ' + Section_config["name.bas.file"])
    if sys.platform == "darwin" or sys.platform == "linux":
        subprocess.Popen([RVM,"-i", DSK,"-b=cpc"+rvm_model["model.cpc"],"-c=RUN\""+Section_config["name.bas.file"]+"\"\n"], stdout=subprocess.DEVNULL)
    elif sys.platform == "win32" or sys.platform == "win64":
        run = ' -c=RUN"'+Section_config["name.bas.file"]
        os.system(r"start " + RVM + " -i "+ DSK +  " -b=cpc"+rvm_model["model.cpc"] + run +"\n\n")
    footer()