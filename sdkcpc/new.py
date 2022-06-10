#!/usr/bin/python

import sys, os
import inquirer
import shutil
from datetime import datetime

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
def createNewProject(nameProject):
    head("6128")
    # chequeamos si el nombre del proyecto contiene espacios
    checkNameProject(nameProject)
    # Creamos estructura del proyecto
    build = createBuild()
    console.rule("[yellow]\[New Project: " + nameProject + "]")

    console.print("[yellow]\nProject Folders")
    if not path.exists(PWD + "/" + nameProject):
        os.makedirs(PWD + "/" + nameProject)
        createStructure(nameProject)
        # Creamos makefile del proyecto
        makeFileTemplate(nameProject,build)
        basFileTemplate(nameProject,build)
        if CONFIG["project.git"] == 1:
            console.print("[yellow]\nGit Repository")
            gitInit(nameProject)
        # Creamos proyecto vscode si activado
        if CONFIG["project.vscode"] == 1:
            console.print("[yellow]\nVisual Studio Code")
            createVscode(nameProject)

        console.print("[green]Project " + nameProject + " Create successfully")
        console.rule("")
        footer()
        if CONFIG["project.vscode"] == 1:
            questions = [
                inquirer.List("vscodeopen", message="Do you want to open the new Project with Visual Studio Code?", choices=["Yes", "No"], default="Yes"),
            ]
            answers = inquirer.prompt(questions)
        
            if answers["vscodeopen"] == "Yes":
                openVscode(nameProject)
    else:
        print(f"[red]The " + nameProject + " project exists on this path")
        sys.exit(1)

# Cheque si el nombre de proyecto contiene espacios.
#   @Param Nombre del Proyecto
def checkNameProject(nameProject):
    if nameProject.find(' ') != -1:
        print("[red]The project name cannot contain spaces")
        sys.exit(1)

# Create makefile
def makeFileTemplate(project_name, build):

    data = {
        "project_name": project_name,
        "compilation" : build
    }
    
    template = """
[compilation]
build = {{ compilation }}
version = 0.0.1

[general]
name = {{ project_name }}
description = None
authors = authors <authors@mail.com>

[config]
concatenate = No
validate83 = Yes
basfile = {{ project_name }}.bas
dskfile = {{ project_name }}.dsk

[rvm]
model = 6128

[winape]
model = 6128

[m4]
ip = 0.0.0.0

    """
    j2_template = Template(template)
    fichero = open(PWD + project_name + "/" + MAKEFILE, 'w')
    fichero.write(j2_template.render(data))
    fichero.close()

# Crea estructura del proyecto
def createStructure(project):
    estructura = FOLDER_PROJECT_NEW
    for i in estructura:
        if not os.path.isdir(PWD + project + "/" + i):
            os.makedirs(PWD + project + "/" + i)
            print("[white]" + project + "/" + i)

# Crea estructura vscode
def createVscode(project):
    try:
        shutil.copytree(path.dirname(path.abspath(__file__)) + "/resources/vscode",PWD + project + "/.vscode")
        print("[white]Create vscode files.")
    except OSError as err:
        print("[red]"+err)
        sys.exit(1)

# Inicializacion repositorio GIT
def gitInit(project):
    try:
        os_cmd = "git init " + PWD + project
        if os.system(os_cmd) != 0:
            raise Exception('[WARNING] The git command does not exist. Unable to initialize repository')
            print("[green]    Initialized Git repository.")
    except:
        print('[yellow]    [WARNING] The git command does not exist.')

    try:
        shutil.copy(path.dirname(path.abspath(__file__)) + "/resources/gitignore",PWD + project + "/.gitignore")
        print("[white]Create .gitignore file.")
    except OSError as err:
        print("[bold red blink]"+err)
        sys.exit(1)

# Open Visual Studio Code
def openVscode(project):
    try:
        os_cmd = "code \"" + PWD + project +"\""
        if os.system(os_cmd) != 0:
            raise Exception('[WARNING] Visual Studio Code command does not exist.')
    except:
        print('[yellow][WARNING] Visual Studio Code command does not exist.')

# CREATE BAS FILE TEMPLATE
def basFileTemplate(project_name, build):
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
    fichero = open(PWD + project_name + "/BASIC/" + project_name.upper() + ".BAS", 'w')
    fichero.write(j2_template.render(data))
    fichero.close()