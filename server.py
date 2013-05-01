#Dedicated Server - Main
from engine import shared, debug
from engine.Networking import sh_netObject, TwCLI
from engine.Networking.server import server

shared.logInit("server")
shared.DPrint("Main",1,"Initializing Modules...")

sh_netObject.ObjectManager()

shared.Service=server.Service()

server.PlayerManager()

cliFactory=TwCLI.CLIFactory()

server.Startup()