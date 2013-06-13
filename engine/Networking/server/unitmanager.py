#Serverside Unitmanager
import pickle
from engine import shared, debug
from random import randrange

class UnitManager():
	def __init__(self):
		shared.UnitManager=self
		shared.objectManager.addEntry(0,4, self)

	def req_build(self, name, Protocol=None):
		shared.DPrint(0, "netUnitManager", "Building "+str(name))

		## UNIT VALIDATION AND SERVERSIDE CREATION HERE

		team = shared.PlayerManager.getFromProto(Protocol).team
		userid = shared.PlayerManager.getFromProto(Protocol).UID

		shared.PlayerManager.Broadcast(4, "build", [name, randrange(0,100,1), randrange(100,300,1), randrange(0,100,1), userid, team])

	def massMove(self, unitlist, pos):
		amount=len(unitlist)
		shared.DPrint(0, "netUnitManager", "Massmoving "+str(amount)+ "units to "+str(pos))

		## PATHFINDING SPLITTING AND PATH VALIDATION HERE
		pickledunits=pickle.dumps(unitlist)
		x, y, z = pos
		shared.PlayerManager.Broadcast(4, "massmove", [pickledunits, x, y, z])