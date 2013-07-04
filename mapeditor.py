#Tools/Mapeditor

from engine import shared, debug
shared.logInit("mapeditor")
shared.DPrint("Main",1,"Initializing Modules...")

from engine.Render import render
from engine.Object import unitmanager, prop, decorator, zone, directormanager
from engine.Networking.client import client
from engine.World import maploader, pathfinding
from engine.Tool.Mapeditor import globalgui, toolmanager, backend, mapfile

shared.wd="./Data/Map/"
shared.side = "Tool"

#Mainloop
shared.DPrint("Main",1,"Initializing Mainloop...")
shared.client=client.Service()
shared.reactor=client.reactor

#Render
shared.DPrint("Main",1,"Initializing Render...")
shared.render=render.RenderApplication(True) #Render should only Initialize, not setup

#Managers
shared.DPrint("Main",1,"Initializing Managers...")
shared.unitManager=unitmanager.UnitManager()
shared.unitHandeler=shared.unitManager
shared.decHandeler=decorator.DecoratorHandeler()
shared.propManager=prop.propManager()
shared.zoneManager=zone.zoneManager()

shared.toolManager=toolmanager.ToolManager()
shared.mapBackend=backend.MapeditorBackend()

#MapLoader
shared.MapLoader=maploader.MapLoader()
shared.Map=shared.MapLoader.Load("nice.map")

#MapSaver
shared.Mapfile=mapfile.Mapfile()

#CommandParser
shared.DPrint("Main",1,"Initializing CommandParser...")
shared.ParseCommand=debug.ParseCommand

#DirectorManager
shared.DPrint("Main",1,"Initializing DirectorManager...")
shared.DirectorManager=directormanager.DirectorManager()
shared.DirectorManager.Init("Mapeditor")
shared.DirectorManager.Action("Mapeditor")

#Pathfinding
shared.Pathfinder = pathfinding

#Power it up!
shared.DPrint("Main",1,"Startin' Powerin' up!..")
shared.DPrint("Main",1,"PWR: UnitManager")
shared.unitManager.PowerUp()
shared.DPrint("Main",1,"PWR: Render")
shared.render.PowerUp()

shared.render3dScene.Setup()
#shared.renderGUI.SetupBare()

shared.globalGUI=globalgui.MapeditorGUI()
shared.globalGUI.Setup()

shared.renderGUI.createDebugOnly()

shared.renderioInput.SetupBare()

shared.render3dSelectStuff.Trigger="decoNode"

shared.DPrint("Main",1,"PWR: MapSetup")
shared.Map.Setup()

#Release tha clutch and start moving forward
shared.DPrint("Main", 1, "Starting Mainloop..")
shared.client.Run()

#We have come to a stop, lets clean up after ourselves
shared.DPrint("Main", 1, "Mainloop stopped..")
shared.client.cleanUp()
shared.DPrint("Main", 1, "Cleaning up render..")
shared.render.cleanUp()
shared.DPrint("Main", 1, "Ha det bra..")
