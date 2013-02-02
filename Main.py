#Main
#Submodules: Render, Networking, Gameplay, Other

#Initialize stuff
from engine import shared, debug
shared.logInit("engine")
shared.DPrint("Main",1,"Initializing Modules...")

from engine.Render import render
from engine.Object import unitmanager, prop, decorator, zone, directormanager
#from engine.Networking import client

#Networking
#client.Startup()

#Render
shared.render=render.RenderApplication()

#Managers
shared.unitManager=unitmanager.UnitManager()
shared.unitHandeler=shared.unitManager
shared.decHandeler=decorator.DecoratorHandeler()
shared.propManager=prop.propManager()
shared.zoneManager=zone.zoneManager()

#CommandParser
shared.ParseCommand=debug.ParseCommand

#DirectorManager
shared.DirectorManager=directormanager.DirectorManager()

#Power it up!
shared.DPrint("Main",1,"Powerin' up!..")
shared.DPrint("Main",1,"PWR: UnitHandeler")
shared.unitHandeler.PowerUp()
shared.DPrint("Main",1,"PWR: Render")
shared.render.PowerUp()

#Release tha clutch and start moving forward
#shared.render.startRenderLoop()