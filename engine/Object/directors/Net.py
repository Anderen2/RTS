#Director - Net
#This director allows the usage of networked connections to play with others

from engine import shared, debug
from string import split

class Director():
	def __init__(self):
		self.Active=False

	def Init(self):
		#debug.ACC("dirgo", self.UnitGo, args=2, info="Tell the units directed by NetDir to go towards the coordinates")
		debug.ACC("dirbuild", self.UnitBuild, args=1, info="Simulate a unit build on the server")

	def Action(self):
		self.Cast=[]
		self.CurrentSelection=[]
		self.Active=True

	def UnitBuild(self, name):
		shared.DPrint(0, "NetDir", "Sending building request..")
		shared.protocol.sendMethod(4, "req_build", [name])
		#self.Cast.append(shared.unitManager.Create(0, name))

	def evt_selected(self, selections):
		shared.DPrint("NetDir", 0, "Selections Updated")
		self.selections=selections
		for x in self.CurrentSelection:
			x._deselected()

		self.CurrentSelection=[]

		for x in self.selections:
			unitID=int(split(x.getName(),"_")[1])
			unit=shared.unitHandeler.Get(unitID)
			unit._selected()
			self.CurrentSelection.append(unit)

	def evt_moveclick(self, pos):
		selectedIDS=[]
		for x in self.CurrentSelection:
			shared.DPrint("NetDir", 0, "Moving unit: "+str(x))
			selectedIDS.append(x.ID)
			
		shared.SelfPlayer.MoveUnits(selectedIDS, pos)

	def evt_actionclick(self, data):
		for x in self.CurrentSelection:
			pass
			#unitID=int(split(item.movable.getParentSceneNode().getName(),"_")[1])
			#unitRclicked=shared.unitHandeler.Get(unitID)
			#x.entity.node.showBoundingBox(True)
			#shared.reactor.callLater(1, lambda: x.entity.node.showBoundingBox(False))

	def Frame(self):
		#This will get executed each frame
		if self.Active:
			pass