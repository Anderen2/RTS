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
		self._constantaltitude = False
		self._health = 100
		self.steer_state = False
		self.pendingattrib={} #All attributes waiting to be sent
		self.currentattrib={} #All current attributes (Used for gamestate syncing)

		self.Initialize(self.ID)
		shared.DPrint(0, "BaseUnit", "Initialized "+str(self.ID))
		self._setPosition(pos)
		self.Hook.call("OnCreation", self._pos)

	def _inithooks(self):
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


	### UnitScript Functions
	def SetPosition(self, x, y, z):
		self._setPosition((x,y,z))
		self._updateAttrib("pos", (x,y,z))

	def GetPosition(self):
		return self._pos

	def SetEntity(self, ent):
		#Setup Pathfinding variables here (sizes, etc)
		self._entityname = ent
		shared.DPrint(0, "BaseUnit", "UnitID: "+str(self.ID)+" = "+str(ent))
		self._updateAttrib("entityname", ent)

	def SetSolid(self, yn):
		self._solidentity=yn
		self._updateAttrib("solidentity", yn)

	def SetConstantAltitude(self, altitude):
		self._constantaltitude = altitude
		self._updateAttrib("constantaltitude", altitude)

	def SetMoveType(self, movetype):
		#Setup Pathfinding algorthim based on the movetype here
		self._movetype = movetype
		self._updateAttrib("movetype", movetype)

	def SetMoveSpeed(self, speed):
		#Setup Pathfinding movespeed here
		self._movespeed = speed
		self._updateAttrib("movespeed", speed)

	def SetMaxHealth(self, health):
		self._health = health
		self._updateAttrib("health", health)

	def SetHealth(self, health):
		self.Hook.call("OnHealthChange", health)
		self._sethealth(health)

	def TakeDamage(self, damage):
		self.Hook.call("OnDamage", damage, "DamageType Here!")
		self._sethealth(self._health-damage)

	def SetViewRange(self, viewrange):
		self._viewrange = viewrange
		self._updateAttrib("viewrange", viewrange)

	def SetVehicleSize(self, size):
		self._vehicle.size = size
		self._updateAttrib("vehicle.size", size)

	def SetVehicleMaxForce(self, maxforce):
		self._vehicle.max_force = maxforce
		self._updateAttrib("vehicle.max_force", maxforce)

	def SetVehicleMass(self, mass):
		self._vehicle.mass = mass
		self._updateAttrib("vehicle.mass", mass)

	def SetVehiclePathNodeRadius(self, pnr):
		self._vehicle.path_node_radius = pnr
		self._updateAttrib("vehicle.path_node_radius", pnr)

	def SetVehicleArriveBreakingRadius(self, abr):
		self._vehicle.arrive_breaking_radius = abr
		self._updateAttrib("vehicle.arrive_breaking_radius", abr)

	def SetVehicleMaxVelocity(self, maxvelocity):
		self._vehicle.max_velocity = maxvelocity
		self._updateAttrib("vehicle.max_velocity", maxvelocity)

	def SetVehicleMaxSpeed(self, maxspeed):
		self._vehicle.max_speed = maxspeed
		self._updateAttrib("vehicle.max_speed", maxspeed)

	def SetVehicleBreakingForce(self, breaks):
		self._vehicle.breaking_force = breaks
		self._updateAttrib("vehicle.breaking_force", breaks)

	def SetVehicleMaxSeeAhead(self, msa):
		self._vehicle.max_see_ahead = msa
		self._updateAttrib("vehicle.max_see_ahead", msa)

	def SetVehicleMaxAvoidForce(self, maf):
		self._vehicle.max_avoid_force = maf
		self._updateAttrib("vehicle.max_avoid_force", maf)

	def CreateProjectileLauncher(self, type):
		launcher = shared.LauncherManager.create(type, self)
		return launcher

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

		if self._vehicle!=None:
			if self.steer_state == "path":
				self._vehicle.followPath(delta, towards=self._movetype==0)

			elif self.steer_state == "seek":
				self._vehicle.seekPos(self.steer_target)

			newpos = self._vehicle.step(delta)
			if newpos!=self.__oldsteeringpos:
				self.__oldsteeringpos = newpos

				if not self._constantaltitude:
					y = shared.Map.Terrain.getHeightAtPos(newpos[0], newpos[2])+1
				else:
					y = shared.Map.Terrain.getHeightAtPos(newpos[0], newpos[2]) + self._constantaltitude

				self._setPosition((newpos[0], y, newpos[2]))

		if self._movetopoint!=None:
			if type(self._movetopoint)!=list:
				dist, self._pos = movetypes.Move(self._pos, self._movetopoint, self._movespeed*delta, self._movetype)
				print(self._pos)

				if dist<1:
					self._movetopoint=None
			else:
				dist, self._pos = movetypes.Move(self._pos, self._movetopoint[0], self._movespeed*delta, self._movetype)

				if dist<1:
					self._movetopoint.pop(0)
					
					if len(self._movetopoint) == 0:
						self._movetopoint = None

	def _actionfinish(self):
		if self._group!=None:
			self._group.unitActionDone(self)

	### Internal Functions

	## Networked

	#Unit Attributes
	def _updateAttrib(self, attribname, data):
		if len(self.pendingattrib)==0:
			#The reason for why we do this is to collect all attribute changes in one frame and send them all in one package.
			#As the client seemly only could recieve 60 pkgs each secound [With the current transferring method], we keep the packagequeue from getting too big
			reactor.callLater(0.1, self._broadcastAttrib)
		self.pendingattrib[attribname]=data
		self.currentattrib[attribname]=data

	def _broadcastAttrib(self):
		if len(self.pendingattrib)!=0:
			self.Hook.call("OnServerUpdate", self.pendingattrib.copy())
			shared.PlayerManager.Broadcast(4, "recv_attrib", [self.ID, self.pendingattrib.copy()])
			self.pendingattrib={}

	#Health
	def _sethealth(self, health):
		if health != self._health:
			self._health = health
			shared.PlayerManager.Broadcast(4, "recv_unithealth", [self.ID, self._health])

		if health<1:
			self._die()

	def _die(self):
		self.Hook.call("OnDeath", "LastDamageType Here!")
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
		if self._movetype!=0: #MOVETYPE_AIR
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
		self._movetopoint = movetypes.Path(self._pos, pos, self._movetype)

	def _movetowards(self, pos):
		#Moves straight towards position, ignores obstacles
		self._movetopoint=pos
		self._look(self._movetopoint)
		self.Hook.call("OnMove", pos)

	def _stopmove(self):
		self.Hook.call("OnMoveStop", self._movetopoint)
		self._movetopoint=None
		if self._vehicle:
			self._vehicle.clearPath()
			self.steer_state = None
			self.steer_target = None


	# ENTITY
	def _setPosition(self, pos):
		self._pos = pos

	def _look(self, pos):
		self._lookpos = pos

	# ACTIONS
	def _loadActions(self):
		pass

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