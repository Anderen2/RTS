#BaseUnit - Serverside
#This is the class which all units derive from and bases itself on
from traceback import print_exc
from importlib import import_module
from twisted.internet import reactor
from engine import shared, debug
from engine.Object.unitact import sv_move, sv_fau
from engine.World import movetypes
from engine.Lib.hook import Hook

class BaseUnit():
	#Setup Constants
	MOVETYPE_AIR = 0
		
	def __init__(self, ID, owner, pos):
		#Setup variables
		self.ID=int(ID)
		self._owner=owner
		self._group=None

		#Initialize all hooks
		self._inithooks()

		#Actions
		self._currentaction=None
		self._globalactions = [sv_move.Action, sv_fau.Action]

		#Movement
		self._vehicle = shared.VehicleManager.create(pos)
		self._movetopoint=None
		self.__oldsteeringpos = (0,0,0)

		#State
		self._autoengage = False #LEGACY Support for vision.py
		self._health = 100
		self.steer_state = False

		self.attributes={} #All current attributes (Used for gamestate syncing)
		self.attributes["default"] = {}
		self.attributes["current"] = {}
		self.attributes["readonly"] = {}

		self._pendingattributes = []

		self._attributehook = Hook(self.attributes) #Hook for listening after attribute changes

		#Attributes
		self.newAttribute("entity.name", "")
		self.newAttribute("entity.solid", False)
		self.newAttribute("movement.constantaltitude", False)
		self.newAttribute("movement.movetype", 1) #Pathfinding algorthim
		self.newAttribute("movement.movespeed", 0) #Pathfinding modespeed
		self.newAttribute("unit.position", (0,0,0))
		self.newAttribute("unit.health", 192)
		self.newAttribute("unit.viewrange", 192)
		self.newAttribute("unit.autoengage", False, readonly=False)
		self.newAttribute("vehicle.size", 1)
		self.newAttribute("vehicle.max_force", 1)
		self.newAttribute("vehicle.mass", 1)
		self.newAttribute("vehicle.path_node_radius", 1)
		self.newAttribute("vehicle.arrive_breaking_radius", 1)
		self.newAttribute("vehicle.max_velocity", 1)
		self.newAttribute("vehicle.max_speed", 1)
		self.newAttribute("vehicle.breaking_force", 1)
		self.newAttribute("vehicle.max_see_ahead", 1)
		self.newAttribute("vehicle.max_avoid_force", 1)
		self.newAttribute("debug.ghostposition", (0,0,0))

		self.addAttributeListener("unit.health", self._sethealth)
		self.addAttributeListener("unit.autoengage", self._setAutoengage)

		self.Hook.Add("OnAttributeModified", self._actOnAttribute)

		self.Initialize(self.ID)
		shared.DPrint(0, "BaseUnit", "Initialized "+str(self.ID))

		#All under is after initialization!
		self._setPosition(pos)

		#QuadTree
		shared.VisionManager.addUnit(self, self.getAttribute("unit.viewrange"))

		self.Hook.call("OnCreation", self._pos)


	def _inithooks(self):
		#Add OnBuild hook
		self.Hook = Hook(self)
		self.Hook.new("Initialize", 1)
		self.Hook.new("OnCreation", 1)
		self.Hook.new("OnThink", 1)
		self.Hook.new("OnHealthChange", 1)
		self.Hook.new("OnDamage", 2)
		self.Hook.new("OnDeath", 1)
		self.Hook.new("OnActionStart", 1)
		self.Hook.new("OnActionAbort", 1)
		self.Hook.new("OnActionFinished", 1)
		self.Hook.new("OnActionState", 3)
		self.Hook.new("OnServerUpdate", 1)
		self.Hook.new("OnGroupChange", 1)
		self.Hook.new("OnMove", 1)
		self.Hook.new("OnMoveStop", 1)
		self.Hook.new("OnConvertStart", 1)
		self.Hook.new("OnConverted", 1)
		self.Hook.new("OnAttributeNew", 1)
		self.Hook.new("OnAttributeModified", 1)
		self.Hook.new("OnAttributeMarked", 1)


	### UnitScript Functions
	def SetPosition(self, x, y, z):
		self._setPosition((x,y,z))
		self.setAttribute("unit.position", (x,y,z), mark=False)

	def GetPosition(self):
		return self._pos

	def CreateProjectileLauncher(self, type):
		launcher = shared.LauncherManager.create(type, self)
		return launcher

	def TakeDamage(self, damage):
		self.setAttribute("unit.health", self._health-damage)
		self.Hook.call("OnDamage", damage, "DamageType Here!")

	def SetAction(self, action, data):
		self._setAction(action, data)

	def GetAction(self):
		return self._currentaction

	def SetOwner(self, newowner):
		"""This is used if the unit is ex. captured by an another player"""
		pass

	### Trigger Hooks

	def _think(self, delta):
		self.Hook.call("OnThink", delta)
		if self._currentaction!=None:
			self._currentaction.update()

		if self.steer_state != "circle" and self._vehicle._previous_path_node_radius:
			self._vehicle.path_node_radius = self._vehicle._previous_path_node_radius
			self._vehicle._previous_path_node_radius = None

		if self._vehicle!=None and self.getAttribute("movement.movetype")!=-1:
			if self.steer_state == "path":
				self._vehicle.followPath(delta, towards=self.getAttribute("movement.movetype")==0)

			elif self.steer_state == "seek":
				if isinstance(self.steer_target, self.__class__):
					self._vehicle.seekPos(self.steer_target._pos)
				else:
					self._vehicle.seekPos(self.steer_target)

			elif self.steer_state == "circle":
				self._vehicle.followCircleAroundPoint(self.steer_circle_pos, 300)

			elif self.steer_state == None and self._vehicle.velocity.length()!=0:
				if self.getAttribute("movement.movetype")==0:
					self._vehicle._circlestate = None
					self.steer_state = "circle"
					self.steer_circle_pos = self._pos
					
				else:
					print("Should stop here")
					self._vehicle.Break()

			if self.steer_state == None and self._vehicle.velocity.length()==0:
				# print("\nStopped entirely!\n")
				pass

			else:
				newpos = self._vehicle.step(delta)
				if newpos!=self.__oldsteeringpos:
					self.__oldsteeringpos = newpos

					if not self.getAttribute("movement.constantaltitude"):
						y = shared.Map.Terrain.getHeightAtPos(newpos[0], newpos[2])+1
					else:
						y = shared.Map.Terrain.getHeightAtPos(newpos[0], newpos[2]) + self.getAttribute("movement.constantaltitude")

					self._setPosition((newpos[0], y, newpos[2]))

		if self._movetopoint!=None:
			if type(self._movetopoint)!=list:
				dist, self._pos = movetypes.Move(self._pos, self._movetopoint, self.getAttribute("movement.movespeed")*delta, self.getAttribute("movement.movetype"))
				print(self._pos)

				if dist<1:
					self._movetopoint=None
			else:
				dist, self._pos = movetypes.Move(self._pos, self._movetopoint[0], self.getAttribute("movement.movespeed")*delta, self.getAttribute("movement.movetype"))

				if dist<1:
					self._movetopoint.pop(0)
					
					if len(self._movetopoint) == 0:
						self._movetopoint = None

		#Quadtree
		shared.VisionManager.unitUpdate(self)

		#Server "ghost"
		if debug.GHOST_SYNC:
			self.setAttribute("debug.ghostposition", self._pos)

		#Attributes
		self._syncAttributes()

	def _actionfinish(self):
		if self._group!=None:
			self._group.unitActionDone(self)

	### Internal Functions

	## Networked

	#Unit Attributes
	def newAttribute(self, attribname, default, readonly=True):
		self.attributes["default"][attribname] = default
		self.attributes["current"][attribname] = default
		self.attributes["readonly"][attribname] = readonly
		self.Hook.call("OnAttributeNew", attribname)

	def delAttribute(self, attribname):
		del self.attributes["default"][attribname]
		del self.attributes["current"][attribname]
		del self.attributes["readonly"][attribname]

	def setAttribute(self, attribname, value, mark=True):
		# shared.DPrint("baseunit", 0, "Attribute S(%s:%i): %s = %s" % (self.UnitID, self.ID, attribname, str(value)))
		if attribname not in self.attributes["current"]:
			shared.DPrint("baseunit", 2, "Attribute (%s:%i): %s does not exist, creating it!" % (self.UnitID, self.ID, attribname))
			self.newAttribute(attribname, value)
		else:
			self.attributes["current"][attribname] = value

		if mark:
			self.markAttribute(attribname)

		if self._attributehook.doesExist(attribname):
			self._attributehook.call(attribname, value)

		self.Hook.call("OnAttributeModified", attribname)

	def getAttribute(self, attribname):
		return self.attributes["current"][attribname]

	def resetAttribute(self, attribname, mark=True):
		self.attributes["current"][attribname] = self.attributes["default"][attribname]

		if mark:
			self.markAttribute(attribname)

		if self._attributehook.doesExist(attribname):
			self._attributehook.call(attribname, value)

		self.Hook.call("OnAttributeModified", attribname)

	def setAttributeInitial(self, attribname, value):
		#Set attribute "inital" value
		shared.DPrint("baseunit", 0, "Attribute I(%s:%i): %s = %s" % (self.UnitID, self.ID, attribname, str(value)))
		self.attributes["current"][attribname] = value
		self.attributes["default"][attribname] = value

		if self._attributehook.doesExist(attribname):
			self._attributehook.call(attribname, value)

		self.Hook.call("OnAttributeModified", attribname)

	def setAttributeDefault(self, attribname, value):
		self.attributes["default"][attribname] = value

	def setAttributeReadonly(self, attribname, value):
		self.attributes["readonly"][attribname] = value

	def markAttribute(self, attribname):
		#Mark attribute as modified
		self._pendingattributes.append(attribname)
		self.Hook.call("OnAttributeMarked", attribname)

	def addAttributeListener(self, attribname, func):
		if self._attributehook.doesExist(attribname):
			self._attributehook.Add(attribname, func)
		else:
			self._attributehook.new(attribname, 1)
			self._attributehook.Add(attribname, func)
		
	def _syncAttributes(self):
		if len(self._pendingattributes)!=0:
			self._broadcastAttributes()

	def _broadcastAttributes(self):
		diff = {}
		for attribname in self._pendingattributes:
			diff[attribname] = self.attributes["current"][attribname]

		self.Hook.call("OnServerUpdate", diff.copy())
		shared.PlayerManager.Broadcast(4, "recv_attrib", [self.ID, diff.copy()])
		self._pendingattributes = []

	# Attribute actions
	def _actOnAttribute(self, attribname): #Needed?
		attrib = attribname.split(".")
		if attrib[0]=="vehicle":
			if attrib[1]=="size": self._vehicle.size = self.getAttribute(attribname)
			elif attrib[1]=="max_force": self._vehicle.max_force = self.getAttribute(attribname)
			elif attrib[1]=="mass": self._vehicle.mass = self.getAttribute(attribname)
			elif attrib[1]=="path_node_radius": self._vehicle.path_node_radius = self.getAttribute(attribname)
			elif attrib[1]=="arrive_breaking_radius": self._vehicle.arrive_breaking_radius = self.getAttribute(attribname)
			elif attrib[1]=="max_velocity": self._vehicle.max_velocity = self.getAttribute(attribname)
			elif attrib[1]=="max_speed": self._vehicle.max_speed = self.getAttribute(attribname)
			elif attrib[1]=="breaking_force": self._vehicle.breaking_force = self.getAttribute(attribname)
			elif attrib[1]=="max_see_ahead": self._vehicle.max_see_ahead = self.getAttribute(attribname)
			elif attrib[1]=="max_avoid_force": self._vehicle.max_avoid_force = self.getAttribute(attribname)

			print "Vehicle Attributes Changed!"

	def _setAutoengage(self, enabled):
		self._autoengage = enabled #LEGACY Support for vision.py
		if enabled:
			shared.VisionManager.addAimNode(self, self.getAttribute("unit.viewrange"))
		else:
			shared.VisionManager.removeAimNode(self)

	#Health
	def _sethealth(self, health):
		if health != self._health:
			self._health = health
			# shared.PlayerManager.Broadcast(4, "recv_unithealth", [self.ID, self._health])

		if health<1:
			self._die()

	def _die(self):
		# print(self.attributes)
		# print("\n\n")
		# print(self._pendingattributes)
		self._syncAttributes() #Sync all last attributes
		self.Hook.call("OnDeath", "LastDamageType Here!")
		shared.DPrint(0, "BaseUnit", "Unit %s:%s died" % (self._owner.username, self.UnitID))
		shared.VisionManager.rmUnit(self)
		if self._group!=None:
			self._group.unitDown(self)
		self._owner.Units.remove(self)

	def _hackishDie(self):
		#DO NOT CALL THIS THING
		#This is only to be used when the action-abort requires unit death!
		self._abortAction = self._____donotcallme
		self.Hook.call("OnDeath", "LastDamageType Here!")
		if self._group!=None:
			self._group.unitDown(self)
		self._owner.Units.remove(self)

	def _____donotcallme(self):
		self._currentaction=None


	## NON-Networked (Mostly stuff handeled by the groupmanager instead)

	# MOVEMENT
	def _steerToPath(self, path):
		# self._movetopoint=pos
		# self._look(self._movetopoint)
		if self.getAttribute("movement.movetype")!=0: #MOVETYPE_AIR
			for node in path:
				self._vehicle.addPosToPath((node[0], self._pos[1], node[1]))
			self.steer_state = "path"
			self.steer_target = None
		else:
			#self._vehicle.seekPos((pos[0], self._pos[1], pos[2]))
			#self.steer_state = "seek"
			#self.steer_target = (pos[0], self._pos[1], pos[1])
			path = [path[len(path)-1]]
			for node in path:
				self._vehicle.addPosToPath((node[0], self._pos[1], node[1]))
			self.steer_state = "path"
			self.steer_target = None
		self.Hook.call("OnMove", path)

	def _moveto(self, pos):
		#Calculates an correct path, and moves according to this
		self._movetopoint = movetypes.Path(self._pos, pos, self.getAttribute("movement.movetype"))

	def _movetowards(self, pos):
		#Moves straight towards position, ignores obstacles
		self._movetopoint=pos
		self._look(self._movetopoint)
		self.Hook.call("OnMove", pos)

	def _stopmove(self):
		self.Hook.call("OnMoveStop", self._movetopoint)
		self._movetopoint=None
		if self._vehicle:
			self._vehicle.Break()
			self._vehicle.clearPath()
			self.steer_state = None
			self.steer_target = None

	def _finishedmove(self):
		self.Hook.call("OnMoveStop", self._movetopoint)
		self._movetopoint=None
		self.steer_state = None
		self.steer_target = None

	# ENTITY
	def _setPosition(self, pos):
		self._pos = pos

	def _look(self, pos):
		self._lookpos = pos

	# ACTIONS

	def _getActionByID(self, aid):
		for action in self._globalactions:
			if action.actionid == aid:
				return action

		for action in self.Actions:
			if action.actionid == aid:
				return action

	def _getAllActions(self):
		allactions = []
		allactions.extend(self._globalactions)
		allactions.extend(self.Actions)
		return allactions

	def _setAction(self, act, evt):
		print("Member: Setting Action")
		if self._currentaction:
			self._currentaction.finish()

		print("Setting Action")
		self._currentaction=act(self, evt)
		print("Beginning Action")
		self._currentaction.begin()
		print("Calling all hooks")
		self.Hook.call("OnActionStart", self._currentaction)
		print("Member: Action Set!")

	def _finishAction(self):
		if self._currentaction!=None:
			self.Hook.call("OnActionFinished", self._currentaction)
			self._currentaction.finish()
			self._currentaction=None

	def _abortAction(self):
		if self._currentaction!=None:
			self.Hook.call("OnActionAbort", self._currentaction)
			self._currentaction.abort()
			self._currentaction=None

	def _sendActionState(self, state, data):
		self.Hook.call("OnActionState", self._currentaction, state, data)
		shared.PlayerManager.Broadcast(4, "recv_updact", [self.ID, state, data])

	# GROUP
	def _changegroup(self, newgroup):
		self.Hook.call("OnGroupChange", newgroup)
		print("CHANGING GROUP from "+str(self._group)+ " to "+str(newgroup))
		if self._group!=None:
			self._group.unitSwitchGroup(self)
		self._group=newgroup