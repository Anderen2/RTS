#Main
#Submodules: Render, Networking, Gameplay, Other
from engine.Render import render
from engine.Object import unitmanager
from engine.Object import decorator
from engine import shared, debug

#Initialize stuff
shared.DPrint(0,1,"Initializing Modules...")
shared.render=render.RenderApplication()
shared.unitManager=unitmanager.UnitManager()
shared.unitHandeler=shared.unitManager
shared.decHandeler=decorator.DecoratorHandeler()
shared.ParseCommand=debug.ParseCommand

#Power it up!
shared.DPrint(0,1,"Powerin' up!..")
shared.DPrint(0,1,"PWR: UnitHandeler")
shared.unitHandeler.PowerUp()
shared.DPrint(0,1,"PWR: Render")
shared.render.PowerUp()

#Release tha clutch and start moving forward
#shared.render.startRenderLoop()