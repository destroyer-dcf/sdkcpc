from rich.console import Console

from .config import *
from .common import *
from .new import *
from .check import *

import os

from rich import print


contador_files = 0

def info():
    Section_config  = readProyectSection("config")
    Section_general = readProyectSection("general")
    Section_compile = readProyectSection("compilation")
    Section_rvm     = readProyectSection("rvm")

    head(str(Section_rvm["model.cpc"]))
    print(" ")
    print("[yellow] name        : "+Section_general["name"])
    print("[yellow] version     : "+str(Section_compile["version"]))
    print("[yellow] description : "+Section_general["description"])

    GetTotalKbytesFolder("BASIC")
    GetTotalKbytesFolder("BIN")
    GetTotalKbytesFolder("ASCII")
    footer()

# Get number of kbytes of folder
#   @Param folder project
def GetTotalKbytesFolder(folder):
    print("\n[yellow] files in " + folder +" ("+str(CountFilesFolderProject(folder))+"): ")
    total_size = 0
    tabla_files =[]
    tabla_sizes =[]
    files = glob.glob(PWD + folder + "/*") 
    contador = 0
    for f in files: 
        if int(f"{os.path.getsize(f)/float(1<<10):,.0f}") == 0:
            total_size = total_size + 1
            print("[yellow]  -"+os.path.basename(f)+ " (1 KB)")
        else:
            total_size = total_size + int(f"{os.path.getsize(f)/float(1<<10):,.0f}")
            print("[yellow]   -"+os.path.basename(f)+ str(f"{os.path.getsize(f)/float(1<<10):,.0f} KB"))
        contador += 1
    if contador == 0:
        print("[yellow]  -No files in folder")
        print("")

    # return total_size

# Count files in folder project
#   @Param folder project
def CountFilesFolderProject(folder):
    try:
        dir_path = r''+PWD+"/"+folder
        count = 0
        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        return count
    except IOError:
        return 0