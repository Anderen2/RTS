#Render3dExtension - render3dent
#Classes for handeling Entitys
#Lowlevel Module (Text)

import render3dtext as text
from engine import shared, debug
from engine.shared import DPrint
from engine.shared import Vector
from engine.Lib import YModConfig
from random import randrange
from traceback import format_exc
import ogre.renderer.OGRE as ogre

#Entity QueryFlags
MASK_UNIT = 1 << 1 #All units
MASK_DECO = 1 << 2 #All map decorators
MASK_OTHER = 1 << 3 #All other entitys
MASK_GADGET = 1 << 4 #All entity additonal entitys/meshes (ex. the tank turret)

class EntityHandeler():
	def ReadEntitys(self):
		self.parser=YModConfig.Parser("Data/Ent/","ent")
		self.EntDict=self.parser.start()
		if self.EntDict==False:
			shared.DPrint("Render3dEnt", 3, "Parsing files failed!")

	def GetParam(self, ent, key):
		return self.EntDict[ent][key]

	def GetParams(self, ent):
		return self.EntDict[ent]

	def Create(self, Identifyer, Type, Interactive, Team=None):
		shared.DPrint("Render3dEnt",0,"Creating Entity: "+str(Interactive)+":"+Type+" ["+str(Identifyer)+"]")
		ent=Entity(Identifyer, Type, Team, Interactive)
		return ent

	def Destroy(self, Identifyer):
		pass

