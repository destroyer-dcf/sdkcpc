#!/usr/bin/python

import sys, os
import datetime

from rich.console import Console
from rich import print
from datetime import datetime
import glob
import glob2
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

# Variables for platform
if sys.platform == "darwin":
    _download_idsk = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-OSX.zip"
    _commando_idsk  = path.dirname(path.abspath(__file__)) + "/resources/software/iDSK"
elif sys.platform == "win32" or sys.platform == "win64":
    _download_idsk = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-windows.zip"
    _commando_idsk  = path.dirname(path.abspath(__file__)) + "/resources/software/iDSK.exe"
elif sys.platform == "linux":
    _download_idsk = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-linux.zip"
    _commando_idsk = path.dirname(path.abspath(__file__)) + "/resources/software/iDSK"

# Common variables

BAS_PATH = PWD + "BASIC"
OBJ_PATH = PWD + "OBJ"



project_data = Get_data_project_dict()
    
def build():
    # Download iDSK Software
    Download_IDSK()
    print()
    console.rule("[yellow bold]\[Build Project]")
    console.print("")
    
    # Generate new Version
    new_version     = incrementVersion(project_data["compilation"]["version"])
    new_compilation = str(datetime.now())
    
    # Deleting temporal files
    remove_temporal_files(OBJ_PATH,"*")
    
    # Validate Project
    # checkProject()
    
    # Deleting comment lines ('1) bas files
    files = os.listdir(BAS_PATH + '/')
    for infile in files:
        remove_comments_lines_in_bas_files(infile,new_version, new_compilation)

    # Concatenate files
    if project_data["config"]["concatenate.files"].upper() == "YES":
        files_in_path = os.listdir(OBJ_PATH + '/')
        with open(OBJ_PATH + '/' + project_data["config"]["name.bas.file"]+".concat", "a") as file_object:
            for basfile in files_in_path:
                with open(OBJ_PATH + '/' + basfile) as file:
                    print("[+] Concatenate file -> " +str(basfile))
                    while (line := file.readline().rstrip()):
                        file_object.write(line + "\r\n")
                os.remove(OBJ_PATH + '/' + basfile)
        os.rename(OBJ_PATH + '/' + project_data["config"]["name.bas.file"]+".concat",OBJ_PATH + '/' + project_data["config"]["name.bas.file"])
    
    # Create DSK file
    if project_data["general"]["template"] == "Basic":
        FNULL = open(os.devnull, 'w')
        try:
            retcode = subprocess.Popen([_commando_idsk, PWD+project_data["general"]["name"]+".dsk","-n"], stdout=FNULL, stderr=subprocess.STDOUT)
            print("[+] Create DSK " + project_data["general"]["name"]+".dsk")
        except:
            print("[red bold]ERROR: "+"iDSK does not exist.")
            sys.exit(1)
        Folders = FOLDER_PROJECT_NEW
    else:
        copy_file(path.dirname(path.abspath(__file__)) + "/resources/software/8bp.dsk",project_data["general"]["name"]+".dsk")
        Folders = FOLDER_PROJECT_8BP

    # Add files to DSK
    dsk  = PWD + "/" + project_data["general"]["name"]+".dsk"
    for x in range(0,len(Folders)):
        if not Folders[x] == "BASIC":
            files = os.listdir(PWD + "/" + Folders[x])
            for addfile in files:
                if is_binary(PWD + Folders[x] + "/" + addfile):
                    type_file = "1"
                else:
                    type_file = "0"
                
                FNULL = open(os.devnull, 'w')
                try:
                    retcode = subprocess.run([_commando_idsk, dsk,"-i",PWD + Folders[x] + "/" + addfile,"-f","-t",type_file], stdout=FNULL, stderr=subprocess.STDOUT)
                    print("[+] Add " + Folders[x] + "/" + addfile + " to DSK")
                except:
                    print("[red bold]ERROR: "+"Added file " + Folders[x] + "/" + addfile + " to DSK")
                    sys.exit(1)

    Change_Version_makefile(new_version,new_compilation)
    remove_temporal_files(OBJ_PATH,"*")

    console.print("")
    console.rule("")
    console.print("")
    print ("[blue bold]VERSION: [white bold]" + new_version)
    print ("[blue bold]BUILD  : [white bold]" + new_compilation)
    print ("[blue bold]STATUS : [green bold]SUCCESSFULLY")
    console.print("")
    console.rule("")

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

def Change_Version_makefile(version, compilation):
    try:
        config = configparser.RawConfigParser()
        config.read(PWD + MAKEFILE)
        config.set("compilation", "version", version)
        config.set("compilation", "build", compilation)
        with open(PWD + MAKEFILE, 'w') as configfile:
            config.write(configfile)
    except:
        console.print("[red bold]\[ERROR]: Section " + section + " or key " + key + " not exist in "+MAKEFILE)
        sys.exit(1)

def is_binary(file_name):
    try:
        with open(file_name, 'tr') as check_file:
            check_file.read()
            return False
    except:
        return True

# Copy file
def copy_file(origen,destino):
    try:
        shutil.copy(origen,destino)
    except OSError as err:
        print("[red bold]File copy error" +str(err))
        sys.exit(1)

# Borra ficheros temporales
#   @Param: Carpeta a borrar
def remove_temporal_files(Folder,wilcard):
    files = glob.glob(Folder+'/'+wilcard) 
    for f in files: 
        os.remove(f)
        print("[-] Delete temporal file -> " + os.path.basename(f))

def remove_comments_lines_in_bas_files(file,new_version, new_compilation):
    # Elimina comentarios de linea de Visual studio Code (1 ')
    with open(BAS_PATH + "/" +file, "r") as input:
        with open(OBJ_PATH + "/"+file, "w",newline='\r\n') as output:
            output.write("1 ' Version: " + new_version + " -- Build: " + new_compilation)
            for line in input:
                if not line.strip("\n").startswith("1 '"):
                    output.write(line)
            output.write("\n")
    print("[-] Remove Comment lines -> OBJ/"+file)
    print("[-] Unix to Dos -> OBJ/"+file)

# Version increment
#   @Param current version
def incrementVersion(version):
    version = version.split('.')
    version[2] = str(int(version[2]) + 1)
    return '.'.join(version)