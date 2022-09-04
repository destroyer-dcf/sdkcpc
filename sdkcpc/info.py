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
    
    if project_data["general"]["template"] == "8BP":
        info_files(FOLDER_PROJECT_8BP)
    elif project_data["general"]["template"] == "BASIC":
        info_files(FOLDER_PROJECT_NEW)


def info_files(estructura):
    show_head("Files Information","white")
    TOTAL_FILES= 0
    TOTAL_SIZE = 0
    for i in estructura:
        if not i == "8bp_library":
            TOTAL_FILES = TOTAL_FILES + CountFilesFolderProject(i)
            print("[+] [blue bold]"+ i + " [/] (" + str(CountFilesFolderProject(i))+ " Files)")
            arr = next(os.walk(PWD + i))[2]
            if len(arr) == 0:
                TOTAL_SIZE = TOTAL_SIZE + 0
                print('{message: <18}'.format(message="[+]  ....")+"[0 KB]")
            for x in range(0,len(arr)):
                TOTAL_SIZE = TOTAL_SIZE + int(GetKbytes(PWD + i + "/" + arr[x]))
                print('{message: <18}'.format(message="[+]   " + arr[x])+"[" +GetKbytes(PWD + i + "/" + arr[x])+" KB]")
    show_foot("Total "+str(TOTAL_FILES)+" files with a size of " + str(TOTAL_SIZE) + " KB","green")

def GetKbytes(file):
    if int(f"{os.path.getsize(file)/float(1<<10):,.0f}") == 0:
        return "1"
    else:
        return str(f"{os.path.getsize(file)/float(1<<10):,.0f}")



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