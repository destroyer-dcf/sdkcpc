import yaml
from yaml.loader import SafeLoader
import pkgutil
import os.path as path
from rich.console import Console
from rich import print

from rich.console import Console
console = Console(width=80,color_system="windows",force_terminal=True)

# Lista el contenido de todas la variables de configuracion de sdkcpc
#   @Param text to write
def listConfigsKeys():
    # data = pkgutil.get_data(__package__, 'sdkcpc.yml')
    print("")
    yaml_file = open(path.dirname(path.abspath(__file__)) + '/sdkcpc.yml', 'r')
    yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
    for key, value in yaml_content.items():
        print(f"[blue]{key}: [white]{value}")

# Muestra el valor de la clave especificada
#   @Param: Nombre de la Clave
def getConfigKey(key):
    with open(path.dirname(path.abspath(__file__)) + '/sdkcpc.yml', 'r', encoding='utf8') as f:
        try:
            data = yaml.load(f, Loader=SafeLoader)
            print(f"[blue]{key}: [white]"+ data[key])
        except KeyError as e:
            print('[red]The key %s does not exist' % str(e))
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
            print('[red]The key %s does not exist' % str(e))
        except IndexError as e:
            print ('[red]I got an IndexError - reason "%s"' % str(e))

# Verifica que exista la clave en el fichero de configuracion
#   @Param: Nombre de la Clave
def checkConfigKey(key):
    with open(path.dirname(path.abspath(__file__)) + '/sdkcpc.yml', 'r', encoding='utf8') as f:
        try:
            data = yaml.load(f, Loader=SafeLoader)
            print("[yellow]Chage value Key: [white]" + data[key])
        except KeyError as e:
            print('[red]The key %s does not exist' % str(e))
            exit(1)
        except IndexError as e:
            print ('[red]I got an IndexError - reason "%s"' % str(e))

# Cambiar el valor de la clave por el especificado
#   @Param: Nombre de la Clave
#   @Param: Nuevo valor de la Clave
def setConfigKeyValue(key,value):
    checkConfigKey(key)
    with open(path.dirname(path.abspath(__file__)) + '/sdkcpc.yml', 'r', encoding='utf8') as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)

    doc[key] = value

    with open(path.dirname(path.abspath(__file__)) + '/sdkcpc.yml', 'w', encoding='utf8') as f:
        yaml.dump(doc, f)
    getConfigKey(key)

# Lee los datos de configuracion para utilizarlos en el programa
def loadConfigData():
    with open(path.dirname(path.abspath(__file__)) + '/sdkcpc.yml', 'r', encoding='utf8') as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)
        return doc