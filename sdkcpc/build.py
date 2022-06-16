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
    console.rule("[yellow bold]\[Build Project]")
    console.print("")
    checkProject()
    new_version     = incrementVersion(readProyectKey("compilation","version"))
    new_compilation = str(datetime.now())
    BorraTemporales("OUT")
    BorraTemporales("OBJ")
    files = os.listdir(PWD + 'BASIC/')
    for idx, infile in enumerate(files):
            DeleteCommentLines(infile,new_version, new_compilation)

    if Section_config["concatenate.files"].upper() == "YES":
            concat = '\n'.join([open(PWD + "OBJ/" + f).read() for f in files])
            BorraTemporales("OBJ")
            with open(PWD + "OBJ/"+Section_config["name.bas.file"]+".tmp", "w") as fo:
                fo.write(concat)
            infoLog("/BASIC","Contatenate files")
            unix2dos(Section_config["name.bas.file"])
  

    # Creamos Dsk en OUT si el template es basic, si no copiamos la bibliotec 8bp que esta en dsk
    if Section_general["template"] == "Basic":
        FNULL = open(os.devnull, 'w')
        try:
            retcode = subprocess.call([_commando_idsk, PWD+"OUT/"+ Section_config["name.dsk.file"],"-n"], stdout=FNULL, stderr=subprocess.STDOUT)
            infoLog(Section_config["name.dsk.file"],"Create DSK.")
        except:
            errorLog("SDKCPC","iDSK does not exist.")
            sys.exit(1)

    if Section_general["template"] == "8BP":
        copy8bp(Section_general["name"],Section_config["name.dsk.file"])
    addDskFiles("OBJ",0)
    addDskFiles("BIN",1)
    addDskFiles("ASCII",0)
    setProjectKeyValue("compilation","version",new_version)
    setProjectKeyValue("compilation","build",new_compilation)
    BorraTemporales("OBJ")

    console.print("")
    console.rule("")
    console.print("")
    print ("[blue bold]VERSION: [white bold]" + new_version)
    print ("[blue bold]BUILD  : [white bold]" + new_compilation)
    print ("[blue bold]STATUS : [green bold]SUCCESSFULLY")
    console.print("")
    console.rule("")
    footer()

# Copia 8bp defauld
def copy8bp(project,dskfile):
    try:
        shutil.copy(PWD+ "/DSK/8bp.dsk",PWD + "/OUT/"+dskfile)
        infoLog("/DSK","Added 8bp library")
    except OSError as err:
        errorLog("/DSK","Added 8bp library: " +str(err))
        sys.exit(1)

def addDskFiles(folder,tipo):
    Section_config  = readProyectSection("config")
    path = PWD + folder + '/'
    dsk  = PWD + "OUT/" + Section_config["name.dsk.file"]
    files = os.listdir(path)
    for idx, infile in enumerate(files):
        
        FNULL = open(os.devnull, 'w')
        try:
            retcode = subprocess.call([_commando_idsk, dsk,"-i",path + infile,"-f","-t",str(tipo)], stdout=FNULL, stderr=subprocess.STDOUT)
            infoLog(Section_config["name.dsk.file"],"Added file "+folder + '/'+infile)
        except:
            errorLog(Section_config["name.dsk.file"],"Added file "+folder + '/'+infile)
            sys.exit(1)

    if len(files) == 0:
        # Warning("\["+folder+"]: No files in folder ")
        infoLog("/"+folder,"No files in folder")

def DeleteCommentLines(file,new_version, new_compilation):
    # Elimina comentarios de linea de Visual studio Code (1 ')
    file_modificado = file
    with open(PWD + "BASIC/" +file, "r") as input:
        with open(PWD + "OBJ/"+file+".tmp", "w",newline='\r\n') as output:
            # iterate all lines from file
            output.write("1 ' Version: " + new_version + " -- Build: " + new_compilation)
            for line in input:
                if not line.strip("\n").startswith("1 '"):
                    output.write(line)
            output.write("\n")

    infoLog(file,"Delete Comment lines OBJ/"+file)
    # Convertimos fichero a dos
    unix2dos(file)

def unix2dos(file):
    # Convertimos fichero a dos
    remove_lines = open(PWD + "OBJ/"+file+".tmp").read()
    remove_lines = remove_lines.replace('\n', '\r\n')
    with open(PWD + "OBJ/"+file, "w") as fo:
        fo.write(remove_lines + "\n\n")
    os.remove(PWD + "OBJ/"+file+".tmp")
    infoLog(file,"Convert file to dos")
    # infoLog(file,"Delete temporal file")

# Borra ficheros temporales
#   @Param: Carpeta a borrar
def BorraTemporales(Folder):
    files = glob.glob(PWD + Folder+'/*') 
    for f in files: 
        os.remove(f)
        infoLog("/"+Folder,"Delete temporal file " + os.path.basename(f))

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