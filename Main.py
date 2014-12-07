#Main
#Submodules: Render, Networking, Gameplay, Other

from sys import argv
from traceback import print_exc

#Initialize stuff
from engine import shared, debug
shared.wd="./"
shared.side = "Client"

shared.logInit("engine")
shared.DPrint("Main",1,"Initializing Modules...")

from engine.Render import render
from engine.Object import prop, decorator, zone, directormanager
from engine.Networking.client import client
from engine.World import maploader, pathfinding, steering

from engine.Game import gamemanager

#Networking and Mainloop
shared.DPrint("Main",1,"Initializing Networking...")
shared.client=client.Service()
shared.reactor=client.reactor
shared.client.Connect("192.168.1.112", 1337)

#Render
shared.DPrint("Main",1,"Initializing Render...")
shared.render=render.RenderApplication()

#Entity Managers
shared.DPrint("Main",1,"Initializing Entity Managers...")
#shared.unitGroup=unitgroup.GroupManager() This is now initialized under networking.client
shared.decHandeler=decorator.DecoratorHandeler()
shared.propManager=prop.propManager()
shared.zoneManager=zone.zoneManager()

#Pathfinding and Steering
shared.DPrint("Main",1,"Initializing Steering and Pathfinding...")
shared.VehicleManager = steering.VehicleManager()
shared.Pathfinder = pathfinding

#MapLoader
shared.DPrint("Main",1,"Initializing Maploader...")
shared.MapLoader=maploader.MapLoader()
shared.Map=shared.MapLoader.Load("tri6.map")

#Command Parser
shared.DPrint("Main",1,"Initializing CommandParser...")
shared.ParseCommand=debug.ParseCommand

#DirectorManager
shared.DPrint("Main",1,"Initializing DirectorManager...")
shared.DirectorManager=directormanager.DirectorManager()

#Gamemanager
shared.DPrint("Main",1,"Initializing Gamemanager...")
shared.Gamemanager = gamemanager.cl_Gamemanager()

#Power it up!
shared.DPrint("Main",1,"Startin' Powerin' up!..")
#shared.DPrint("Main",1,"PWR: UnitManager")
#shared.unitManager.PowerUp()
shared.DPrint("Main",1,"PWR: Render")
shared.render.PowerUp()
shared.DPrint("Main",1,"PWR: MapSetup")
shared.Map.Setup()
shared.DPrint("Main",1,"PWR: DecoratorHandeler")
shared.decHandeler.PowerUp()

#Autoexec
shared.DPrint("Main",1,"Executing autoexec")
try:
	debug.runFile("./autoexec")
except:
	shared.DPrint("Main",2,"No autoexec file exsists!")
	print_exc()

#CLI Parameters
shared.DPrint("Main",1,"Executing CLI Parameters")
if len(argv) > 1:
	try:
		debug.runCLI(argv[1:])
	except:
		pass

#Release tha clutch and start moving forward
shared.DPrint("Main", 1, "Starting Mainloop..")
shared.client.Run()

#We have come to a stop, lets clean up after ourselves
shared.DPrint("Main", 1, "Mainloop stopped..")
shared.client.cleanUp()
shared.DPrint("Main", 1, "Cleaning up render..")
shared.render.cleanUp()
shared.DPrint("Main", 1, "Ha det bra..")
