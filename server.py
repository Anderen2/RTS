#Dedicated Server - Main
#import algotest
from engine import shared, debug
from engine.Networking import sh_netObject, TwCLI
from engine.Networking.server import server
from engine.World import sv_map, steering

shared.wd = "./"
shared.side = "Server"

shared.logInit("server")
shared.DPrint("Main",1,"Initializing Modules...")

sh_netObject.ObjectManager()

shared.Service=server.Service()

server.PlayerManager()

cliFactory=TwCLI.CLIFactory()

shared.VehicleManager = steering.VehicleManager()
shared.MapLoader = sv_map.MapLoader()
shared.Map = shared.MapLoader.Load("astar2.map")
shared.Map.Setup()

#algotest.run()

server.Startup()

