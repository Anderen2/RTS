#Serverside Projectiles/Launchers

from time import time
from twisted.internet import reactor
from engine import shared, debug
from engine.World import posalgo

class LauncherManager():
	UNITLAUNCHER = 1
	SUPERWEAPONLAUNCHER = 2
	def __init__(self):
		shared.LauncherManager = self
		shared.objectManager.addEntry(0, 6, self)
		self.projectilecount = 0
		self.ProjectilesAvailible={"rocket":Rocket}

	def create(self, type, unit):
		if type == self.UNITLAUNCHER:
			return UnitLauncher(unit)
		
class UnitLauncher():
	def __init__(self, unit):
		shared.DPrint("Projectiles", 0, "Projectile Launcher Created")
		self.Projectiles=[]
		self.lastframe=time()
		reactor.callLater(0, self.update)
		self.unit = unit

		#Defaults
		self.pos = unit._pos
		self.oldunitpos = self.pos
		self.trans = (0,0,0)
		self.rot = (0,0,0)
		self.projtype=Rocket
		self.firerange=100
		self.firespeed=1
		self.reloadspeed=2
		self.magcap=10
		self.rellive=True

		self.dmgradius=10
		self.dmgdrain = 50
		self.dmgrelative = False

		#Variables
		self.magazine=self.magcap
		self.lastfired=time()
		self.reloading=False
		self.uidcount = 0

	#Sets And Gets
	def SetPosition(self, x, y, z):
		"""Set Launchers position (Relative to unit pos)"""
		self.trans = (x,y,z)
		print("Unit: "+str(self.unit._pos))
		print("Trans: "+str(self.trans))
		self.pos=tuple(map(sum, zip(self.unit._pos, self.trans)))
		print("Result: "+str(self.pos))

	def SetRotation(self, x, y, z):
		"""Set Launchers rotation (Relative to unit rot)"""
		self.rot = (x, y, z)

	def SetProjectile(self, projtype):
		"""Set Launchers projectile"""
		if projtype in shared.LauncherManager.ProjectilesAvailible:
			self.projtype=shared.LauncherManager.ProjectilesAvailible[projtype]
		else:
			return False

	def SetFireRange(self, firerange):
		"""Set Launchers Fire Range (Max. fire distance)"""
		self.firerange=firerange

	def SetFiringSpeed(self, firespeed):
		"""Set Launchers Firing speed (Time between projectile fires)"""
		self.firespeed=firespeed

	def SetReloadingSpeed(self, reloadspeed):
		"""Set Launchers reloading speed (Time to wait after magazine is empty)"""
		self.reloadspeed=reloadspeed

	def SetMagasineCapasity(self, magcap):
		"""Set Launchers magazine capasity (Set this to -1 if you do not want reloading)"""
		self.magcap=magcap

	def CanReloadLive(self, rellive):
		"""Set if the launcher can reload while on the move, or if it needs some kind of 
		condition to be in before being able to reload"""
		self.rellive=rellive

	def SetDamageRadius(self, radius):
		"""Set the how big the radius for the damage is (0 for only damaging what it hit)"""
		self.dmgradius=radius

	def SetDamageHealth(self, dmg):
		"""Set how much health the projectile should drain from what it hits"""
		self.dmgdrain=dmg

	def SetRelativeDamage(self, reldam):
		"""Set if damage is relative to how close it is to the center of the radius"""
		self.dmgrelative=reldam

	#Actions
	def Reload(self):
		if self.reloading==False and self.magazine<self.magcap:
			self.reloading=time()
			shared.DPrint("Projectiles", 0, "Reloading..")
		elif (time()-self.reloading)>self.reloadspeed:
			self.magazine=self.magcap
			self.reloading=False
			shared.DPrint("Projectiles", 0, "Reloaded!")
			return True
		return False


	def FireAtPos(self, x, y, z):
		pos = (x,y,z)
		if self.isAbleToFire(pos):
			projectile = self.createProjectile(self.pos)
			projectile.ignite(pos)
		else:
			pass
			#Move closer to target

	def FireAtUnit(self, unit):
		if self.isAbleToFireAtUnit(unit):
			if self.isAbleToFire(unit._pos):
				projectile = self.createProjectile(self.pos)
				projectile.ignite(unit)
			else:
				pass
				#Move closer to target
			
	def update(self):
		deltatime = time()-self.lastframe
		self.lastframe=time()

		for projectile in self.Projectiles:
			projectile._think(deltatime)
		reactor.callLater(0, self.update)

		if self.oldunitpos!=self.unit._pos:
			self.pos=tuple(map(sum, zip(self.unit._pos, self.trans)))
			self.oldunitpos=self.unit._pos

	#Internal Functions
	def createProjectile(self, pos):
		uid = shared.LauncherManager.projectilecount
		#shared.DPrint("Projectiles", 0, "Creating projectile: "+str(uid))
		projectile = self.projtype(self.pos, uid, self)
		self.Projectiles.append(projectile)
		shared.LauncherManager.projectilecount+=1
		return projectile

	def isAbleToFireAtUnit(self, unit):
		if unit._owner.team!=self.unit._owner.team:
			return True
		else:
			#shared.DPrint("Projectiles", 0, "Friendly fire")
			return True
			#return False

	def isAbleToFire(self, pos):
		#If free line of fire:
		if posalgo.in_circle(self.pos[0], self.pos[2], self.firerange, pos[0], pos[2]):
			if (time()-self.lastfired)>self.firespeed:
				self.lastfired=time()
				if self.magazine>0:
					self.magazine-=1
					return True
				else:
					return self.Reload()

		return False

	def removeProjectile(self, projectile):
		self.Projectiles.remove(projectile)

	def generateDamageSquare(self, centerpos):
		dist = self.dmgradius/2
		TopX = centerpos[0]+dist
		TopY = centerpos[2]+dist
		BtmX = centerpos[0]-dist
		BtmY = centerpos[2]-dist

		print "\n\n\n\n"
		print "Generating Damage Square"
		print "centerpos: "+str(centerpos)
		print "Dist: "+str(dist)
		print ((TopX, TopY), (BtmX, BtmY))

		return ((TopX, TopY), (BtmX, BtmY))

	def calculateRelativeDamage(self, dmgsquare, position):
		pass

	#Triggers
	def projectileExploded(self, projectile):
		if self.dmgradius!=None and self.dmgradius!=0:
			dmgsquare = self.generateDamageSquare(projectile.pos)
			for unit in shared.UnitManager.generateUnitsWithin(dmgsquare):
				print "\n\n\n\n"
				print "Unit is within DMGSQARE"
				print unit.ID
				print unit._pos
				print dmgsquare
				if not self.dmgrelative:
					unit.TakeDamage(self.dmgdrain)
				else:
					self.calculateRelativeDamage(dmgsquare, unit._pos)
		else:
			unit = shared.UnitManager.getUnitAtPos(projectile.pos)
			if unit:
				unit.TakeDamage(self.dmgdrain)

