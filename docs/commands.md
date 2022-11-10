# COMANDOS

Podemos ver todas las opciones del programa escribiendo el comando **sdkcpc** seguido del argumento correspondiente y de la opción en el caso de que la tubiera.

```
sdkcpc [argumento] [opcion]
```

```
sdkcpc [argumento] [opcion]
```

## Argumentos
A continuacion se muestra una lista de todos los comandos y sus funcionalidades.

### about

Muestra información del desarrollador del proyecto.

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc about`    |     | Muestra información del software y del desarrollador    |

### -h, --help

Muestra información del desarrollador del proyecto.

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc about`    |     | Muestra información del software y del desarrollador    |



### info

Muestra información del proyecto de la ruta actual.

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc info`    |    | Muestra información del proyecto de la ruta actual.|

### make

Crea una imagen para Disco (DSK) y Cinta (CDT) con el software del proyecto


| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc make`    |     | Genera un archivo DSK con todo el software del proyecto.    |

### new

Crea un nuevo proyecto en la ruta actual con la estructura necesaria para trabajar en Amstrad Locomotive Basic.

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc new`    | [Nombre_proyecto]  | El argumento lleva como opción el nombre que asignaremos a nuestro proyecto.|

> **NOTA:** *No se admiten espacios en el nombre del proyecto.*

### validate

Valida que las configuraciones del proyecto en la ruta actual esten correctas.

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc validate`    |     | Valida que las configuraciones (Project.cfg) del proyecto sean correctas.|

### new-8bp

Crea un nuevo proyecto en la ruta actual con la estructura necesaria para trabajar con la libreria  [8BP](https://github.com/jjaranda13/8BP)

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc new-8bp`    | [Nombre_proyecto]  |El argumento lleva como opción el nombre que asignaremos a nuestro proyecto.|

> **NOTA:** 
> **No se admiten espacios en el nombre del proyecto.**
---

### run

Carga nuestro DSK generado y ejecuta el bas seleccionado sobre el emulador pasado como opcion al argumento.

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc run`    |  --rvm   | Ejecuta el emulador Retro virtual Machine.|
---

### deploy

Carga nuestro DSK generado y ejecuta el bas seleccionado sobre el emulador pasado como opcion al argumento.

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc deploy`    |  --rvm   | Compila y carga el dsk resultante en el emulador Retro virtual Machine.|
---
