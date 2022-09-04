#!/usr/bin/python

import argparse
import configparser
import os
import os.path
import sys

from . import __version__
from .common import *

from .about import *
from .project import *
from .validate import *
# from .build import *
from .compile import *
from .run import *
from .info import *

from .validate import *



def main():
    #Program arguments
    parser = argparse.ArgumentParser()
    parser.version = developer_info()
    
    subparsers = parser.add_subparsers(help='commands',dest='command')

    # A about comman
    about_parser = subparsers.add_parser('about', help='Shows information about Basic SDK')

    # A build comman
    build_parser = subparsers.add_parser('make', help='make the DSK image of the project')
    build_parser.add_argument('-v','--verbose',action='store_false',help='Show all info in compilation project')

    # A deploy comman
    deploy_parser = subparsers.add_parser('deploy', help='Make and Run the dsk image on the emulator or M4-Board')
    deploy_parser.add_argument('-v','--verbose',action='store_false',help='Show all info in Make/Run project')
    deploy_parser = deploy_parser.add_mutually_exclusive_group()
    deploy_parser.add_argument('--rvm',action='store_true',help='Run in Retro Virtual Machine Software')
    deploy_parser.add_argument('--m4',action='store_true',help='Run in M4-Board')
    
    # A check comman
    check_parser = subparsers.add_parser('validate', help='Project data validation.')

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
    run_parser.add_argument('-v','--verbose',action='store_false',help='Show all info in run project')
    run_parser = run_parser.add_mutually_exclusive_group()
    run_parser.add_argument('--rvm',action='store_true',help='Run in Retro Virtual Machine Software')
    run_parser.add_argument('--m4',action='store_true',help='Run in M4-Board')

    # A version comman
    parser.add_argument('-v','--version', action='version')

    # If there are no arguments we exit with error
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)

    args = parser.parse_args()

    if args.command == 'new':

        createNewProject(args.name_project,"Basic")

    elif args.command == 'new-8bp':

        createNewProject(args.name_project_8bp,"8BP")

    elif args.command == 'run':
        if args.verbose == False:
            validate_data_project()
        if args.rvm == True:
            rvm()
            sys.exit(0)
        if args.m4 == True:
            print("[yellow]This option will be supported for the next version")
            sys.exit(0)
        print("\n[red bold]Missing parameter.\n")

    elif args.command == 'deploy':
        if args.rvm == True:
            if args.verbose == False:
                validate_data_project()
            if build() == True:
                rvm()
                sys.exit(0)
        if args.m4 == True:
            print("[yellow]This option will be supported for the next version")
            sys.exit(0)
        print("\n[red bold]Missing parameter.\n")

    elif args.command == 'info':
        info()
    elif args.command == "validate":
        validate_data_project()

    elif args.command == "make":
        if args.verbose == False:
            validate_data_project()
        build()
    elif args.command == "about":
        about()
# def main(args):
#     return 0

if __name__=='__main__':
    main()