from rich.console import Console

from .config import *
from .common import *
from .new import *
from .check import *
from . import __version__
import os

from rich import print
from rich.console import Console
console = Console(width=100,color_system="windows",force_terminal=True)



# Show Banner in console
#   @Param text to show in banner
def about():
    head("6128")
    ver =  __version__
    banner ="""\n[bold white] ╔═╗╔═╗╔═╗╔═╗╦ ╦ [bold white]┌─────────────┐[/]    [bold white]Created by: [bold green] © Destroyer - 2022[/]
[bold white] ║  ╠═╝║  ╠═╝╚╦╝ [bold white]│ [red]■■■[green] ■■■[blue] ■■■ [white]│[/]    [bold white]Github    : [bold green] https://github.com/amstrad-cpc/cpcp_core.git[/]
[bold white] ╚═╝╩  ╚═╝╩   ╩  [bold white]│ [red]■■■[green] ■■■[blue] ■■■ [white]│[/]    [bold white]Version   : [bold green] {ver}[/]
[yellow] SDK Amstrad CPC[bold white] └─────────────┘[/]    [bold white]Follow me : [bold green] https://faceboock.com/cpcpy[/]""".format(ver=ver)


    #print(Panel(banner,expand=True))
    console.rule("About")
    console.print (banner)
    console.print("")
    footer()


