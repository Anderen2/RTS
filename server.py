#Dedicated Server - Main
#import algotest
from engine import shared, debug

shared.wd = "./"
shared.side = "Server"

from engine.Networking import sh_netObject, TwCLI
from engine.Networking.server import server
from engine.World import sv_map, steering, pathfinding

from engine.Game import gamemanager

shared.logInit("server")
shared.DPrint("Main",1,"Initializing Modules...")
shared.DPrint("Main",1,"Initializing Networked ObjectManager...")
sh_netObject.ObjectManager()

shared.DPrint("Main",1,"Initializing Server Service...")
shared.Service=server.Service()

shared.DPrint("Main",1,"Initializing UnitManager...")
server.UnitManager()

shared.DPrint("Main",1,"Initializing PlayerManager...")
server.PlayerManager()

shared.DPrint("Main",1,"Initializing Console...")
cliFactory=TwCLI.CLIFactory()

shared.DPrint("Main",1,"Initializing Pathfinder and Steering...")
shared.Pathfinder = pathfinding
shared.VehicleManager = steering.VehicleManager()

shared.DPrint("Main",1,"Initializing MapLoader...")
shared.MapLoader = sv_map.MapLoader()
shared.Map = shared.MapLoader.Load("tri6.map")
shared.Map.Setup()

shared.DPrint("Main",1,"Initializing Gamemanager")
shared.Gamemanager = gamemanager.sv_Gamemanager()

shared.DPrint("Main",1,"Starting Server...")
server.Startup()