class Entity():
 	def __init__(self, Identifyer, Type, Team, Interactive):
 		EntImporter=1.1
 		self.ID=Identifyer
 		self.Team=Team
 		self.Type=Type
 		self.text=None

 		#Used in movement effects
 		self.lastMovementDirection = Vector(0,0,0)

 		DPrint("Entity",0,"Loading Entity: "+str(self.Type))
 		try:
 			self.params=shared.EntityHandeler.GetParams(self.Type)
 			self.filever=self.params["version"]
	 		DPrint("Entity",0,"	EntityFile v."+str(self.filever))
	 		DPrint("Entity",0,"	Mesh: "+str(self.params["mesh"]))
			self.mesh=shared.render3dScene.sceneManager.createEntity(Interactive+str(Identifyer), self.params["mesh"])
			self.shadows=self.params["shadows"]
			self.mesh.setCastShadows(self.shadows)
			self.node=shared.render3dScene.sceneManager.getSceneNode("EntNode").createChildSceneNode(Interactive+"Node_"+str(Identifyer))
			self.node.attachObject(self.mesh)
			self.node.scale(self.params["meshscale"][0],self.params["meshscale"][1],self.params["meshscale"][2])
			self.meshturret=None
			self.nodeturret=None

			if Interactive == "unit":
				self.mesh.setQueryFlags(MASK_UNIT)
			elif Interactive == "deco":
				self.mesh.setQueryFlags(MASK_DECO)
			else:
				self.mesh.setQueryFlags(MASK_OTHER)

			if not self.params["meshturret"]==None:
				DPrint("Entity",0,"	MeshTurret")
				self.meshturret=shared.render3dScene.sceneManager.createEntity(Interactive+str(Identifyer)+"-turret", self.params["meshturret"])
				self.meshturret.setCastShadows(self.shadows)
				self.meshturret.setQueryFlags(MASK_GADGET)
				self.nodeturret=self.node.createChildSceneNode(Interactive+"Node-Turret_"+str(Identifyer))
				self.nodeturret.attachObject(self.meshturret)
				
			self.meshes=[]
			self.meshnodes=[]
			if not self.params["addmesh"]==None:
				for x in range(0, self.params["addmesh"]):
					y=x+1
					DPrint("Entity",0,"	AddMesh: "+str(y))
					mesh=shared.render3dScene.sceneManager.createEntity(Interactive+str(Identifyer)+"-addmesh"+str(y), self.params["mesh"+str(y)])
					mesh.setCastShadows(self.shadows)
					node=self.node.createChildSceneNode(Interactive+"Node-Mesh"+str(y)+"_"+str(Identifyer))
					node.attachObject(mesh)
					self.meshes.append(mesh)
					self.meshnodes.append(node)
			self.movepart=[]
			self.movepartnode=[]
	 		if not self.params["moveeff"]==None:
	 			DPrint("Entity",0,"	MoveEffect")
	 			movepart=shared.render3dScene.sceneManager.createParticleSystem("moveeff0-"+str(self.ID)+"-"+str(Interactive),self.params["moveeff"])
				movepartnode=self.node.createChildSceneNode()
				movepart.getEmitter(0).setTimeToLive(self.params["moveefftime"])
				movepart.getEmitter(0).setEnabled(False)
				movepartnode.setPosition(self.params["moveeffpos"])
				movepartnode.rotate((1,0,0),ogre.Degree(self.params["moveeffrot"][0]))
				movepartnode.rotate((0,1,0),ogre.Degree(self.params["moveeffrot"][1]))
				movepartnode.rotate((0,0,1),ogre.Degree(self.params["moveeffrot"][2]))
				movepartnode.attachObject(movepart)
				self.movepart.append(movepart)
				self.movepartnode.append(movepartnode)
				for x in range(0,self.params["addmoveeff"]):
					y=x+1
					print(y)
					DPrint("Entity",0,"	AddMoveEffect: "+str(y))
					movepart=shared.render3dScene.sceneManager.createParticleSystem("moveeff"+str(y)+"-"+str(self.ID)+"-"+str(Interactive),self.params["moveeff"+str(y)])
					movepartnode=self.node.createChildSceneNode()
					movepart.getEmitter(0).setTimeToLive(self.params["moveefftime"+str(y)])
					movepart.getEmitter(0).setEnabled(False)
					movepartnode.setPosition(self.params["moveeffpos"+str(y)])
					movepartnode.rotate((1,0,0),ogre.Degree(self.params["moveeffrot"+str(y)][0]))
					movepartnode.rotate((0,1,0),ogre.Degree(self.params["moveeffrot"+str(y)][1]))
					movepartnode.rotate((0,0,1),ogre.Degree(self.params["moveeffrot"+str(y)][2]))
					movepartnode.attachObject(movepart)
					self.movepart.append(movepart)
					self.movepartnode.append(movepartnode)

			self.dieeff=None
			self.dieeffnode=None
			if not self.params["dieeff"]==None:
				DPrint("Entity",0,"	DieEffect")
				dieeff=shared.render3dScene.sceneManager.createParticleSystem("dieeff0-"+str(self.ID)+"-"+str(Interactive),self.params["dieeff"])
				dieeffnode=self.node.createChildSceneNode()
				dieeff.getEmitter(0).setTimeToLive(self.params["dieefftime"])
				dieeff.getEmitter(0).setEnabled(False)
				dieeffnode.setPosition(self.params["dieeffpos"])
				dieeffnode.rotate((1,0,0),ogre.Degree(self.params["dieeffrot"][0]))
				dieeffnode.rotate((0,1,0),ogre.Degree(self.params["dieeffrot"][1]))
				dieeffnode.rotate((0,0,1),ogre.Degree(self.params["dieeffrot"][2]))
				dieeffnode.attachObject(dieeff)
				self.dieeff=dieeff
				self.dieeffnode=dieeffnode

			self.actpart=[]
			self.actpartnode=[]
			if not self.params["acteff"]==None:
				for x in range(0, self.params["acteff"]):
					y=x+1
					DPrint("Entity",0,"	ActEffect: "+str(y))
					actpart=shared.render3dScene.sceneManager.createParticleSystem("acteff"+str(y)+"-"+str(self.ID)+"-"+str(Interactive),self.params["acteff"+str(y)])
					actpartnode=self.node.createChildSceneNode()
					actpart.getEmitter(0).setTimeToLive(self.params["actefftime"+str(y)])
					actpart.getEmitter(0).setEnabled(False)
					actpartnode.setPosition(self.params["acteffpos"+str(y)])
					actpartnode.rotate((1,0,0),ogre.Degree(self.params["acteffrot"+str(y)][0]))
					actpartnode.rotate((0,1,0),ogre.Degree(self.params["acteffrot"+str(y)][1]))
					actpartnode.rotate((0,0,1),ogre.Degree(self.params["acteffrot"+str(y)][2]))
					actpartnode.attachObject(actpart)
					self.actpart.append(actpart)
					self.actpartnode.append(actpartnode)

			self.light=[]
			self.lightnode=[]
			if not self.params["light"]==None:
				for x in range(0, self.params["light"]):
					y=x+1
					DPrint("Entity",0,"	Light: "+str(y))
					light=shared.render3dScene.sceneManager.createLight("light"+str(y)+"-"+str(self.ID)+"-"+str(Interactive))
					light.type = ogre.Light.LT_POINT
					light.diffuseColour = (.5, .5, .0)
					light.spectacularColour=(.75,.75,.75)
					light.setVisible(False)
					lightnode=self.node.createChildSceneNode()
					lightnode.setPosition(self.params["lightpos"+str(y)])
					lightnode.rotate((1,0,0),ogre.Degree(self.params["lightrot"+str(y)][0]))
					lightnode.rotate((0,1,0),ogre.Degree(self.params["lightrot"+str(y)][1]))
					lightnode.rotate((0,0,1),ogre.Degree(self.params["lightrot"+str(y)][2]))
					lightnode.attachObject(light)
					self.light.append(light)
					self.lightnode.append(lightnode)

			self.moveanim=None
			if not self.params["moveanim"]==None:
				DPrint("Entity",0,"	MoveAnimation")
				self.moveanim=self.mesh.getAnimationState(self.params["moveanim"])
				self.moveanim.setLoop(True)

			self.deadanim=None
			if not self.params["deadanim"]==None:
				DPrint("Entity",0,"	DeadAnimation")
				self.deadanim=self.mesh.getAnimationState(self.params["deadanim"])

			self.idleanim=None
			if not self.params["idleanim"]==None:
				DPrint("Entity",0,"	IdleAnimation")
				self.idleanim=self.mesh.getAnimationState(self.params["idleanim"])
				self.idleanim.setLoop(True)

			self.idlehurtanim=None
			if not self.params["idlehurtanim"]==None:
				DPrint("Entity",0,"	IdleHurtAnimation")
				self.idlehurtanim=self.mesh.getAnimationState(self.params["idlehurtanim"])
				self.idlehurtanim.setLoop(True)

			self.movehurtanim=None
			if not self.params["movehurtanim"]==None:
				DPrint("Entity",0,"	MoveHurtAnimation")
				self.movehurtanim=self.mesh.getAnimationState(self.params["movehurtanim"])
				self.movehurtanim.setLoop(True)

			self.addidleanim=[]
			if not self.params["addidleanim"]==None:
				for x in range(0, self.params["addidleanim"]):
					y=x+1
					DPrint("Entity",0,"	AddIdleAnimation: "+str(y))
					idleanim=self.mesh.getAnimationState(self.params["idleanim"+str(y)])
					self.addidleanim.append(idleanim)

			self.actanim=[]
			if not self.params["actanim"]==None:
				for x in range(0, self.params["actanim"]):
					y=x+1
					DPrint("Entity",0,"	ActAnimation: "+str(y))
					actanim=self.mesh.getAnimationState(self.params["actanim"+str(y)])
					self.actanim.append(actanim)

			self.animtime=self.params["animtime"]

			#Some defines:
			self.hurtidle=False
			self.hurtmove=False
			self.curranim=None

			self.error=False
		except:
			DPrint("Entity",4,"Entity loading FAILED!")
			DPrint("Entity",0,format_exc())
			self.error=True
			try:
				if EntImporter>self.filever:
					DPrint("Entity",3,"Entity File is outdated! "+str(EntImporter)+">"+str(self.filever))
				elif EntImporter<self.filever:
					DPrint("Entity",3,"Are you from the future? This entity file has a newer version than this entity loader! Tell your local law enforcement that the creator of this file has broken the laws of timetraveling! "+str(EntImporter)+"<"+str(self.filever))
				else:
					DPrint("Entity",3,"Entity File has errors. Please nag the creator to fix it.")
			except:
				DPrint("Entity",3,"Entity File is corrupt! Please try to redownload the entity, or contact the creator")

 	def RandomPlacement(self):
 		x=randrange(1, 200, 1)
		y=0
		z=randrange(1, 200, 1)
		Raytrace=ogre.Ray()
		Raytrace.setOrigin((x,y+1000,z))
		Raytrace.setDirection(ogre.Vector3().NEGATIVE_UNIT_Y)
		self.raySceneQuery=shared.render3dScene.sceneManager.createRayQuery(Raytrace)
		for queryResult in self.raySceneQuery.execute():
			if queryResult.worldFragment is not None:  
				self.node.translate (x, 1000-queryResult.distance+1, z)
				print(queryResult.distance)

	def CreateTextOverlay(self):
		self.text=text.OgreText(self.mesh, shared.render3dCamera.camera, "**UNITTEXT**")
		self.text.enable(False)

	def Delete(self):
		print("detachObject")
		self.node.detachObject(self.mesh)
		print("destroyEntity")
		shared.render3dScene.sceneManager.destroyEntity(self.mesh.getName())
		print("destroySceneNode")
		shared.render3dScene.sceneManager.destroySceneNode(self.node.getName())
		print("text.destroy")
		if self.text:
			self.text.destroy()

	def actMove(self, yn):
		if yn==True:
			if not self.params["moveeff"]==None:
				for x in self.movepart:
					x.getEmitter(0).setEnabled(True)
			if not self.moveanim==None:
				if not self.hurtmove:
					self.moveanim.setEnabled(True)
					self.curranim=self.moveanim
				else:
					self.movehurtanim.setEnabled(True)
					self.curranim=self.movehurtanim
		else:
			if not self.params["moveeff"]==None:
				for x in self.movepart:
					x.getEmitter(0).setEnabled(False)
			if not self.params["moveanim"]==None:
				self.moveanim.setEnabled(False)
			if not self.params["movehurtanim"]==None:
				self.movehurtanim.setEnabled(False)

	def actHurt(self, yn):
		if yn==True:
			if not self.params["idlehurtanim"]==None:
				self.hurtidle=True
			if not self.params["movehurtanim"]==None:
				self.hurtmove=True
		else:
			if not self.params["idlehurtanim"]==None:
				self.hurtidle=False
			if not self.params["movehurtanim"]==None:
				self.hurtmove=False

	def actIdle(self, yn):
		if yn==True:
			if not self.params["idleanim"]==None:
				self.idleanim.setEnabled(True)
				self.curranim=self.idleanim
		else:
			if not self.params["idleanim"]==None:
				self.idleanim.setEnabled(False)

	def actDead(self, yn):
		if yn==True:
			if not self.params["deadanim"]==None:
				self.deadanim.setEnabled(True)
				self.deadanim.setLoop(False)
				self.curranim=self.deadanim
			if not self.params["dieeff"]==None:
				self.dieeff.getEmitter(0).setEnabled(True)
		else:
			if not self.params["deadanim"]==None:
				self.deadanim.setEnabled(False)
			if not self.params["dieeff"]==None:
				self.dieeff.getEmitter(0).setEnabled(False)

	def actEff(self, eff, yn):
		if yn==True:
			self.actpart[eff].getEmitter(0).setEnabled(True)
		else:
			self.actpart[eff].getEmitter(0).setEnabled(False)

	def actAnim(self, anim, yn):
		if yn==True:
			if anim in self.actanim:
				self.actanim[anim].setEnabled(True)
				self.curranim=self.actanim[anim]
			else:
				self.actanim[anim].setEnabled(False)

	def actLight(self, light, yn):
		if yn==True:
			self.light[light].setVisible(True)
		else:
			self.light[light].setVisible(False)

	def actNone(self):
		self.actMove(False)
		self.actHurt(False)
		self.actIdle(False)
		self.actDead(False)
		self.curranim=None

	def rotTurret(self, ang):
		if not self.params["meshturret"]==None:
			self.nodeturret.rotate((0,1,0),ogre.Degree(ang))

	def rotTurretTowardPos(self, x, y, z):
		if not self.params["meshturret"]==None:
			self.nodeturret.setFixedYawAxis(True, ogre.Vector3().UNIT_Y)
			self.nodeturret.lookAt((int(x), self.nodeturret.getPosition().y, int(z)), self.nodeturret.TS_PARENT, ogre.Vector3().UNIT_Z)

	def SetPosition(self, x, y, z):
		self.lastMovementDirection = Vector(x,y,z) - Vector(self.GetPosition())
		#print(self.lastMovementDirection)
		self.node.setPosition(x, y, z)
		return self.node.getPosition()

	def GetPosition(self):
		pos = self.node.getPosition()
		return (pos.x, pos.y, pos.z)

	def Translate(self, x, y, z):
		lastpos = Vector(self.GetPosition())
		self.node.translate(x, y, z)
		newpos = Vector(self.GetPosition())
		self.lastMovementDirection = newpos - lastpos
		return self.node.getPosition()

	def setOrientation(self, w, x, y, z):
		self.node.setOrientation(float(w), float(x), float(y), float(z))

	def Rotate(self, x, y, z):
		self.node.rotate((1,0,0),ogre.Degree(x))
		self.node.rotate((0,1,0),ogre.Degree(y))
		self.node.rotate((0,0,1),ogre.Degree(z))
		return self.node.getOrientation()

	def RPYRotate(self, roll, pitch, yaw):
		self.node.roll(ogre.Degree(float(roll)))
		self.node.pitch(ogre.Degree(float(pitch)))
		self.node.yaw(ogre.Degree(float(yaw)))

	def transRotate(self, x, y, z):
		px=float(self.node.getOrientation().getRoll().valueDegrees())
		py=float(self.node.getOrientation().getPitch().valueDegrees())
		pz=float(self.node.getOrientation().getYaw().valueDegrees())
		print("PrevRot:")
		print (px, py, pz)
		#self.node.rotate((1,0,0),ogre.Degree(px))
		#self.node.rotate((0,1,0),ogre.Degree(float(py+0.00000000001)))
		#self.node.rotate((0,0,1),ogre.Degree(pz))
		self.node.roll(ogre.Degree(px+x))
		self.node.pitch(ogre.Degree(py+y))
		self.node.yaw(ogre.Degree(pz+z))

		print("TRot:")
		print(px+x, py+y, pz+z)
		return self.node.getOrientation()

	def LookAtZ(self, x, y, z):
		self.node.setFixedYawAxis(True, ogre.Vector3().UNIT_Y)
		#self.node.setFixedRollAxis(True, ogre.Vector3().UNIT_X)
		self.node.lookAt((int(x), self.node.getPosition().y, int(z)), self.node.TS_PARENT, ogre.Vector3().UNIT_Z)
		# direction=ogre.Vector3(int(x), int(y), int(z)) - self.node.getPosition()
		# src = self.node.getOrientation() * ogre.Vector3().NEGATIVE_UNIT_Z
		# quat = src.getRotationTo(direction)
		# self.node.rotate(quat)

	def getAltitude(self):
		Pos = self.GetPosition()
		Raytrace=ogre.Ray()
		Raytrace.setOrigin(Pos)
		Raytrace.setDirection(ogre.Vector3().NEGATIVE_UNIT_Y)
		self.raySceneQuery=shared.render3dScene.sceneManager.createRayQuery(Raytrace)
		for queryResult in self.raySceneQuery.execute():
			if queryResult.worldFragment is not None:  
				return queryResult.distance

	def Think(self):
		if self.error!=True:
			if self.curranim!=None and self.animtime!=None:
				self.curranim.addTime(self.animtime)

	def getIfAnimIsFinish(self):
		if self.curranim!=None:
			return self.curranim.hasEnded()
		else:
			return True

	def __del__(self):
		if shared!=None:
			shared.DPrint("Entity",5,"Entity gc'd: "+str(self.ID))