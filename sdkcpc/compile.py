#!/usr/bin/python

from re import T
import sys, os
import datetime

from rich.console import Console
from rich import print
from datetime import datetime
import glob
import requests
from tqdm.auto import tqdm
from zipfile import ZipFile


from .common import *
from .project import *
from .validate import *

from rich.console import Console
console = Console(width=80,color_system="windows",force_terminal=True)

project_data = Get_data_project_dict()
    
def build():

    # Download iDSK Software
    Download_IDSK()
    print()
    show_head("Build Project","white")
    
    # Generate new Version
    new_version     = incrementVersion(project_data["compilation"]["version"])
    new_compilation = str(datetime.now())
    
    # Deleting temporal files
    remove_temporal_files(OBJ_PATH,"*")
    
    # Deleting comment lines ('1) bas files
    files = os.listdir(BAS_PATH + '/')
    for infile in files:
        remove_comments_lines_in_bas_files(infile,new_version, new_compilation)

    # Concatenate files
    if project_data["config"]["concatenate.bas.files"].upper() == "YES":
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
    # if project_data["general"]["template"] == "Basic":
    #     FNULL = open(os.devnull, 'w')
    #     try:
    #         retcode = subprocess.Popen([COMMANDO_IDSK, PWD+project_data["general"]["name"]+".dsk","-n"], stdout=FNULL, stderr=subprocess.STDOUT)
    #         print("[+] Create DSK " + project_data["general"]["name"]+".dsk")
    #     except:
    #         show_info("BUILD ERROR - "+"iDSK does not exist.","red")
    #         sys.exit(1)
    #     Folders = FOLDER_PROJECT_NEW
    # else:
    #     copy_file(PWD + "8bp_library/8bp.dsk",project_data["general"]["name"]+".dsk")
    #     print("[+] Copy library 8BP to DSK")
    #     Folders = FOLDER_PROJECT_8BP

    FNULL = open(os.devnull, 'w')
    try:
        retcode = subprocess.Popen([COMMANDO_IDSK, PWD+project_data["general"]["name"]+".dsk","-n"], stdout=FNULL, stderr=subprocess.STDOUT)
        print("[+] Create DSK " + project_data["general"]["name"]+".dsk")
    except:
        show_info("BUILD ERROR - "+"iDSK does not exist.","red")
        sys.exit(1)
    Folders = FOLDER_PROJECT_NEW

    if project_data["general"]["template"] == "8BP":
        if not path.exists(PWD + "8bp_library/8bp.dsk"):
            show_foot("BUILD ERROR - 8bp_library/8bp.dsk does not exist.","red")
            sys.exit(1) 
        else:
            try:
                retcode = subprocess.Popen([COMMANDO_IDSK, PWD+"8bp_library/8bp.dsk","-g","bin/8BP.BIN"], stdout=FNULL, stderr=subprocess.STDOUT)
                Folders = FOLDER_PROJECT_8BP
            except:
                show_info("BUILD ERROR - "+"iDSK does not exist.","red")
                sys.exit(1) 
        print("[+] Extract 8BP.BIN to 8bp.dsk")
        
    # Add files to DSK
    dsk  = PWD + project_data["general"]["name"]+".dsk"
    for x in range(0,len(Folders)):
        if Folders[x] == "obj" or Folders[x] == "bin" or Folders[x] == "ascii":
            files = os.listdir(PWD + "/" + Folders[x])
            for addfile in files:
                if is_binary(PWD + Folders[x] + "/" + addfile):
                    type_file = "1"
                else:
                    type_file = "0"
                
                FNULL = open(os.devnull, 'w')
                try:
                    retcode = subprocess.run([COMMANDO_IDSK, dsk,"-i",PWD + Folders[x] + "/" + addfile,"-f","-t",type_file], stdout=FNULL, stderr=subprocess.STDOUT)
                    print("[+] Add " + Folders[x] + "/" + addfile + " to DSK")
                except:
                    show_info("BUILD ERROR - "+"Added file " + Folders[x] + "/" + addfile + " to DSK","red")
                    sys.exit(1)

    Change_Version_makefile(new_version,new_compilation)
    remove_temporal_files(OBJ_PATH,"*")
    print("[+] Building DSK " + project_data["general"]["name"]+".dsk")
    show_foot("Build Successfull - Version: "+new_version + " - Build: "+new_compilation,"green")
    console.print("")

    return True

def Download_IDSK():
    if not os.path.exists(COMMANDO_IDSK):
        show_info("Download iDSK Software Version 0.20.... please wait..","white")
        print()
        with requests.get(DOWNLOAD_IDSK, stream=True) as r:
            total_length = int(r.headers.get("Content-Length"))
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
                with open(APP_PATH + "/resources/software/idsk.zip", 'wb')as output:
                    shutil.copyfileobj(raw, output)
                    with ZipFile(APP_PATH + "/resources/software/idsk.zip", "r") as zipObj:
                        zipObj.extractall(APP_PATH + "/resources/software")
        os.remove(APP_PATH + "/resources/software/idsk.zip")
        if sys.platform == "darwin" or sys.platform == "linux":
            make_executable(COMMANDO_IDSK)

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
        show_info("BUILD ERROR - Section compilation or keys build or version not exist in "+MAKEFILE,"red")
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
        show_info("BUILD ERROR - File copy error" +str(err),"red")
        sys.exit(1)
    return True

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