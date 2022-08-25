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
from .config import *
from .common import *
from .new import *
from rich.console import Console

console = Console(width=80,color_system="windows",force_terminal=True)

# GET PLATFORM
if sys.platform == "darwin":
    _rvm  = path.dirname(path.abspath(__file__)) + "/resources/software/RetroVirtualMachine"
    _url = "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "win32" or  sys.platform == "win64":
    _rvm  = path.dirname(path.abspath(__file__)) + "/resources/software/RetroVirtualMachine.exe"
    _url = "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "linux":
     _rvm = path.dirname(path.abspath(__file__)) + "/resources/software/RetroVirtualMachine"
     _url = "https://static.retrovm.org/release/beta1/linux/x64/RetroVirtualMachine.2.0.beta-1.r7.linux.x64.zip"

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(path, mode)

def Download_RVM():
    if not os.path.exists(_rvm):
        print()
        print("Download Retro Virtual Machine.... please wait..")
        print()
        with requests.get(_url, stream=True) as r:
            total_length = int(r.headers.get("Content-Length"))
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
                with open(path.dirname(path.abspath(__file__)) + "/resources/software/rvm.zip", 'wb')as output:
                    shutil.copyfileobj(raw, output)
                    with ZipFile(path.dirname(path.abspath(__file__)) + "/resources/software/rvm.zip", "r") as zipObj:
                        zipObj.extractall(path.dirname(path.abspath(__file__)) + "/resources/software")
        os.remove(path.dirname(path.abspath(__file__)) + "/resources/software/rvm.zip")
        if sys.platform == "darwin" or sys.platform == "linux":
            make_executable(_rvm)

# Ejecuta retro virtual machine con el dsk asociado
def rvm():
    
    Download_RVM()
    print()
    project_data = Get_data_project_dict()
    DSK = PWD + project_data["general"]["name"]+".dsk"
    console.print("[blue bold][Build   ][white] " + project_data["compilation"]["build"])
    console.print("[blue bold][Version ][white] " + project_data["compilation"]["version"])
    console.print("[blue bold][Emulator][white] Retro Virtual Machine")
    console.print('[blue bold][DSK File][white] ' + project_data["general"]["name"]+".dsk")
    console.print('[blue bold][BAS File][white] ' + project_data["config"]["name.bas.file"])
    subprocess.run([_rvm,"-i", DSK,"-b=cpc"+project_data['rvm']['model.cpc'],"-c=RUN\""+project_data["config"]["name.bas.file"]+"\n"])
