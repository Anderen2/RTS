#Dedicated Server - Main
from engine import shared, debug
from engine.Networking import server, sh_netObject
shared.logInit("server")
shared.DPrint("Main",1,"Initializing Modules...")

sh_netObject.ObjectManager()

shared.Service=server.Service()

server.PlayerManager()

server.Startup()