#Dedicated Server - Main
from engine import shared, debug
from engine.Networking import server
shared.logInit("engine")
shared.DPrint("Main",1,"Initializing Modules...")

server.Startup()