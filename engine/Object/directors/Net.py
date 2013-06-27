#Director - Net
#This director allows the usage of networked connections to play with others

from engine import shared, debug
from string import split

class Director():
	def __init__(self):
		self.Active=False

	def Init(self):
		debug.ACC("dirbuild", self.UnitBuild, args=1, info="Simulate a unit build on the server")

	def Action(self):
		self.Cast=[]
		self.CurrentSelection=[]
		self.CurrentSelectedGroup=None
		self.Active=True

	def UnitBuild(self, name):
		shared.DPrint(0, "NetDir", "Sending building request..")
		shared.protocol.sendMethod(4, "req_build", [name])
	
	def deselectAll(self):
		for unit in self.CurrentSelection:
			unit._deselected()

		if self.CurrentSelectedGroup!=None:
			self.CurrentSelectedGroup.deselected()

	def selectAll(self):
		for unit in self.CurrentSelection:
			unit._selected()

	def evt_selected(self, selections, actionQueueing):
		shared.DPrint("NetDir", 0, "Selections Updated")

		#Update selectionlists
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


		#Check unit group and if the ActionQueueing key is down
		if len(self.CurrentSelection)>0:
			if actionQueueing==True:
				#If only one were selected while AQ was down, and he has a group ...
				#... select all the units in his group
				if len(self.CurrentSelection)==1:
					if self.CurrentSelection[0].group!=None:
						self.deselectAll()
						self.CurrentSelection=self.CurrentSelection[0].group.members[:]
						self.CurrentSelectedGroup=self.CurrentSelection[0].group
						self.selectAll()

				#If only one were selected while AQ was down, and they do not have a group ...
				#... but the previous selection was a group. Add the new selected in the group
				#... and select them all
				if len(self.CurrentSelection)>1:
					if self.OldSelectedGroup!=None:
						newunits = list(set(self.CurrentSelection) - set(self.OldSelection))
						for unit in newunits:
							unit.group = self.OldSelectedGroup
							self.OldSelectedGroup.addUnit(unit)

			#Groupchecks
			if self.CurrentSelection[0].group!=None:
				#Sets the current group if only one unit was selected
				if len(self.CurrentSelection)==1:
					self.CurrentSelectedGroup=self.CurrentSelection[0].group

				#Sets the current group if all the units selected is in the same group
				elif self.CurrentSelection[0].group.members[:] == self.CurrentSelection[:]:
					self.CurrentSelectedGroup=self.CurrentSelection[0].group

		#Update the GUI after the new data
		if self.CurrentSelectedGroup!=None:
			shared.gui['unitinfo'].groupSelected(self.CurrentSelectedGroup)
			self.CurrentSelectedGroup.selected()
		else:
			shared.gui['unitinfo'].noSelection()

		self.OldSelection=[]
		self.OldSelectedGroup=None

	def evt_moveclick(self, pos, actionQueueing):
		selectedIDS=[]
		for x in self.CurrentSelection:
			shared.DPrint("NetDir", 0, "Moving unit: "+str(x))
			selectedIDS.append(x.ID)
			
		shared.SelfPlayer.MoveUnits(selectedIDS, pos)

	def evt_actionclick(self, data, actionQueueing):
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