# SDKCPC (Software Developer Kit para Amstrad CPC)

**SDKCPC** son una serie de librerias y programas multiplataforma desarrollados en *[Python](https://www.python.org/downloads/)*. que nos sirve para facilitarnos la vida en la programación con Locomotive Amstrad Basic, en ordenadores actuales. **SDKCPC** se distribuye bajo licencia [LGPL v3](https://www.python.org/downloads/)

**SDKCPC** incluye: 

- Integración con Vscode
- Snnipet integrado para Basic y para la libreria [8BP](https://github.com/jjaranda13/8BP)
- Integración con gestor de versiones Git
- Creación DSK
- Comentarios en codigo
- Trabajo por objetos
- Verificacion formato 8:3
- Compatible con Emuladores: Retro Virtual Machine y Winape
- Integración con M4-Board
- y mucho mucho más.....


## Plataformas compatibles

- Windows 10 o Superior
- OS X
- Linux


## Requisitos de Software


### Windows
| Software  | Version  | Url |
|:----------|:----------|:----------|
| Python    | =>3.6    | [Descarga](https://www.python.org/downloads/)    |
| Retro Virtual Machine    | =>2.0 BETA-1 R7 10/07/2019    | [Descarga](https://www.retrovirtualmachine.org/es/downloads)    |
| Winape    | 2.0b2    | [Descarga](http://www.winape.net/download/WinAPE20B2.zip)    |
| Visual Studio Code    | latest   | [Descarga](https://code.visualstudio.com/download)    |
| iDSK    | 20    | Incluido en SDKCPC ([Github iDSK](https://github.com/cpcsdk/idsk))      |

### Linux
| Software  | Version  | Url |
|:----------|:----------|:----------|
| Python    | =>3.6    | [Descarga](https://www.python.org/downloads/)    |
| Retro Virtual Machine    | =>2.0 BETA-1 R7 10/07/2019    | [Descarga](https://www.retrovirtualmachine.org/es/downloads)    |
| Winape    | 2.0b2    | [Descarga](http://www.winape.net/download/WinAPE20B2.zip)    |
| Visual Studio Code    | latest   | [Descarga](https://code.visualstudio.com/download)    |
| iDSK    | 20    | Incluido en SDKCPC ([Github iDSK](https://github.com/cpcsdk/idsk))   |
| wine    | --    | **Wine es opcional. Se instalara siempre y cuando queramos usar **Winape** como Emulador para nuestras pruebas.**    |

### OSX
| Software  | Version  | Url |
|:----------|:----------|:----------|
| Python    | =>3.6    | [Descarga](https://www.python.org/downloads/)    |
| Retro Virtual Machine    | =>2.0 BETA-1 R7 10/07/2019    | [Descarga](https://www.retrovirtualmachine.org/es/downloads)    |
| Winape    | 2.0b2    | [Descarga](http://www.winape.net/download/WinAPE20B2.zip)    |
| Visual Studio Code    | latest   | [Descarga](https://code.visualstudio.com/download)    |
| iDSK    | 20    | Incluido en SDKCPC ([Github iDSK](https://github.com/cpcsdk/idsk))       |
| wine    | --    | **Wine es opcional. Se instalara siempre y cuando queramos usar **Winape** como Emulador para nuestras pruebas.**   |


### Instalar Wine en linux:

La instalación en linux se realizada desde nuestro gestor de paquetes:

**Ubuntu/Debian y similares:**

```
sudo apt-get install wine
```
**RHEL/CentOS/Fedora y similares:**
```
sudo yum install wine
```
### Instalar Wine en OSX:

La instalación en OSX la realizaremos desde el gestor de paquetes de codigo abierto **Homebrew**. Lo puedes instalar desde [aqui](https://brew.sh/index_es). Una vez instalado:
```
brew install wine
```

### Instalar Plugins en Visual Studio Code.

Para que nuestra experiencia se total, es necesario instalar la extension Amstrad-Basic de dfreniche para que tengamos el resaltado de sintaxis para los bloques de código fuente Basic. Para ello desde el Gestor de extensiones de Visual Studio Code buscaremos la extension Amstrad-Basic y le datemos a instalar.

![image](screenshot/extension.jpg)


## Instalación SDKCPC en tu sistema

Para instalar **SDKCPC** en tu sistema por favor realice los siguientes pasos:

1. Instale los [Requisitos de Software](#Requisitos-de-Software) de su sistema.
2. Una vez instalados ejecute el siguiente comando desde el cmd/terminal de sus sistema:


```
pip3 install sdkcpc
```
3. Cierre la terminal desde donde lo ejecuto.

Puede comprobar la instalacion del software y sus requisitos escribiendo desde un nuevo cmd/Terminal, que le devolvera la versión instalada del software:

```
sdkcpc --version
```


## Como usar SDKCPC
Podemos ver todas las opciones del programa escribiendo el comando **sdkcpc** seguido del argumento correspondiente y de la opción en el caso de que la tubiera.

```
sdkcpc [argumento] [opcion]
```

## Comandos

A continuacion se muestra una lista de todos los comandos y sus funcionalidades.

**█ about**


| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc about`    |     | Muestra información del software y del desarrollador    |



---
**█ build**


| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc build`    |     | Genera un archivo DSK u CDT con todo el software del proyecto.    |

---
**█ check**


| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc check`    |     | Chequea que las configuraciones (Project.cfg) del proyecto sean correctas.|

---
**█ config**


| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc config`   | --list     | Muestra el listado de las configuraciones SDKCPC.    | 
|                   | [Nombre key]     | Muestra el valor de la key solicitada.    | 
|                   | [Nombre key] [Nuevo valor para la key]    | Modifica el valor de la key solicitada.    | 

Listado de configuracines de SDKCPC. Pueden ser modificadas por el usuario.

| Key  | Valor por defecto  | Descripcion  |
|:----------|:----------|:----------|
| **project.git**    | 1    | Crea el Proyecto con un control de versiones git. Parametros admitidos 1 activado - 0 Desactivado    |
| **project.vscode**    | 1    | Una vez creado el Projecto pregunta si quiere asociarlo a Visual Studio Code. Parametros admitidos 1 activado - 0 Desactivado       |
| **path.rvm**    | None    | Ruta donde esta instalado Retro Virtual Machine. **Es necesario configurar antes de empezar a utilizar SDKCPC**   |
| **path.winape**    | None    | Ruta donde esta instalado Winape. **Es necesario configurar antes de empezar a utilizar SDKCPC**      |
| **show.amstrad.ready**    | 1    | Muestra la cabezera amstrad por consola con la ejecucion de los comandos. Parametros admitidos 1 activado - 0 Desactivado       |
| **show.amstrad.screen**    | 1    | Muestra Ready en la consola una vez ejecutado un comando. Parametros admitidos 1 activado - 0 Desactivado       |

---

Contact information and support
email: cpctelera@cheesetea.com
twitter: @FranGallegoBR
Authors and License
(C) Copyright 2014-2017 CPCtelera's awesome authors
CPCtelera low-level library, examples and scripts are distributed under GNU Lesser General Public License v3
Content authoring tools included within CPCtelera (under cpctelera/tools folder) have their own licenses. Check each of them in their respective folders for more details.