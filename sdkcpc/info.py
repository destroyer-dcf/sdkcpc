from rich.console import Console

from .config import *
from .common import *
from .new import *
from .check import *
import configparser
import os

from rich import print
from rich.table import Table
from rich import box
from rich.table import Column
console = Console(width=100,color_system="windows",force_terminal=True)
contador_files = 0

def info():
    Section_config  = readProyectSection("config")
    Section_general = readProyectSection("general")
    Section_compile = readProyectSection("compilation")
    Section_rvm     = readProyectSection("rvm")

    head(str(Section_rvm["model.cpc"]))
    print(" ")

    config = configparser.ConfigParser()
    config.read(PWD + MAKEFILE)

    for i in config.sections():
        ShowDataProjectinSection(i)
    
    console.rule("[bold yellow]PROJECT FILES")
    table = Table(show_lines= True,show_edge=True,box=box.SQUARE,expand=True)
    table.add_column("Folder", justify="left", style="yellow", no_wrap=True)
    table.add_column("Files", justify="left", style="green")
    table.add_column("Size", justify="left", style="white",width=50)

    if Section_general["template"] == "Basic":
        FOLDERS = FOLDER_PROJECT_NEW 
    else:
        FOLDERS = FOLDER_PROJECT_8BP

    for a in FOLDERS:
        total_size = 0
        tabla_files =[]
        tabla_sizes =[]
        files = glob.glob(PWD + a + "/*") 
        contador = 0
        for f in files: 
            if int(f"{os.path.getsize(f)/float(1<<10):,.0f}") == 0:
                total_size = total_size + 1
                table.add_row(a,os.path.basename(f), "1 KB")
            else:
                total_size = total_size + int(f"{os.path.getsize(f)/float(1<<10):,.0f}")
                table.add_row(a,os.path.basename(f), str(f"{os.path.getsize(f)/float(1<<10):,.0f} KB"))
            contador += 1
        if contador == 0:
            table.add_row(a,"No files in folder", "0 KB")
    console.print(table) 
    footer()
    print("")    


def ShowDataProjectinSection(section):
    Sectionitems  = readProyectSection(section)
    console.rule("[bold yellow]"+section.upper())
    table = Table(show_lines= True,show_edge=True,box=box.SQUARE,expand=True,show_header=False)
    table.add_column("key", justify="left", style="green",max_width=7)
    table.add_column("Value", justify="left", style="white")
    for key,value in Sectionitems.items():
            table.add_row(key, value)
    console.print(table)  

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