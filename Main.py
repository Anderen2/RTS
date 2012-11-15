#Main
#Submodules: Render, Networking, Gameplay, Other
from engine.Render import render
from engine.Object import unitmanager, prop, decorator, zone, directormanager
from engine import shared, debug

#Initialize stuff
shared.DPrint(0,1,"Initializing Modules...")
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
shared.DPrint(0,1,"Powerin' up!..")
shared.DPrint(0,1,"PWR: UnitHandeler")
shared.unitHandeler.PowerUp()
shared.DPrint(0,1,"PWR: Render")
shared.render.PowerUp()

#Release tha clutch and start moving forward
#shared.render.startRenderLoop()