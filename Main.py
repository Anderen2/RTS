#Main
#Submodules: Render, Networking, Gameplay, Other

from sys import argv
from traceback import print_exc

#Initialize stuff
from engine import shared, debug
shared.logInit("engine")
shared.DPrint("Main",1,"Initializing Modules...")

from engine.Render import render
from engine.Object import unitmanager, prop, decorator, zone, directormanager, unitgroup
from engine.Networking.client import client
from engine.World import maploader, pathfinding

shared.wd="./"
shared.side = "Client"

#Networking and Mainloop
shared.DPrint("Main",1,"Initializing Networking...")
shared.client=client.Service()
shared.reactor=client.reactor
shared.client.Connect("localhost", 1337)

#Render
shared.DPrint("Main",1,"Initializing Render...")
shared.render=render.RenderApplication()

#Managers
shared.DPrint("Main",1,"Initializing Managers...")
shared.unitManager=unitmanager.UnitManager()
shared.unitHandeler=shared.unitManager
shared.unitGroup=unitgroup.GroupManager()
shared.decHandeler=decorator.DecoratorHandeler()
shared.propManager=prop.propManager()
shared.zoneManager=zone.zoneManager()

#MapLoader
shared.MapLoader=maploader.MapLoader()
shared.Map=shared.MapLoader.Load("nice.map")

#Pathfinding
shared.Pathfinder = pathfinding

#Command Parser
shared.DPrint("Main",1,"Initializing CommandParser...")
shared.ParseCommand=debug.ParseCommand

#DirectorManager
shared.DPrint("Main",1,"Initializing DirectorManager...")
shared.DirectorManager=directormanager.DirectorManager()

#Power it up!
shared.DPrint("Main",1,"Startin' Powerin' up!..")
shared.DPrint("Main",1,"PWR: UnitManager")
shared.unitManager.PowerUp()
shared.DPrint("Main",1,"PWR: Render")
shared.render.PowerUp()
shared.DPrint("Main",1,"PWR: MapSetup")
shared.Map.Setup()

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
