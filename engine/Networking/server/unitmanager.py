#Serverside Unitmanager
from engine import shared, debug
from random import randrange

class UnitManager():
	def __init__(self):
		shared.UnitManager=self
		shared.objectManager.addEntry(0,4, self)

	def req_build(self, name, Protocol=None):
		shared.DPrint(0, "netUnitManager", "Building "+str(name))
		shared.PlayerManager.Broadcast(4, "build", [name, randrange(0,100,1), randrange(0,100,1), randrange(0,100,1)])