#Director - Launcher
#This is a simple director that allows you to go mad and launch rockets everywhere, and controlling some launcher behaviour from console

from engine import shared, debug
from engine.Object import projectiles
import ogre.renderer.OGRE as ogre
from ogre.gui.CEGUI import MouseCursor
from string import split

class Director():
	def __init__(self):
		self.Active=False

	def Init(self):
		# debug.ACC("dirgo", self.UnitGo, args=2, info="Tell the units directed by SimpleDir to go towards the coordinates")
		# debug.ACC("diraim", self.UnitAim, args=3, info="Tell the units directed by SimpleDir to aim towards the coordinates")
		# debug.ACC("dirpri", self.UnitPri, args=0, info="Tell the units directed by SimpleDir to do the Primary Action")
		# debug.ACC("dirsec", self.UnitPri, args=0, info="Tell the units directed by SimpleDir to do the Secondary Action")
		# debug.ACC("diradd", self.UnitAdd, args=1, info="Add a unit under SimpleDir")
		# debug.ACC("diradde", self.UnitAddEnemy, args=1, info="Add a unit under SimpleDir")
		# debug.ACC("dircls", self.UnitDelAll, args=0, info="Clear/Delete all units directed by SimpleDir")

		self.gotoX=None
		self.gotoY=None
		self.gotoz=None

	def Action(self):
		self.Projectiles=[]
		self.DeadPool=[]
		self.Active=True

	def evt_selected(self, selections, actionQueueing):
		shared.DPrint("LauncherDir", 0, "Nothing Updated")

	def evt_moveclick(self, pos, actionQueueing):
		print("Launching at pos: "+str(pos))
		campos = (shared.render3dCamera.camNode.getPosition().x, shared.render3dCamera.camNode.getPosition().y, shared.render3dCamera.camNode.getPosition().z)
		proj = projectiles.Rocket(campos)
		self.Projectiles.append(proj)
		proj.ignite(pos)

	def evt_actionclick(self, data, actionQueueing):
		mousePos = MouseCursor.getSingleton().getPosition()
		mouseRay = shared.render3dCamera.camera.getCameraToViewportRay(mousePos.d_x / float(self.dimh), mousePos.d_y / float(self.dimv))
		self.raySceneQuery.setRay(mouseRay)
		result = self.raySceneQuery.execute()
		if len(result)>0:
			for item in result:
				if item.movable and not "PDecal" in item.movable.getParentSceneNode().getName():
					hitpoint=mouseRay.intersects(item.movable.getWorldBoundingBox())
					posMoved=mouseRay.getPoint(hitpoint.second)
					pos=(posMoved[0],posMoved[1],posMoved[2])

		print("Launching at pos: "+str(pos))
		campos = (shared.render3dCamera.camNode.getPosition().x, shared.render3dCamera.camNode.getPosition().y, shared.render3dCamera.camNode.getPosition().z)
		proj = projectiles.Rocket(campos)
		self.Projectiles.append(proj)
		proj.ignite(pos)

	def Frame(self):
		#This will get executed each frame
		if self.Active:
			for x in self.DeadPool:
				self.Projectiles.remove(x)

			self.DeadPool=[]

			for x in self.Projectiles:
				if not x._think_():
					self.DeadPool.append(x)