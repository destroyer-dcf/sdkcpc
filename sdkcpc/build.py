#!/usr/bin/python

import argparse
import sys, os
import datetime

from rich.console import Console
from rich import print
from datetime import datetime
import glob

from .config import *
from .common import *
from .new import *
from .check import *

from rich.console import Console
console = Console(width=80,color_system="windows",force_terminal=True)

# GET PLATFORM
if sys.platform == "darwin":
    _commando_idsk  = path.dirname(path.abspath(__file__)) + "/resources/idsk/" + sys.platform + "/iDSK"
elif sys.platform == "win32":
    _commando_idsk  = path.dirname(path.abspath(__file__)) + "/resources/idsk/" + sys.platform + "/iDSK.exe"
elif sys.platform == "win64":
    _commando_idsk  = path.dirname(path.abspath(__file__)) + "/resources/idsk/" + sys.platform + "/iDSK.exe"
elif sys.platform == "linux":
     _commando_idsk = path.dirname(path.abspath(__file__)) + "/resources/idsk/" + sys.platform + "/iDSK"


def build():
    Section_config  = readProyectSection("config")
    Section_general = readProyectSection("general")
    Section_rvm     = readProyectSection("rvm")

    head(str(Section_rvm["model.cpc"]))
    console.rule("[yellow]\[Project]")
    console.print("")
    console.print("[Name        ]: [white]" + Section_general["name"])
    console.print("[Template    ]: [white]" + Section_general["template"])
    console.print("[Concatenate ]: [white]" + Section_config["concatenate.files"])
    console.print("[Validate 8:3]: [white]" + Section_config["validate.83.files"])
    console.print("")
    console.rule("[yellow]\[Verifying Project Data]")
    console.print("")
    checkProject()
    console.print("")
    new_version     = incrementVersion(readProyectKey("compilation","version"))
    new_compilation = str(datetime.now())
    console.rule("[yellow]\[Delete temporary files]")
    console.print("")
    BorraTemporales("OUT")
    BorraTemporales("OBJ")
    console.print("")
    console.rule("[yellow]\[ Processing BAS files ]")
    console.print("")
    files = os.listdir(PWD + 'BASIC/')
    for idx, infile in enumerate(files):
            Info("File #" + str(idx) + "  " + infile)
            DeleteCommentLines(infile,new_version, new_compilation)

    if Section_config["concatenate.files"].upper() == "YES":
            concat = '\n'.join([open(PWD + "OBJ/" + f).read() for f in files])
            BorraTemporales("OBJ")
            with open(PWD + "OBJ/"+Section_config["name.bas.file"]+".tmp", "w") as fo:
                fo.write(concat)
            unix2dos(Section_config["name.bas.file"])
    console.print("")
    # Creamos Dsk en OUT
    console.rule("[yellow]\[   Create DSK File    ]")
    console.print("")
    try:
        os_cmd = _commando_idsk + " " + PWD+"OUT/"+ Section_config["name.dsk.file"] +  ' -n'
        if os.system(os_cmd) != 0:
            raise Exception(_commando_idsk + ' does not exist')
    except:
        Error(Section_config["name.dsk.file"] + " not create!!!")
        print("[blue]VERSION: [bold  white]"+ new_version +"\n[blue]BUILD  : [white]" + new_compilation +"\n[blue]STATUS : [red]ERROR")
        sys.exit(1)
    console.print("")
    addDskFiles("OBJ",0)
    console.print("")
    addDskFiles("BIN",1)
    console.print("")
    addDskFiles("ASCII",0)
    console.print("")
    setProjectKeyValue("compilation","version",new_version)
    setProjectKeyValue("compilation","build",new_compilation)
    console.rule("[yellow]\[Delete temporary files]")
    console.print("")
    BorraTemporales("OBJ")
    console.print("")
    console.rule("")
    console.print("")
    Info ("[blue]VERSION: [white]" + new_version)
    Info ("[blue]BUILD  : [white]" + new_compilation)
    Info ("[blue]STATUS : [green]SUCCESSFULLY")
    console.print("")
    console.rule("")
    footer()

def createDskFile(dskFile,new_version,new_compilation):
    try:
        os_cmd = _commando_idsk + " " + PWD+"OUT/"+dskFile +  ' -n'
        if os.system(os_cmd) != 0:
            raise Exception(_commando_idsk + ' does not exist')
    except:
        Error(dskFile + " not create!!!")
        print("[blue]VERSION: [white]"+ new_version +"\n[blue]BUILD  : [white]" + new_compilation +"\n[blue]STATUS : [red]ERROR")
        sys.exit(1)

def addDskFiles(folder,tipo):
    Section_config  = readProyectSection("config")
    console.rule("[yellow]\[Add Files to DSK folder " + folder.upper()+"]")
    console.print("")
    path = PWD + folder + '/'
    dsk  = PWD + "OUT/" + Section_config["name.dsk.file"]
    files = os.listdir(path)
    for idx, infile in enumerate(files):
        os_cmd = _commando_idsk + " " + dsk + ' -i ' + path + infile + " -f -t " + str(tipo)
        # print(os_cmd)
        try:
            if os.system(os_cmd) != 0:
                raise Exception(_commando_idsk + ' does not exist')
        except:
            Error(path + infile + " not add to DSK!!!")
            sys.exit(1)
        # if folder.upper() == "OBJ":
        #     os.remove(path + infile)  
    if len(files) == 0:
        # Warning("\["+folder+"]: No files in folder ")
        print("[FILES]: No files in folder ")

def DeleteCommentLines(file,new_version, new_compilation):
    # Elimina comentarios de linea de Visual studio Code (1 ')
    with open(PWD + "BASIC/" +file, "r") as input:
        with open(PWD + "OBJ/"+file+".tmp", "w",newline='\r\n') as output:
            # iterate all lines from file
            output.write("1 ' Version: " + new_version + " -- Build: " + new_compilation)
            for line in input:
                if not line.strip("\n").startswith("1 '"):
                    output.write(line)
            output.write("\n")
    print("  [DELETE ]: Comment lines")
    # Convertimos fichero a dos
    unix2dos(file)

def unix2dos(file):
    # Convertimos fichero a dos
    remove_lines = open(PWD + "OBJ/"+file+".tmp").read()
    remove_lines = remove_lines.replace('\n', '\r\n')
    with open(PWD + "OBJ/"+file, "w") as fo:
        fo.write(remove_lines + "\n\n")
    os.remove(PWD + "OBJ/"+file+".tmp")
    print("  [CONVERT]: Convert file to dos")
    print("  [DELETE ]: Delete temporal file") 


# Borra ficheros temporales
#   @Param: Carpeta a borrar
def BorraTemporales(Folder):
    files = glob.glob(PWD + Folder+'/*') 
    for f in files: 
        os.remove(f)
        print("[DELETE ]: " + os.path.basename(f))

# Version increment
#   @Param current version
def incrementVersion(version):
    version = version.split('.')
    version[2] = str(int(version[2]) + 1)
    return '.'.join(version)

# Write log file in project
#   @Param text to write
def WriteLog(texto):
    file_object = open(PWD + LOG_FILE, 'a')
    file_object.write(texto)
    file_object.close()

# Log INFO message
#   @Param text to write
def Info(text):
    print("[white]"+text)

# Log WRITE message
#   @Param text to write
def Warning(text):
    print("[yellow]WARNING  [white]"+text)


# Log ERROR message
#   @Param text to write
def Error(text):
    print("[red]ERROR    [white]"+text)