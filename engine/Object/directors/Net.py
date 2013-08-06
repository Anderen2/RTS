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
		shared.protocol.sendMethod(4, "req_build", [name, 100, 300, 100])

	def deselectUnit(self, unit):
		if unit in self.CurrentSelection:
			unit._deselected()
			self.CurrentSelection.remove(unit)
			if len(self.CurrentSelection)==0:
				if self.CurrentSelectedGroup:
					self.CurrentSelectedGroup.deselected()
				self.CurrentSelectedGroup=None

			#Update the GUI after the new data
			self.updateGUI()
	
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
			unit=shared.netUnitManager.getFromUID(unitID)
			if unit:
				if unit.GetOwner() == shared.SelfPlayer:
					unit._selected()
					self.CurrentSelection.append(unit)


		#Check unit group and if the ActionQueueing key is down
		if len(self.CurrentSelection)>0:
			if actionQueueing==True:
				print("NET: AQ")
				#If only one were selected while AQ was down, and he has a group ...
				#... select all the units in his group
				if len(self.CurrentSelection)==1:
					if self.CurrentSelection[0]._group!=None:
						self.deselectAll()
						self.CurrentSelection=self.CurrentSelection[0]._group.members[:]
						self.CurrentSelectedGroup=self.CurrentSelection[0]._group
						self.selectAll()

				#If only one were selected while AQ was down, and they do not have a group ...
				#... but the previous selection was a group. Add the new selected in the group
				#... and select them all
				if len(self.CurrentSelection)>1:
					if self.OldSelectedGroup!=None:
						newunits = list(set(self.CurrentSelection) - set(self.OldSelection))
						for unit in newunits:
							#unit._changegroup(self.OldSelectedGroup)
							self.OldSelectedGroup.requestUnitAdd(unit)

			#Groupchecks
			if self.CurrentSelection[0]._group!=None:
				#Sets the current group if only one unit was selected
				if len(self.CurrentSelection)==1:
					self.CurrentSelectedGroup=self.CurrentSelection[0]._group
					print("Currently selected group = "+str(self.CurrentSelectedGroup))

				#Sets the current group if all the units selected is in the same group
				elif self.CurrentSelection[0]._group.members[:] == self.CurrentSelection[:]:
					self.CurrentSelectedGroup=self.CurrentSelection[0]._group

		#Update the GUI after the new data
		self.updateGUI()

		self.OldSelection=[]
		self.OldSelectedGroup=None

	def evt_moveclick(self, pos, actionQueueing):
		if self.CurrentSelectedGroup==None and actionQueueing==False and len(self.CurrentSelection)>0:
			#print("CurrentSelection: "+str(self.CurrentSelection[:]))
			group = shared.GroupManager.req_newgroup(False, self.CurrentSelection[:])
			self.CurrentSelectedGroup=group
			#print("Moving group: "+str(self.CurrentSelectedGroup))

		#Update the GUI after the new data
		self.updateGUI()

		if self.CurrentSelectedGroup!=None and actionQueueing:
			#If we have selected an unit(s) with a groupmembership, check if we got all his members
			#print(self.CurrentSelection)
			#print(self.CurrentSelectedGroup.members)
			if self.CurrentSelection == self.CurrentSelectedGroup.members:
				#Sending an move action to the currently selected group
				evt = {"3dMouse":pos}
				self.CurrentSelectedGroup.requestActionAdd("move", evt)

			#If some members are missing, or not right, create a new group and move it
			else:
				group = shared.GroupManager.req_newgroup(False, self.CurrentSelection[:])
				self.CurrentSelectedGroup=group

				evt = {"3dMouse":pos}
				self.CurrentSelectedGroup.requestActionAdd("move", evt)

		#If we do not have the AQ-Key down, it means we want immidiate action
		elif self.CurrentSelectedGroup!=None and not actionQueueing:
			if self.CurrentSelection == self.CurrentSelectedGroup.members:
				#Sending an move action to the currently selected group
				evt = {"3dMouse":pos}
				self.CurrentSelectedGroup.requestActionDo("move", evt)

			#If some members are missing, or not right, create a new group and move it
			else:
				group = shared.GroupManager.req_newgroup(False, self.CurrentSelection[:])
				self.CurrentSelectedGroup=group

				evt = {"3dMouse":pos}
				self.CurrentSelectedGroup.requestActionDo("move", evt)



	def evt_actionclick(self, data, actionQueueing):
		print("Data: "+str(data))
		unitID=int(split(data,"_")[1])
		print("UnitID: "+str(unitID))
		unitRclicked=shared.netUnitManager.getFromUID(unitID)
		if unitRclicked:
			print("Unit: "+str(unitRclicked))
			print("Owner: "+str(unitRclicked._owner.username))
			
			if self.CurrentSelectedGroup==None and actionQueueing==False and len(self.CurrentSelection)>0:
				group = shared.GroupManager.req_newgroup(False, self.CurrentSelection[:])
				self.CurrentSelectedGroup=group

			#Update the GUI after the new data
			self.updateGUI()
				
			if self.CurrentSelectedGroup!=None and actionQueueing:
				#If we have selected an unit(s) with a groupmembership, check if we got all his members
				if self.CurrentSelection == self.CurrentSelectedGroup.members:
					#Sending an move action to the currently selected group
					evt = {"unitid":unitID}
					self.CurrentSelectedGroup.requestActionAdd("fau", evt)

				#If some members are missing, or not right, create a new group and move it
				else:
					group = shared.GroupManager.req_newgroup(False, self.CurrentSelection[:])
					self.CurrentSelectedGroup=group
						
					evt = {"unitid":unitID}
					self.CurrentSelectedGroup.requestActionAdd("fau", evt)

			#If we do not have the AQ-Key down, it means we want immidiate action
			elif self.CurrentSelectedGroup!=None and not actionQueueing:
				#If we have selected an unit(s) with a groupmembership, check if we got all his members
				if self.CurrentSelection == self.CurrentSelectedGroup.members:
					#Sending an move action to the currently selected group
					evt = {"unitid":unitID}
					self.CurrentSelectedGroup.requestActionDo("fau", evt)

				#If some members are missing, or not right, create a new group and move it
				else:
					group = shared.GroupManager.req_newgroup(False, self.CurrentSelection[:])
					self.CurrentSelectedGroup=group
						
					evt = {"unitid":unitID}
					self.CurrentSelectedGroup.requestActionDo("fau", evt)

	def updateGUI(self):
		#Setting up GUI according to group
		if self.CurrentSelectedGroup!=None:
			shared.gui['unitinfo'].groupSelected(self.CurrentSelectedGroup)
			self.CurrentSelectedGroup.selected()
		else:
			shared.gui['unitinfo'].noSelection()

	def Frame(self):
		#This will get executed each frame
		if self.Active:
			pass