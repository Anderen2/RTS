#Dedicated Server - Main
from engine import shared, debug
from engine.Networking import server
shared.logInit("server")
shared.DPrint("Main",1,"Initializing Modules...")

server.Startup()