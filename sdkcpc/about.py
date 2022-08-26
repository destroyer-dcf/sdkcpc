from rich.console import Console


from .common import *
from .project import *
from .check import *
from . import __version__

from rich import print
from rich.console import Console
console = Console(width=100,color_system="windows",force_terminal=True)



# Show Banner in console
#   @Param text to show in banner
def about():
    ver =  __version__
    banner ="""\n[bold white] ╔═╗╔╦╗╦╔═╔═╗╔═╗╔═╗ [bold white]┌─────────────┐[/]    [bold white]Created by: [bold green]© Destroyer - 2022[/]
[bold white] ╚═╗ ║║╠╩╗║  ╠═╝║   [bold white]│ [red bold]■■■[green] ■■■[blue] ■■■ [white]│[/]    [bold white]Github    : [bold green]https://github.com/destroyer-dcf/sdkcpc[/]
[bold white] ╚═╝═╩╝╩ ╩╚═╝╩  ╚═╝ [bold white]│ [red bold]■■■[green] ■■■[blue] ■■■ [white]│[/]    [bold white]Version   : [bold green]{ver}[/]
[white] For Amstrad Basic[bold white]  └─────────────┘[/]    [bold white]Follow me : [bold green]twitter: @sdkcpc[/]""".format(ver=ver)

    console.print (banner)
    console.print("")


