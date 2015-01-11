#BaseUnit - Clientside
#This is the class which all units derive from and bases itself on
from sys import getrefcount
from random import randrange
from twisted.internet import reactor
from traceback import print_exc
from engine import shared, debug
from engine.shared import Vector
from engine.Lib.hook import Hook
from engine.Object.unitact import cl_move, cl_fau
from engine.Object import moveeff
from engine.World import movetypes

class BaseUnit():
	#Setup Constants
	MOVETYPE_AIR = 0
		
	def __init__(self, ID, owner, pos):
		#Setup variables
		self.ID=int(ID)
		self._owner=owner
		self._group=None
		self._text = ""
		self._isAlive = True

		#Initialize hooks
		self._inithooks()

		#Actions
		self._currentaction=None
		self._globalactions = [cl_move.Action, cl_fau.Action]

		#Movement
		self._vehicle = shared.VehicleManager.create(pos)
		self._movetopoint=None

		#Visibility, minimap and FOW
		self._visible = True
		self._unitIndicator = None

		#MoveEffects
		self._currentmoveeff = None

		#State
		self._health=100 #Bogus value, Getting this from attributes instead See: UnitManager
		self.steer_state = False

		self.attributes={} #All current attributes (Used for gamestate syncing)
		self.attributes["default"] = {}
		self.attributes["current"] = {}
		self.attributes["readonly"] = {}
		self._attributehook = Hook(self.attributes)

		self.addAttributeListener("unit.health", self._setHealth)

		self.Initialize(self.ID)

		shared.DPrint(0, "BaseUnit", "Initialized "+str(self.ID))
		self._setPosition(pos)
		self.Hook.call("OnCreation", pos)

	def _inithooks(self):
		self.Hook = Hook(self)
		#Shared
		self.Hook.new("Initialize", 1)
		self.Hook.new("OnCreation", 1)
		self.Hook.new("OnThink", 1)
		self.Hook.new("OnMoving", 0)
		self.Hook.new("OnHealthChange", 1)
		self.Hook.new("OnDamage", 2)
		self.Hook.new("OnDeath", 1)
		self.Hook.new("OnActionStart", 1)
		self.Hook.new("OnActionAbort", 1)
		self.Hook.new("OnActionFinished", 1)
		#self.Hook.new("OnActionState", 3) Currently Serverside Only
		self.Hook.new("OnServerUpdate", 1)
		self.Hook.new("OnGroupChange", 1)
		self.Hook.new("OnMove", 1)
		self.Hook.new("OnMoveStop", 1)
		self.Hook.new("OnConvertStart", 1)
		self.Hook.new("OnConverted", 1)

		#Clientside
		self.Hook.new("OnMoveEffectStart", 1)
		self.Hook.new("OnMoveEffectDone", 1)
		self.Hook.new("OnSelected", 0)
		self.Hook.new("OnDeselected", 0)

	### UnitScript Functions
	def GetID(self):
		return int(self.ID)

	def GetOwner(self):
		return self._owner

	def GetTeam(self):
		return self._owner.team

	def GetPosition(self):
		return self._getPosition()

	def SetEntity(self, ent):
		self._entityname = ent
		self._entity=shared.EntityHandeler.Create(self.ID, ent, "unit", self.GetTeam())
		try:
			if self._entity.error:
				shared.DPrint("Globalunit",4,"Entity error! Unit creation aborted!")
				self._del()

			self._entity.CreateTextOverlay()
		except:
			shared.DPrint("Globalunit",4,"Entity critical error! Unit creation aborted!")
			self._del()

	def GetEntity(self):
		return self._entity

	def SetSelectedText(self, text):
		self._text=text

	def GetSolid(self):
		return self._solidentity

	def GetMoveType(self):
		return self.getAttribute("movement.movetype")

	def GetMoveSpeed(self):
		return self.getAttribute("movement.movespeed")

	def GetHealth(self):
		return self._health

	def GetViewRange(self):
		return self._viewrange

	def GetState(self):
		if self._movetopoint!=None:
			return "Moving"
		else:
			return "Idle"

	def StartMoveEffect(self, mveff):
		self._currentmoveeff = self._getMoveEffect(mveff)
		self.Hook.call("OnMoveEffectStart", mveff)

	def Destroy(self):
		self._rm()

	### Trigger Hooks
	def _setVisible(self, visible):
		self._visible = visible
		self._entity.node.setVisible(visible)
		if self._unitIndicator:
			self._unitIndicator.update()
		#print("I now have Visibility set to %s!" % str(visible))

	def _selected(self):
		self.Hook.call("OnSelected")
		shared.DPrint("Globalunit",5,"Unit selected: "+str(self.ID))
		self._entity.text.enable(True)
		self._updateText()
		if debug.AABB:
			self._entity.node.showBoundingBox(True)

	def _deselected(self):
		self.Hook.call("OnDeselected")
		shared.DPrint("Globalunit",5,"Unit deselected: "+str(self.ID))
		self._entity.text.enable(False)
		if debug.AABB:
			self._entity.node.showBoundingBox(False)

	def _hover(self):
		self.Hook.call("OnMouseHover")

	def _think(self, delta):
		self.Hook.call("OnThink", delta) #Additional THINK Calls [??]
		self._entity.Think(delta) #Additional THINK Calls [??]
		if self._currentaction!=None:
			self._currentaction.update() #Additional THINK Calls [??]

		if self._vehicle!=None and self.getAttribute("movement.movetype")!=-1:
			if self.steer_state == "path":
				self._vehicle.followPath(delta, towards=self.getAttribute("movement.movetype")==0)

			elif self.steer_state == "seek":
				self._vehicle.seekPos(self.steer_target)

			elif self.steer_state == None:
				#print("Should stop here")
				self._vehicle.Break()

			if self.steer_state == None and self._vehicle.velocity.length()==0:
				#print("\nStopped entirely!\n")
				pass

			else:
				newpos = self._vehicle.step(delta)
				newdir = self._vehicle.velocity.asTuple()

				self._entity.RotateTowardsDirection(newdir[0], 0, newdir[2])

				if not self.getAttribute("movement.constantaltitude"):
					y = shared.render3dTerrain.getHeightAtPos(newpos[0], newpos[2])+1
				else:
					y = shared.render3dTerrain.getHeightAtPos(newpos[0], newpos[2]) + self.getAttribute("movement.constantaltitude")

				self._setPosition((newpos[0], y, newpos[2]))
				
				if len(self._vehicle.path)==0:
					pass

				if newdir != (0,0,0):
					self.Hook.call("OnMoving")

		if self._movetopoint!=None:
			if type(self._movetopoint)!=list:
				dist, pos = movetypes.Move(self._pos, self._movetopoint, self.getAttribute("movement.movespeed")*delta, self.getAttribute("movement.movetype"))
				self._setPosition(pos)
				print self._pos

				if dist<1:
					self._movetopoint=None
			else:
				dist, self._pos = movetypes.Move(self._pos, self._movetopoint[0], self.getAttribute("movement.movespeed")*delta, self.getAttribute("movement.movetype"))

				if dist<1:
					self._movetopoint.pop(0)
					
					if len(self._movetopoint) == 0:
						self._movetopoint = None

		if self._currentmoveeff!=None:
			if self._currentmoveeff(self._entity, delta):
				self.Hook.call("OnMoveEffectDone", self._currentmoveeff.func_name)
				self._currentmoveeff=None

	def _updateText(self):
		self._entity.text.setText(self._text+": HP "+str(self.GetHealth()))

	### Internal Functions

	# Health
	def _setHealth(self, health):
		self.Hook.call("OnDamage", health, "DamageType Here!")
		self._health=health
		self._updateText()
		if self._health<1:
			self._predie()

			dieAction = self.Hook.call("OnDeath", "LastDamageType Here!")
			if not dieAction:
				self._die()
			else:
				print("convertToDecoration")
				dec = shared.decHandeler.Import(self._entity)
				dec.sinkSlowly(10)

				temp = self._entity
				#shared.EntityHandeler.entsWithNoOwner.append(self._entity)
				#reactor.callLater(5, lambda: shared.EntityHandeler.Destroy(temp))
				self._entity = None
				self._die()



	def _predie(self):
		#Removing from interaction with game
		shared.DirectorManager.CurrentDirector.deselectUnit(self)
		if self._group:
			self._group.rmUnit(self)
		self._movetopoint=None

		if shared.FowManager!=None and shared.FowManager!=True:
			shared.FowManager.rmNode(self._entity.node)

		if shared.MinimapManager!=None and self._unitIndicator!=None:
			self._unitIndicator.remove()

		self._isAlive = False

	def _die(self):
		shared.DPrint("BaseUnit", 0, "_die")
		self._rm()

	def _rm(self):
		#Removing all visuals and itself
		shared.DPrint("BaseUnit", 0, "_rm - Units remove self")
		self._owner.Units.remove(self)
		shared.DPrint("BaseUnit", 0, "Removing all hooks")
		self.Hook.removeAll()

		shared.DPrint("BaseUnit", 0, "Entity delete")
		if self._entity!=None:
			self._entity.Delete()
			print("Dead Referances: "+str(getrefcount(self)))

	# Movement
	def _steerToPath(self, path):
		#self._movetopoint=pos
		#self._look(self._movetopoint)
		if self.getAttribute("movement.movetype")!=0:
			for node in path:
				self._vehicle.addPosToPath((node[0], self._pos[1], node[1]))
			self.steer_state = "path"
			self.steer_target = None
		else: 
			# self._vehicle.seekPos((pos[0], self._pos[1], pos[2]))
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

	def _getMoveEffect(self, mveff):
		if mveff in dir(moveeff):
			return getattr(moveeff, mveff)

	# ENTITY
	def _setPosition(self, pos):
		self._pos=pos
		self._entity.SetPosition(pos[0], pos[1], pos[2])
		if shared.FowManager!=None and shared.FowManager!=True:
			shared.FowManager.nodeUpdate(self._entity.node)

		if shared.MinimapManager!=None and self._unitIndicator!=None:
			self._unitIndicator.update()

	def _getPosition(self):
		self._pos = self._entity.GetPosition()
		return self._pos

	def _setrotation(self, rot):
		self._entity.Rotate(rot[0], rot[1], rot[2])

	def _look(self, pos):
		if len(pos) == 3:
			self._entity.LookAtZ(pos[0], pos[1], pos[2])
		else:
			self._entity.LookAtZ(pos[0], self._getPosition()[1], pos[1])

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
		self._currentaction=act(self, evt)
		self._currentaction.begin()
		self.Hook.call("OnActionStart", self._currentaction)

	def _finishAction(self):
		self.Hook.call("OnActionFinished", self._currentaction)
		if self._currentaction!=None:
			self._currentaction.finish()
			self._currentaction=None

	def _abortAction(self):
		self.Hook.call("OnActionAbort", self._currentaction)
		if self._currentaction!=None:
			self._currentaction.abort()
			self._currentaction=None

	# GROUP
	def _changegroup(self, newgroup):
		self.Hook.call("OnGroupChange", newgroup)
		print("CHANGING GROUP from "+str(self._group)+ " to "+str(newgroup))
		if self._group!=None:
			self._group.rmUnit(self)
		self._group=newgroup

	#Attributes
	def setAttribute(self, attribname, value):
		#Request server modify of attribute
		pass

	def getAttribute(self, attribname):
		return self.attributes["current"][attribname]

	def resetAttribute(self, attribname):
		#Request server reset of attribute
		pass

	def addAttributeListener(self, attribname, func):
		if self._attributehook.doesExist(attribname):
			self._attributehook.Add(attribname, func)
		else:
			self._attributehook.new(attribname, 1)
			self._attributehook.Add(attribname, func)

	def fullAttributeResync(self):
		#Request an full resync of all attributes
		pass

	def _serverAttributeSync(self, attributes, inital=False):
		self.attributes["current"].update(attributes)
		for attribname, value in attributes.iteritems():
			shared.DPrint("baseunit", 0, "Attribute S(%s:%i): %s = %s" % (self.UnitID, self.ID, attribname, str(value)))
			self._actOnAttribute(attribname)
			if self._attributehook.doesExist(attribname):
				self._attributehook.call(attribname, value)

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

		if attrib[0]=="unit":
			if attrib[1]=="position": 
				self._setPosition(self.getAttribute(attribname))
			elif attrib[1]=="viewrange":
				print("Setting viewrange")
				if shared.FowManager!=None and shared.FowManager!=True:
					shared.FowManager.chViewSize(self._entity.node, self.getAttribute(attribname))


	#Other
	def _randomCallback(self, tmin, tmax, call):
		reactor.callLater(randrange(tmin, tmax, 1), call)