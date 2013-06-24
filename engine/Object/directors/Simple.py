#Director - Simple
#This is a simple director that allow you to test out unit animations and movement by using the console

from engine import shared, debug
from engine.Object.unitact import move
from string import split

class Director():
	def __init__(self):
		self.Active=False

	def Init(self):
		debug.ACC("dirgo", self.UnitGo, args=2, info="Tell the units directed by SimpleDir to go towards the coordinates")
		debug.ACC("diraim", self.UnitAim, args=3, info="Tell the units directed by SimpleDir to aim towards the coordinates")
		debug.ACC("dirpri", self.UnitPri, args=0, info="Tell the units directed by SimpleDir to do the Primary Action")
		debug.ACC("dirsec", self.UnitPri, args=0, info="Tell the units directed by SimpleDir to do the Secondary Action")
		debug.ACC("diradd", self.UnitAdd, args=1, info="Add a unit under SimpleDir")
		debug.ACC("diradde", self.UnitAddEnemy, args=1, info="Add a unit under SimpleDir")
		debug.ACC("dircls", self.UnitDelAll, args=0, info="Clear/Delete all units directed by SimpleDir")

		self.gotoX=None
		self.gotoY=None
		self.gotoz=None

	def Action(self):
		self.Cast=[]
		self.CurrentSelection=[]
		self.CurrentSelectedGroup=None
		self.Active=True

	def UnitGo(self, x, z):
		self.gotoX=x
		self.gotoZ=z

	def UnitAim(self, x, y, z):
		for actor in self.Cast:
			actor._look(x, y, z)

	def UnitPri(self):
		pass

	def UnitSec(self):
		pass

	def UnitAdd(self, name):
		unit=shared.unitManager.Create(0, name)
		self.Cast.append(unit)

		if not shared.FowManager==None:
			shared.FowManager.addAlly(unit.entity.node, 500)
			shared.FowManager.nodeUpdate(unit.entity.node)

	def UnitAddEnemy(self, name):
		unit=shared.unitManager.Create(0, name)
		self.Cast.append(unit)

		if not shared.FowManager==None:
			shared.FowManager.addEnemy(unit.entity.node)
			shared.FowManager.nodeUpdate(unit.entity.node)

	def UnitDelAll(self):
		pass

	def deselectAll(self):
		for unit in self.CurrentSelection:
			unit._deselected()

		if self.CurrentSelectedGroup!=None:
			self.CurrentSelectedGroup.deselected()

	def selectAll(self):
		for unit in self.CurrentSelection:
			unit._selected()

	def evt_selected(self, selections, actionQueueing):
		shared.DPrint("SimpleDir", 0, "Selections Updated")
		self.selections=selections
		
		self.deselectAll()

		self.OldSelectedGroup = self.CurrentSelectedGroup
		self.OldSelection = self.CurrentSelection[:]

		self.CurrentSelection=[]
		self.CurrentSelectedGroup=None

		for x in self.selections:
			unitID=int(split(x.getName(),"_")[1])
			unit=shared.unitHandeler.Get(unitID)
			unit._selected()
			self.CurrentSelection.append(unit)

		if len(self.CurrentSelection)>0:
			if actionQueueing==True:
				if len(self.CurrentSelection)==1:
					if self.CurrentSelection[0].group!=None:
						self.deselectAll()
						self.CurrentSelection=self.CurrentSelection[0].group.members[:]
						self.CurrentSelectedGroup=self.CurrentSelection[0].group
						self.selectAll()

				if len(self.CurrentSelection)>1:
					if self.OldSelectedGroup!=None:
						newunits = list(set(self.CurrentSelection) - set(self.OldSelection))
						for unit in newunits:
							unit.group = self.OldSelectedGroup
							self.OldSelectedGroup.addUnit(unit)


			if self.CurrentSelection[0].group!=None:
				if len(self.CurrentSelection)==1:
					self.CurrentSelectedGroup=self.CurrentSelection[0].group

				elif self.CurrentSelection[0].group.members[:] == self.CurrentSelection[:]:
					self.CurrentSelectedGroup=self.CurrentSelection[0].group

		if self.CurrentSelectedGroup!=None:
			shared.gui['unitinfo'].groupSelected(self.CurrentSelectedGroup)
			self.CurrentSelectedGroup.selected()
		else:
			shared.gui['unitinfo'].noSelection()

		self.OldSelection=[]
		self.OldSelectedGroup=None

	def evt_moveclick(self, pos, actionQueueing):
		# for x in self.CurrentSelection:
		# 	x._setwaypoint(pos)

		if self.CurrentSelectedGroup==None or actionQueueing==False:
			group = shared.unitGroup.newGroup(persistent=False, members=self.CurrentSelection[:])
			self.CurrentSelectedGroup=group
			for unit in self.CurrentSelection:
				unit.group = group

		if self.CurrentSelectedGroup!=None:
			shared.gui['unitinfo'].groupSelected(self.CurrentSelectedGroup)
			self.CurrentSelectedGroup.selected()
		else:
			shared.gui['unitinfo'].noSelection()

		evt = {"3dMouse":pos}
		self.CurrentSelectedGroup.addAction(move.ActMove(self.CurrentSelectedGroup, evt))

		shared.DPrint("SimpleDir", 0, "Moving group: "+str(shared.unitGroup.groups.index(self.CurrentSelectedGroup)))

	def evt_actionclick(self, data, actionQueueing):
		for x in self.CurrentSelection:
			x.entity.node.showBoundingBox(True)
			shared.reactor.callLater(1, lambda: x.entity.node.showBoundingBox(False))

	def Frame(self):
		#This will get executed each frame
		if self.Active:
			pass