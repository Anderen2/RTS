#Unitmanagermodule - Globalunit
#This is the class which all units derive from and bases itself on
from engine import shared, debug
from engine.World import pathfinding

class GlobalUnit():
	def __init__(self, ID, team, name, ent, pos=None):
		#Setup constants
		self.ID=ID
		self.name=name
		self.team=team
		self.ent=ent
		self.entity=None
		self.hname=shared.unitManager.GetParam(self.name, "name")

		#Start rendering the unit (self, Identifyer, Type, Team, Interactive)
		self.entity=shared.EntityHandeler.Create(self.ID, self.ent, "unit", self.team)
		try:
			if self.entity.error:
				shared.DPrint("Globalunit",4,"Entity error! Unit creation aborted!")
				self._del()
		except:
			shared.DPrint("Globalunit",4,"Entity critical error! Unit creation aborted!")
			self._del()

		#Do some post-render stuff
		self.entity.CreateTextOverlay()
		if pos==None:
			self.entity.RandomPlacement()
		else:
			self._setPos(pos[0], pos[1], pos[2])
		self.entity.text.setText(self.name+" "+str(ID))

		#Sound:
		#self.snd=shared.SoundEntMgr.Create

		#Phys:
		#self.phys=shared.PhysicsEntMgr.Create

		#Movement
		self.nextwaypoint=None

		#Start unit-dependant shit:
		self.init()

		#Notify that we have successfuly created a unit!
		shared.DPrint("Globalunit",5,"Unit created! ID="+str(self.ID))

	def _think(self):
		self.entity.text.update()
		self.entity.Think()
		if self.nextwaypoint!=None:
			if self._movetowards(self.nextwaypoint[0], self.nextwaypoint[2])<1:
				self.nextwaypoint=None
		

	def _selected(self):
		shared.DPrint("Globalunit",5,"Unit selected: "+str(self.ID))
		self.entity.text.enable(True)
		if debug.AABB:
			self.entity.node.showBoundingBox(True)
		self.entity.rotTurret(60)

	def _deselected(self):
		shared.DPrint("Globalunit",5,"Unit deselected: "+str(self.ID))
		self.entity.text.enable(False)
		if debug.AABB:
			self.entity.node.showBoundingBox(False)
		#self.entity.actNone()
		#self.entity.actDead(True)
		#self.entity.rotTurret(60)

	def _setPos(self, x, y, z):
		self.entity.SetPosition(float(x), float(y), float(z))
		shared.FowManager.nodeUpdate(self.entity.node)

	def _setRot(self, rotx, roty, rotz):
		self.entity.Rotate(float(rotx), float(roty), float(rotz))

	def _movetowards(self, x, z):
		self.entity.actNone()
		self.entity.actMove(True)
		src=self.entity.node.getPosition()
		src2d=(src[0], src[2]) #2D Coordinates (X, Z) or Longitude and Latitude (Not Altitude!)
		xzd=pathfinding.GetNextCoord(src2d, (x,z)) #Returns next Xcoord, Zcoord and a measure of how much distance which is left (x, z, dist)
		if xzd[0]>src[0]-1 or xzd[1]>src[2]-1 or xzd[0]<src[0]+1 or xzd[1]<src[2]+1:
			self._look(xzd[0], src[1], xzd[1])
		self._setPos(xzd[0], src[1], xzd[1])
		return xzd[2]

	def _setwaypoint(self, pos):
		self.nextwaypoint=pos

	def _move(self):
		pass

	def _look(self, x, y, z):
		self.entity.LookAtZ(x, y, z)

	def _act1(self):
		pass

	def _act2(self):
		pass

	def _act3(self):
		pass

	def _act4(self):
		pass

	def _damage(self, dmg):
		pass

	def _dead(self):
		pass

	def _del(self):
		shared.DPrint("Globalunit",5,"Unit deleted: "+str(self.ID))

		try:
			xExsist=None
			for x in shared.render3dSelectStuff.CurrentSelection:
				if self.entity.node.getName() == x.getName():
					xExsist=x
			if xExsist!=None:
				shared.render3dSelectStuff.CurrentSelection.remove(xExsist)

			if not entity.error:
				self.entity.Delete()
			shared.unitManager.Delete(self.ID)
		except:
			shared.DPrint("Globalunit",5,"Unit Deletion Failed! Unit may still be in memory and/or in game world!")

	def __del__(self):
		shared.DPrint("Globalunit",5,"Unit gc'd: "+str(self.ID))