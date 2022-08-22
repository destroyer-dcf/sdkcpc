#!/usr/bin/python

import os
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
    _rvm  = path.dirname(path.abspath(__file__)) + "/resources/platform/" + sys.platform + "/RetroVirtualMachine"
    _url = "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "win32" or  sys.platform == "win64":
    _rvm  = path.dirname(path.abspath(__file__)) + "/resources/platform/" + sys.platform + "/RetroVirtualMachine.exe"
    _url = "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "linux":
     _rvm = path.dirname(path.abspath(__file__)) + "/resources/platform/" + sys.platform + "/RetroVirtualMachine"
     _url = "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"

def Download_RVM():
    if not os.path.exists(_rvm):
        print()
        print("Download Retro Virtual Machine.... please wait..")
        print()
        with requests.get(_url, stream=True) as r:
            total_length = int(r.headers.get("Content-Length"))
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
                with open(path.dirname(path.abspath(__file__)) + "/resources/platform/" + sys.platform + "/rvm.zip", 'wb')as output:
                    shutil.copyfileobj(raw, output)
                    with ZipFile(path.dirname(path.abspath(__file__)) + "/resources/platform/" + sys.platform + "/rvm.zip", "r") as zipObj:
                        zipObj.extractall(path.dirname(path.abspath(__file__)) + "/resources/platform/" + sys.platform)
        os.remove(path.dirname(path.abspath(__file__)) + "/resources/platform/" + sys.platform + "/rvm.zip")

# Ejecuta retro virtual machine con el dsk asociado
def rvm():
    
    Download_RVM()
    print()
    project_data = Get_data_project_dict()
    DSK = PWD + project_data["general"]["name"]+".dsk"

    # if not os.path.exists(CONFIG["path.rvm"]):
    #     print("[red bold] path.rvm: " + CONFIG["path.rvm"] + " File does not exist.")
    #     exit(1)

    # Depending on the platform we execute
    RVM = _rvm

    console.print("[blue bold][Build   ][white] " + project_data["compilation"]["build"])
    console.print("[blue bold][Version ][white] " + project_data["compilation"]["version"])
    console.print("[blue bold][Emulator][white] Retro Virtual Machine")
    console.print('[blue bold][DSK File][white] ' + project_data["general"]["name"]+".dsk")
    console.print('[blue bold][BAS File][white] ' + project_data["config"]["name.bas.file"])
    subprocess.run([_rvm,"-i", DSK,"-b=cpc"+project_data['rvm']['model.cpc'],"-c=RUN\""+project_data["config"]["name.bas.file"]+"\"\n"],shell=True)
    # FNULL = open(os.devnull, 'w')
    # if sys.platform == "darwin" or sys.platform == "linux":
    #     RVM = RVM.replace(" ","\ ")
    #     #subprocess.Popen([RVM,"-i", DSK,"-b=cpc"+project_data['rvm']['model.cpc'],"-c=RUN\""+project_data["config"]["name.bas.file"]+"\"\n"], stdout=subprocess.DEVNULL,shell=True)
    #     subprocess.run(["RetroVirtualMachine","-i", DSK,"-b=cpc"+project_data['rvm']['model.cpc'],"-c=RUN\""+project_data["config"]["name.bas.file"]+"\"\n"], stderr=subprocess.STDOUT)
    # elif sys.platform == "win32" or sys.platform == "win64":
    #     # run = ' -c=RUN"'+project_data["config"]["name.bas.file"]
    #     # print ('start "' + RVM + ' -i '+ DSK +  ' -b=cpc'+project_data['rvm']['model.cpc'] + run +'"')
    #     # #os.system(r'start "' + RVM + ' -i '+ DSK +  ' -b=cpc'+project_data['rvm']['model.cpc'] + run +'\n\n"')
    #     # cmd = 'start "{0} -i {1} -b=cpc{2} {3}"'.format(RVM,DSK,project_data['rvm']['model.cpc'],run)
    #     # print(cmd)
    #     # os.system(cmd)
    #     subprocess.run([_rvm,"-i", DSK,"-b=cpc"+project_data['rvm']['model.cpc'],"-c=RUN\""+project_data["config"]["name.bas.file"]+"\"\n"],shell=True)
    #         #subprocess.run([RVM,"-i", DSK,"-b=cpc"+project_data['rvm']['model.cpc'],"-c=RUN\""+project_data["config"]["name.bas.file"]+"\"\n"], capture_output=False, shell=True)