#Clientside Unitmanager
from engine import shared, debug

class UnitManager():
	def __init__(self):
		shared.netUnitManager=self
		shared.objectManager.addEntry(0,4, self)

	def build(self, name, x, y, z, Protocol=None):
		shared.DPrint(0, "netUnitManager", "Erecting "+str(name)+"at"+str((x,y,z)))
		pos=(x, y, z)
		shared.unitManager.Create(0, name, pos)