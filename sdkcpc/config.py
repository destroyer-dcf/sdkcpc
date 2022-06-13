import yaml
from yaml.loader import SafeLoader
import os.path as path
from rich import print
import os
from .common import *
from rich.console import Console
from rich.table import Table
from rich import box

console = Console(width=100,color_system="windows",force_terminal=True)

# Lista el contenido de todas la variables de configuracion de sdkcpc
#   @Param text to write
def listConfigsKeys():
    # data = pkgutil.get_data(__package__, 'sdkcpc.yml')
    print("")
    table = Table(title="sdkcpc configurations",show_lines= True,show_edge=True,box=box.SQUARE,expand=True)
    table.add_column("Key", justify="left", style="yellow", no_wrap=True)
    table.add_column("Value", justify="left", style="green")
    yaml_file = open(path.dirname(path.abspath(__file__)) + '/sdkcpc.yml', 'r')
    yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
    for key, value in yaml_content.items():
        # print(f"[blue]{key}: [white]{value}")
        table.add_row(key, str(value))
    console.print(table)        

# Muestra el valor de la clave especificada
#   @Param: Nombre de la Clave
def getConfigKey(key):
    table = Table(title="sdkcpc configurations",show_lines= True,show_edge=True,box=box.SQUARE,expand=True)
    table.add_column("Key", justify="left", style="yellow", no_wrap=True)
    table.add_column("Value", justify="left", style="green")
    with open(path.dirname(path.abspath(__file__)) + '/sdkcpc.yml', 'r', encoding='utf8') as f:
        try:
            data = yaml.load(f, Loader=SafeLoader)
            table.add_row(key, str(data[key]))
            console.print(table)  
        except KeyError as e:
            print('[red bold]The key %s does not exist' % str(e))
        except IndexError as e:
            print ('red]I got an IndexError - reason "%s"' % str(e))

# Devuelve el valor de la clave especificada
#   @Param: Nombre de la Clave
def getConfigKeyProgram(key):
    with open(path.dirname(path.abspath(__file__)) + '/sdkcpc.yml', 'r', encoding='utf8') as f:
        try:
            data = yaml.load(f, Loader=SafeLoader)
            return data[key]
        except KeyError as e:
            print('[red bold]The key %s does not exist' % str(e))
        except IndexError as e:
            print ('[red bold]I got an IndexError - reason "%s"' % str(e))

# Verifica que exista la clave en el fichero de configuracion
#   @Param: Nombre de la Clave
def checkConfigKey(key):
    with open(path.dirname(path.abspath(__file__)) + '/sdkcpc.yml', 'r', encoding='utf8') as f:
        try:
            data = yaml.load(f, Loader=SafeLoader)
            print("[yellow]Change value Key ("+key+"): [white]" + data[key])
        except KeyError as e:
            print('[red bold]The key %s does not exist' % str(e))
            exit(1)
        except IndexError as e:
            print ('[red bold]I got an IndexError - reason "%s"' % str(e))

# Cambiar el valor de la clave por el especificado
#   @Param: Nombre de la Clave
#   @Param: Nuevo valor de la Clave
def setConfigKeyValue(key,value):
    
    if key == "rvm.path" or key == "winape.path":
        if not os.path.exists(value):
            print("[yellow](config sdkcpc)[red bold]\["+key+"]:El archivo " + value + " does not exist.")
            exit(1)
    checkConfigKey(key)
    with open(path.dirname(path.abspath(__file__)) + '/sdkcpc.yml', 'r', encoding='utf8') as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)

    doc[key] = value

    with open(path.dirname(path.abspath(__file__)) + '/sdkcpc.yml', 'w', encoding='utf8') as f:
        yaml.dump(doc, f)
    print("[yellow]New Value Key    ("+key+"): [green]" + value)

    listConfigsKeys()

# Lee los datos de configuracion para utilizarlos en el programa
def loadConfigData():
    with open(path.dirname(path.abspath(__file__)) + '/sdkcpc.yml', 'r', encoding='utf8') as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)
        return doc