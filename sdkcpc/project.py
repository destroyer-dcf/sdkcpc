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

from jinja2 import Environment, FileSystemLoader

from .common import *
from rich.console import Console
console = Console(width=80,color_system="windows",force_terminal=True)

# Crea nuevo proyecto en la ruta actua.
#   @Param Nombre del Proyecto
def createNewProject(nameProject,template):
    
    # check nomenclature (spaces, 8:3 file)
    check_project_nomenclature(nameProject)
    
    # Creamos estructura del proyectod

    show_info("Create New Project "+nameProject,"white")
    
    data = {"project_name": nameProject,"compilation": str(datetime.now()),"template": template}

    if not path.exists(PWD + "/" + nameProject):
        
        # Create project folder
        os.makedirs(PWD + "/" + nameProject)
        
        # Create estructure project for template
        create_structure_project(nameProject,template)
        
        # create template makefile
        data = {"project_name": nameProject,"compilation": str(datetime.now()),"template": template}
        create_template(data,"project.j2",PWD + nameProject +"/" + MAKEFILE)

        # create template bas file
        if template == "8BP":
            copy_8bp_library(PWD + nameProject +"/8bp_library/8bp.dsk")
            create_template(data,"8bp.j2",PWD + nameProject +"/src/" + nameProject + ".bas")
        elif template == "Basic":
            create_template(data,"basic.j2",PWD + nameProject +"/src/" + nameProject + ".bas")

        # Create a Git Versions and Vscode files
        questions = [
            inquirer.List("creategit", message="Do you want to create version control in the project (git software needed)?", choices=["Yes", "No"], default="Yes"),
            inquirer.List("vscodeopen", message="Do you want to open the new Project with Visual Studio Code?", choices=["Yes", "No"], default="Yes"),
        ]
        answers = inquirer.prompt(questions)
        if answers["creategit"] == "Yes":
            console.print("[+] Create Git Repository")
            gitInit(nameProject)
        if answers["vscodeopen"] == "Yes":
            createVscode(nameProject)
            openVscode(nameProject)
            
        show_info(nameProject + " project successfully created","green")
    else:
        print("[red bold]\[ERROR] " + nameProject + " project exists on this path.")
        sys.exit(1)

# Cheque si el nombre de proyecto contiene espacios.
#   @Param Nombre del Proyecto
def check_project_nomenclature(nameProject):
    if nameProject.find(' ') != -1:
        print("[red bold]The project name cannot contain spaces")
        sys.exit(1)

    if len(nameProject) > 8:
        print("[red bold] The project name can only have a maximum of 8 characters.")
        sys.exit(1)

# Create template file
def create_template(data,template_name,file):
    j2_env = Environment(loader=FileSystemLoader(TEMPLATES),trim_blocks=True)
    with open(file, mode="w", encoding="utf-8") as message:
            message.write(j2_env.get_template(template_name).render(data))
    print("[+] Create Template " + file)

# Crea estructura del proyecto
def create_structure_project(project,template):
    
    if template == "Basic":
        estructura = FOLDER_PROJECT_NEW
    elif template == "8BP":
        estructura = FOLDER_PROJECT_8BP

    for i in estructura:
        if not os.path.isdir(PWD + project + "/" + i):
            os.makedirs(PWD + project + "/" + i)
            print("[+] Create Folder " + project + "/" + i)

# Crea estructura vscode
def createVscode(project):
    try:
        shutil.copytree(APP_PATH + "/resources/vscode",PWD + project + "/.vscode")
        print("[+] Create Vscode files.")
    except OSError as err:
        print("[red bold]"+str(err))
        sys.exit(1)

# Copia 8bp defauld
def copy_8bp_library(project):
    try:
        shutil.copy(APP_PATH + "/resources/software/8bp.dsk",project)
        print("[+] Copy example 8bp library.")
    except OSError as err:
        print("[red bold]"+str(err))
        sys.exit(1)

# Inicializacion repositorio GIT
def gitInit(project):
    FNULL = open(os.devnull, 'w')
    try:
        retcode = subprocess.call(['git', 'init',PWD + project], stdout=FNULL, stderr=subprocess.STDOUT)
    except:
        print('[red bold][ERROR] The git command does not exist.')

    try:
        shutil.copy(APP_PATH + "/resources/gitignore",PWD + project + "/.gitignore")
        print("[+] Create gitignore file.")
    except OSError as err:
        print("[bold red]"+err)
        sys.exit(1)

# Open Visual Studio Code
def openVscode(project):
    FNULL = open(os.devnull, 'w')
    try:
        retcode = subprocess.call(['code',PWD + project], stdout=FNULL, stderr=subprocess.STDOUT)
    except:
        print('[yellow bold][WARNING] The Visual Studio Code does not exist.')