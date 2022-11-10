# SDKCPC (Software Developer Kit para Amstrad CPC)

**sdkcpc** son una serie de librerias y programas multiplataforma desarrollados en *[Python](https://www.python.org/downloads/)*, que nos sirven para facilitarnos la vida en la programación con Locomotive Amstrad Basic en ordenadores actuales. **sdkcpc** se distribuye bajo licencia [LGPL v3](license.md)

**sdkcpc** incluye: 

- Integración con Vscode
- Snnipet integrado para Basic y la libreria [8BP](https://github.com/jjaranda13/8BP)
- Integración con gestor de versiones Git
- Creación DSK
- Comentarios en codigo que no ocupan memoria.
- Trabajo por objetos
- Verificacion formato 8:3
- Compatible con Emulador: Retro Virtual Machine
- Integración con M4-Board
- y mucho mucho más.....


## Requisitos

| Software  | Version  | Url |
|:----------|:----------|:----------|
| Python    | =>3.6    | [Descarga](https://www.python.org/downloads/)    |
| Visual Studio Code    | latest   | [Descarga](https://code.visualstudio.com/download)    |

## Plataformas compatibles

- Windows 10 o Superior
- OS X
- Linux

## Software utilizado


- [Retro Virtual Machine](https://www.retrovirtualmachine.org/)
- [iDSK](https://github.com/cpcsdk/idsk)


---
**NOTE**

It works with almost all markdown flavours (the below blank line matters).

---

```python
class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)
```

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
