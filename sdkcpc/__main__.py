#!/usr/bin/python

import argparse
import configparser
import os
import os.path
import sys

from . import __version__
from .common import *
from .config import *
from .about import *
from .new import *
from .check import *
from .build import *
from .run import *
from .info import *



def main():
    #Program arguments
    parser = argparse.ArgumentParser()
    parser.version = __version__

    subparsers = parser.add_subparsers(help='commands',dest='command')

    # A about comman
    about_parser = subparsers.add_parser('about', help='Shows information about Basic SDK')

    # A build comman
    build_parser = subparsers.add_parser('build', help='Compile the DSK image of the project')

    # A check comman
    check_parser = subparsers.add_parser('check', help='Checks the validity of the project.cfg file.')

    # A config comman
    config_parser = subparsers.add_parser('config', help='Configuration of Basic SDK')
    config_parser.add_argument('Key',type=str,nargs='?',help='Key of config file')
    config_parser.add_argument('Value',type=str,nargs='?',help='Value of config file')
    group_project =  config_parser.add_mutually_exclusive_group()
    group_project.add_argument('--list',action='store_true',help='List the Basic SDK configuration')
    #config_parser.print_help()

    # A info comman
    info_parser = subparsers.add_parser('info', help='Show information of project')

    # A new comman
    new_parser = subparsers.add_parser('new', help='Create new basic project')
    new_parser.add_argument('name_project',type=str)

    # A new 8bp comman
    new_8bp_parser = subparsers.add_parser('new-8bp', help='Create new basic project 8bp')
    new_8bp_parser.add_argument('name_project_8bp',type=str)

    # A run command
    run_parser = subparsers.add_parser('run', help='Run BAS File in DSK image')
    run_parser = run_parser.add_mutually_exclusive_group()
    run_parser.add_argument('--rvm',action='store_true',help='Run in Retro Virtual Machine Software')
    run_parser.add_argument('--winape',action='store_true',help='Run in Winape Software')
    run_parser.add_argument('--m4',action='store_true',help='Run in M4-Board')

    # A version comman
    parser.add_argument('-v','--version', action='version')

    # If there are no arguments we exit with error
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)

    args = parser.parse_args()

    if args.command == 'new':
        createNewProject(args.name_project)

    elif args.command == 'new-8bp':
        print("new project 8bp")

    elif args.command == 'run':

        if args.rvm == True:
            validateFolderProject()
            rvm()
            sys.exit(0)
        if args.winape == True:
            validateFolderProject()
            print("winape option")
            sys.exit(0)
        if args.m4 == True:
            validateFolderProject()
            print("m4 option")
            sys.exit(0)
        print("ERROR NO HAY PARAMETRO DE RETROVIRTUALMACHINE")

    elif args.command == 'config':
        # Lista las configuraciones de sdkcpc
        if args.list == True and not args.Key and not args.Value:
            head("6128")
            listConfigsKeys()
            footer()
            sys.exit(0)
        if args.Key and args.Value:
            # Cambia el valor de una clave
            head("6128")
            setConfigKeyValue(args.Key,args.Value)
            footer()
        else:
            # Muestra el Valor de una Clave
            head("6128")
            getConfigKey(args.Key)
            footer()

    elif args.command == 'info':
        validateFolderProject()
        info()
    elif args.command == "check":
        validateFolderProject()
        Section_rvm     = readProyectSection("rvm")
        head(str(Section_rvm["model.cpc"]))
        print("")
        checkProject()
        print("")
        footer()
    elif args.command == "build":
        validateFolderProject()
        build()
    elif args.command == "about":
        about()
# def main(args):
#     return 0

if __name__=='__main__':
    main()