class Rocket():
	S_ARMED = 3
	S_IGNITED = 2
	S_TARGETHIT = 1
	S_EXPLODED = 0
	S_GC = -1

	def __init__(self, position, uid, launcher):
		self.pos = position
		self.uid = uid
		self.launcher = launcher
		self.target = None
		self.oldstate = None
		self.state = None

		self._setState(self.S_ARMED)

		self.speed = 100

	def ignite(self, target):
		if self.state == self.S_ARMED:
			if type(target) == tuple:
				self.target = target
				self._setState(self.S_IGNITED)

			else:
				self.target = target._pos
				self._setState(self.S_IGNITED)

	def _setState(self, state):
		if self.oldstate!=state:
			#shared.DPrint("Projectile", 0, "Projectile: "+str(self.uid)+" at state: "+str(state))
			if state == self.S_IGNITED:
				shared.PlayerManager.Broadcast(6, "recv_rocket", [self.uid, self.pos, self.target, self.speed])
			elif state == self.S_EXPLODED:
				shared.PlayerManager.Broadcast(6, "recv_explode", [self.uid, self.pos])
			self.oldstate = self.state
			self.state = state

	def _think(self, delta):
		if self.state == self.S_IGNITED:
			if self.target!=None:
				dist = self._movestep(self.target, delta)
				if dist<1:
					self._setState(self.S_TARGETHIT)

		if self.state == self.S_TARGETHIT:
			self._explode()

	def _movestep(self, dst, delta):
		src = self.pos
		speed = (self.speed*delta)
		nx, ny, nz, dist = shared.Pathfinder.ABPath.GetNextCoord3D(src, dst, speed)
		newpos = (nx, ny, nz)
		
		self.pos = newpos
		return dist

	def _explode(self):
		self._setState(self.S_EXPLODED)
		self.launcher.projectileExploded(self)
		reactor.callLater(5, self._blown)

	def _blown(self):
		self._setState(self.S_GC)
		self.launcher.removeProjectile(self)