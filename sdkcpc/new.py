#!/usr/bin/python

import sys, os
import inquirer
import shutil
from datetime import datetime
import subprocess

import os.path
from os import path

from rich.console import Console
from rich import print
from jinja2 import Template

from .common import *
from rich.console import Console
console = Console(width=80,color_system="windows",force_terminal=True)

# Crea nuevo proyecto en la ruta actua.
#   @Param Nombre del Proyecto
def createNewProject(nameProject,template):
    # chequeamos si el nombre del proyecto contiene espacios
    checkNameProject(nameProject)
    # Creamos estructura del proyectod
    build = str(datetime.now())
    console.rule("[yellow bold]\[New Project: " + nameProject + "]")

    # console.print("[yellow]\nProject Folders")
    if not path.exists(PWD + "/" + nameProject):
        os.makedirs(PWD + "/" + nameProject)
        createStructure(nameProject,template)
        # Creamos makefile del proyecto
        makeFileTemplate(nameProject,build,template)
        # console.print("[yellow]\nBas File")
        basFileTemplate(nameProject,build,template)
        if template == "8BP":
            copy8bp(nameProject)
        console.print("[blue bold]\[Create][white bold] "+nameProject+".bas File.")

        questions = [
            inquirer.List("creategit", message="Do you want to create version control in the project (git software needed)?", choices=["Yes", "No"], default="Yes"),
            inquirer.List("vscodeopen", message="Do you want to open the new Project with Visual Studio Code?", choices=["Yes", "No"], default="Yes"),
        ]
        answers = inquirer.prompt(questions)
        if answers["creategit"] == "Yes":
            console.print("[blue bold]\[Create][white bold] Git Repository")
            gitInit(nameProject)
        if answers["vscodeopen"] == "Yes":
            createVscode(nameProject)
            openVscode(nameProject)
        console.print("[blue bold]\[Create][green bold] Project " + nameProject + " Successfully")
        console.rule("")
    else:
        print(f"[red bold]The " + nameProject + " project exists on this path")
        sys.exit(1)

# Cheque si el nombre de proyecto contiene espacios.
#   @Param Nombre del Proyecto
def checkNameProject(nameProject):
    if nameProject.find(' ') != -1:
        print("[red bold]The project name cannot contain spaces")
        sys.exit(1)

# Create makefile
def makeFileTemplate(project_name, build,template):

    data = {
        "project_name": project_name,
        "compilation" : build,
        "template"    : template
    }
    
    template = """
[compilation]
build = {{ compilation }}
version = 0.0.1

[general]
name = {{ project_name }}
description = None
template = {{ template }}
authors = authors <authors@mail.com>

[config]
concatenate.files = No
validate.83.files = Yes
name.bas.file = {{ project_name }}.bas
name.dsk.file = {{ project_name }}.dsk

[rvm]
model.cpc = 6128

[m4]
ip = 0.0.0.0

    """
    j2_template = Template(template)
    fichero = open(PWD + project_name + "/" + MAKEFILE, 'w')
    fichero.write(j2_template.render(data))
    fichero.close()

# Crea estructura del proyecto
def createStructure(project,template):
    
    if template == "Basic":
        estructura = FOLDER_PROJECT_NEW
    elif template == "8BP":
        estructura = FOLDER_PROJECT_8BP

    for i in estructura:
        if not os.path.isdir(PWD + project + "/" + i):
            os.makedirs(PWD + project + "/" + i)
            print("[blue bold]\[Create][white bold] " + project + "/" + i)

# Crea estructura vscode
def createVscode(project):
    try:
        shutil.copytree(path.dirname(path.abspath(__file__)) + "/resources/vscode",PWD + project + "/.vscode")
        print("[blue bold]\[Create][white bold] Vscode files.")
    except OSError as err:
        print("[red bold]"+str(err))
        sys.exit(1)

# Copia 8bp defauld
def copy8bp(project):
    try:
        shutil.copy(path.dirname(path.abspath(__file__)) + "/resources/8bp.dsk",PWD + project + "/DSK")
        print("[white]Copy example 8bp library.")
    except OSError as err:
        print("[red bold]"+str(err))
        sys.exit(1)

# Inicializacion repositorio GIT
def gitInit(project):
    # try:
    #     os_cmd = "git init " + PWD + project
    #     if os.system(os_cmd) != 0:
    #         raise Exception('[yellow bold][WARNING] The git command does not exist. Unable to initialize repository')
    #         print("[green]    Initialized Git repository.")
    # except:
    #     print('[yellow bold][WARNING] The git command does not exist.')

    FNULL = open(os.devnull, 'w')
    try:
        retcode = subprocess.call(['git', 'init',PWD + project], stdout=FNULL, stderr=subprocess.STDOUT)
    except:
        print('[yellow bold][WARNING] The git command does not exist.')

    try:
        shutil.copy(path.dirname(path.abspath(__file__)) + "/resources/gitignore",PWD + project + "/.gitignore")
        print("[blue bold]\[Create][white bold] gitignore file.")
    except OSError as err:
        print("[bold red]"+err)
        sys.exit(1)

