#!/usr/bin/python

import sys, os
import datetime

from rich.console import Console
from rich import print
from datetime import datetime
import glob
import requests
from tqdm.auto import tqdm
from zipfile import ZipFile
import stat
from .config import *
from .common import *
from .new import *
from .check import *

from rich.console import Console
console = Console(width=80)

# GET PLATFORM
if sys.platform == "darwin":
    _download_idsk = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-OSX.zip"
    _commando_idsk  = path.dirname(path.abspath(__file__)) + "/resources/software/iDSK"
elif sys.platform == "win32" or sys.platform == "win64":
    _download_idsk = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-windows.zip"
    _commando_idsk  = path.dirname(path.abspath(__file__)) + "/resources/software/iDSK.exe"
elif sys.platform == "linux":
    _download_idsk = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-linux.zip"
    _commando_idsk = path.dirname(path.abspath(__file__)) + "/resources/software/iDSK"

project_data = Get_data_project_dict()

def Download_IDSK():
    if not os.path.exists(_commando_idsk):
        print()
        print("Download iDSK Software Version 0.20.... please wait..")
        print()
        with requests.get(_download_idsk, stream=True) as r:
            total_length = int(r.headers.get("Content-Length"))
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
                with open(path.dirname(path.abspath(__file__)) + "/resources/software/idsk.zip", 'wb')as output:
                    shutil.copyfileobj(raw, output)
                    with ZipFile(path.dirname(path.abspath(__file__)) + "/resources/software/idsk.zip", "r") as zipObj:
                        zipObj.extractall(path.dirname(path.abspath(__file__)) + "/resources/software")
        os.remove(path.dirname(path.abspath(__file__)) + "/resources/software/idsk.zip")
        if sys.platform == "darwin" or sys.platform == "linux":
            make_executable(_commando_idsk)

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(path, mode)
    
def build():
    Download_IDSK()
    print()
    console.rule("[yellow bold]\[Build Project]")
    console.print("")
    checkProject()
    new_version     = incrementVersion(project_data["compilation"]["version"])
    new_compilation = str(datetime.now())
    BorraTemporales("OUT")
    BorraTemporales("OBJ")
    files = os.listdir(PWD + 'BASIC/')
    for idx, infile in enumerate(files):
            DeleteCommentLines(infile,new_version, new_compilation)

    if project_data["config"]["concatenate.files"].upper() == "YES":
            concat = '\n'.join([open(PWD + "OBJ/" + f).read() for f in files])
            BorraTemporales("OBJ")
            with open(PWD + "OBJ/"+project_data["config"]["name.bas.file"]+".tmp", "w") as fo:
                fo.write(concat)
            print("Contatenate files")
            unix2dos(project_data["config"]["name.bas.file"])
  

    # Creamos Dsk en OUT si el template es basic, si no copiamos la bibliotec 8bp que esta en dsk
    if project_data["general"]["template"] == "Basic":
        FNULL = open(os.devnull, 'w')
        try:
            retcode = subprocess.Popen([_commando_idsk, PWD+project_data["general"]["name"]+".dsk","-n"], stdout=FNULL, stderr=subprocess.STDOUT)
            print("Create DSK.")
        except:
            print("[red bold]ERROR: "+"iDSK does not exist.")
            sys.exit(1)

    if project_data["general"]["template"] == "8BP":
        copy8bp(project_data["general"]["name"],project_data["general"]["name"]+".dsk")
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

# Copia 8bp defauld
def copy8bp(project,dskfile):
    try:
        shutil.copy(PWD+ "/DSK/8bp.dsk",PWD + "/"+dskfile)
        print("Added 8bp library")
    except OSError as err:
        print("[red bold]ERROR: "+"Added 8bp library: " +str(err))
        sys.exit(1)

def addDskFiles(folder,tipo):

    path = PWD + folder + '/'
    dsk  = PWD + "/" + project_data["general"]["name"]+".dsk"
    files = os.listdir(path)
    for idx, infile in enumerate(files):
        
        FNULL = open(os.devnull, 'w')
        try:
            retcode = subprocess.Popen([_commando_idsk, dsk,"-i",path + infile,"-f","-t",str(tipo)], stdout=FNULL, stderr=subprocess.STDOUT)
            print("Added file "+folder + '/'+infile)
        except:
            print("[red bold]ERROR: "+"Added file "+folder + '/'+infile)
            sys.exit(1)

    if len(files) == 0:
        print("No files in folder "+folder)

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

    print("Delete Comment lines OBJ/"+file)
    # Convertimos fichero a dos
    unix2dos(file)

def unix2dos(file):
    # Convertimos fichero a dos
    remove_lines = open(PWD + "OBJ/"+file+".tmp").read()
    remove_lines = remove_lines.replace('\n', '\r\n')
    with open(PWD + "OBJ/"+file, "w") as fo:
        fo.write(remove_lines + "\n\n")
    os.remove(PWD + "OBJ/"+file+".tmp")
    print("Convert file to dos")

# Borra ficheros temporales
#   @Param: Carpeta a borrar
def BorraTemporales(Folder):
    files = glob.glob(PWD + Folder+'/*') 
    for f in files: 
        os.remove(f)
        print("Delete temporal file " + os.path.basename(f))

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