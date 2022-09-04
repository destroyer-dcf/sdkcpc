#!/usr/bin/python

import os
import stat
import os.path
import sys
import requests
import subprocess
from zipfile import ZipFile
import requests
import shutil
from tqdm.auto import tqdm

from .common import *
from .project import *
from rich.console import Console

console = Console(width=80,color_system="windows",force_terminal=True)

# GET PLATFORM
if sys.platform == "darwin":
    RETROVIRTUALMACHINE  = APP_PATH + "/resources/software/RetroVirtualMachine"
    URL = "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "win32" or  sys.platform == "win64":
    RETROVIRTUALMACHINE  = APP_PATH + "/resources/software/RetroVirtualMachine.exe"
    URL = "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "linux":
     RETROVIRTUALMACHINE = APP_PATH + "/resources/software/RetroVirtualMachine"
     URL = "https://static.retrovm.org/release/beta1/linux/x64/RetroVirtualMachine.2.0.beta-1.r7.linux.x64.zip"

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(path, mode)

def download_retro_virtual_machine():
    if not os.path.exists(RETROVIRTUALMACHINE):
        print()
        show_info("Download Retro Virtual Machine.... please wait..","white")
        print()
        with requests.get(URL, stream=True) as r:
            total_length = int(r.headers.get("Content-Length"))
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
                with open(APP_PATH + "/resources/software/rvm.zip", 'wb')as output:
                    shutil.copyfileobj(raw, output)
                    with ZipFile(APP_PATH + "/resources/software/rvm.zip", "r") as zipObj:
                        zipObj.extractall(APP_PATH + "/resources/software")
        os.remove(APP_PATH + "/resources/software/rvm.zip")
        if sys.platform == "darwin" or sys.platform == "linux":
            make_executable(RETROVIRTUALMACHINE)

# Ejecuta retro virtual machine con el dsk asociado
def rvm():
    
    download_retro_virtual_machine()
    print()
    project_data = Get_data_project_dict()
    
    show_head("Run " + project_data["general"]["name"]+".dsk in the Emulator","white")
    DSK = PWD + project_data["general"]["name"]+".dsk"
    print("[+] Version : " + project_data["compilation"]["version"])
    print("[+] Build   : " + project_data["compilation"]["build"])
    print("[+] Bas File: " + project_data["config"]["name.bas.file"])
    print("[+] Dsk File: " + project_data["general"]["name"]+".dsk")
    
    FNULL = open(os.devnull, 'w')
    try:
        # Variables for platform
        if sys.platform == "darwin":
            retcode = subprocess.Popen([RETROVIRTUALMACHINE,"-i", DSK,"-b=cpc"+project_data['rvm']['model.cpc'],"-c=RUN\""+project_data["config"]["name.bas.file"]+"\n"], stdout=FNULL, stderr=subprocess.STDOUT)
        elif sys.platform == "win32" or sys.platform == "win64":
            retcode = subprocess.run([RETROVIRTUALMACHINE,"-i", DSK,"-b=cpc"+project_data['rvm']['model.cpc'],"-c=RUN\""+project_data["config"]["name.bas.file"]+"\n"])
        elif sys.platform == "linux":
            retcode = subprocess.Popen([RETROVIRTUALMACHINE,"-i", DSK,"-b=cpc"+project_data['rvm']['model.cpc'],"-c=RUN\""+project_data["config"]["name.bas.file"]+"\n"], stdout=FNULL, stderr=subprocess.STDOUT)
        show_foot("Execution Successfull","green")
        print()
    except:
        show_info("An error occurred while running Retro Virtual Machine.'","red")