# Open Visual Studio Code
def openVscode(project):
    # try:
    #     os_cmd = "code \"" + PWD + project +"\""
    #     if os.system(os_cmd) != 0:
    #         raise Exception('[yellow bold]\[WARNING] Visual Studio Code command does not exist.')
    # except:
    #     print('[yellow bold][WARNING] Visual Studio Code command does not exist.')
    FNULL = open(os.devnull, 'w')
    try:
        retcode = subprocess.call(['code',PWD + project], stdout=FNULL, stderr=subprocess.STDOUT)
    except:
        print('[yellow bold][WARNING] The Visual Studio Code does not exist.')


# CREATE BAS FILE TEMPLATE
def basFileTemplate(project_name, build,template):

    if template == "Basic":
        data = {
            "project_name": project_name,
            "compilation": build
        }
    
        template = """
1 '=============================================================
1 '== {{ project_name }}
1 '== {{ compilation }}
1 '=============================================================
10 PRINT "HELLO WORLD"
    """
        j2_template = Template(template)
        fichero = open(PWD + project_name + "/BASIC/" + project_name + ".bas", 'w')
        fichero.write(j2_template.render(data))
        fichero.close()

    elif template == "8BP":
        data = {
            "project_name": project_name,
            "compilation": build
        }
    
        template = """
1 '=============================================================
1 '== {{ project_name }}
1 '== {{ compilation }}
1 '=============================================================
10 MEMORY 23999
15 LOAD "8bp.bin"
20 MODE 0: DEFINT A-Z: CALL &6B78:' install RSX
21 ENT 1,10,100,3  
30 ON BREAK GOSUB 320
40 CALL &BC02:'restaura paleta por defecto por si acaso
50 INK 0,0:'fondo negro
60 FOR j=0 TO 31:|SETUPSP,j,0,0:NEXT:|3D,0:'reset sprites
70 |SETLIMITS,0,80,0,124: ' establecemos los limites de la pantalla de juego
80 PLOT 0,74*2:DRAW 640,74*2
90 x=40:y=100:' coordenadas del personaje
100 PRINT "SCORE:"
110 |SETUPSP,31,0,1+32:' status del personaje
120 |SETUPSP,31,7,1'secuencia de animacion asignada al empezar
130 |LOCATESP,31,y,x:'colocamos al sprite (sin imprimirlo aun)
140 |MUSIC,1,0,0,5:puntos=0      
150 cor=32:cod=32:|COLSPALL,@cor,@cod:' configura comando de colision
160 |PRINTSPALL,0,0,0,0: 'configura comando de impresion
170 '--- ciclo de juego ---
180 c=c+1
190 ' lee el teclado y posiciona al personaje
191 IF INKEY(27)=0 THEN IF dir<>0 THEN |SETUPSP,31,7,1:dir=0 ELSE |ANIMA,31:x=x+1:GOTO 195
192 IF INKEY(34)=0 THEN IF dir<>1 THEN |SETUPSP,31,7,2:dir=1 ELSE |ANIMA,31:x=x-1
195 |LOCATESP,31,y,x
200 |AUTOALL:|PRINTSPALL
210 |COLSPALL
220 IF cod<32 THEN BORDER 7:SOUND 4,638,30,15,0,1:puntos=puntos-1:|SETUPSP,cod,0,9:LOCATE 7,1:PRINT puntos:GOTO 250 ELSE BORDER 0    
230 IF c MOD 20=0 THEN puntos=puntos+10 :LOCATE 7,1:PRINT puntos
240 IF c MOD 5=0 THEN |SETUPSP,i,9,19:|SETUPSP,i,5,4,RND*3-1:|SETUPSP,i,0,11:|LOCATESP,i,10,RND*80: i=i+1:IF i=30 THEN i=0
250 IF c <1000 GOTO 180
310 '---fin del juego---
320 |MUSIC: INK 0,0:PEN 1:BORDER 0
    """
        j2_template = Template(template)
        fichero = open(PWD + project_name + "/BASIC/" + project_name + ".bas", 'w')
        fichero.write(j2_template.render(data))
        fichero.close()

#         template = """
# 1 '=============================================================
# 1 '== {{ project_name }}
# 1 '== {{ compilation }}
# 1 '=============================================================
# 10 memory 23999
# 20 load "8bp.bin"
# 30 run "{{ project_name }}.bas"
#     """
#         j2_template = Template(template)
#         fichero = open(PWD + project_name + "/BASIC/loader.bas", 'w')
#         fichero.write(j2_template.render(data))
#         fichero.close()