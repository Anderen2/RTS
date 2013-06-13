#Clientside Unitmanager
import pickle
from engine import shared, debug

class UnitManager():
	def __init__(self):
		shared.netUnitManager=self
		shared.objectManager.addEntry(0,4, self)

	def build(self, name, x, y, z, userid, team, Protocol=None):
		shared.DPrint(0, "netUnitManager", "Erecting "+str(name)+" at "+str((x,y,z)))
		pos=(int(x), int(y), int(z))
		unit = shared.unitManager.Create(0, name, pos)

		print "TEAM"
		print(team)
		print(shared.SelfPlayer.team)

		if int(team) == int(shared.SelfPlayer.team):
			shared.DPrint("netUnitManager", 0, "Adding unit as ally")
			shared.FowManager.addAlly(unit.entity.node, 500)
		else:
			shared.DPrint("netUnitManager", 0, "Adding unit as enemy")
			shared.FowManager.addEnemy(unit.entity.node)

		shared.FowManager.nodeUpdate(unit.entity.node)

	def massmove(self, pickledunits, x, y, z, Protocol=None):
		units=pickle.loads(pickledunits)

		shared.unitManager.massMove(units, (float(x), float(y), float(z)))