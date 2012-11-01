#Render3dExtension - render3dent
#Classes for handeling Entitys
#Lowlevel Module (Text)

import text
from engine import shared, debug
from engine.shared import DPrint
from os import listdir
from os.path import isfile, join
from string import split
from random import randrange
from traceback import format_exc
import ogre.renderer.OGRE as ogre

class EntityHandeler():
	def ReadEntitys(self):
		DPrint(8,1,"Reading Files..")
		FilePath="Data/Ent"
		Files=[]

		for f in listdir(FilePath):
			if isfile(join(FilePath,f)):
				if f[len(f)-3:]=="ent":
					Files.append(f)

		self.EntDict={}
		for x in Files:
			f=open(join(FilePath,x),"r")
			Lines=f.readlines()
			for line in Lines:
				if line==Lines[0]:
					Name=line[:len(line)-1]
					self.EntDict[Name]={}
				elif line==Lines[len(Lines)-1]:
					Key, Value = self.ParseLine(line[:len(line)])
					self.EntDict[Name][Key]=Value
					print (Name+": "+Key+"="+str(Value)+str(type(Value)))
				else:
					Key, Value = self.ParseLine(line[:len(line)-1])
					self.EntDict[Name][Key]=Value
					print (Name+": "+Key+"="+str(Value)+str(type(Value)))			

	def ParseLine(self,line):
		DPrint(8,1,"Parsing Files..")
		ComPar=split(line, "=")
		Key=ComPar[0]
		Value=ComPar[1]
		#Parsing Vector3:
		if Value[0]=="(" and Value[len(Value)-1]==")":
			Value=split(Value[1:len(Value)-1],",")
			#print Value
			Value=(int(Value[0]),int(Value[1]),int(Value[2]))

		#Parsing Lists:
		elif Value[0]=="[" and Value[len(Value)-1]=="]":
			Value=split(Value[1:len(Value)-1],",")
			print("Shit..")

		#Parsing Boolean:
		elif Value.lower()=="true":
			Value=True
		elif Value.lower()=="false":
			Value=False

		#Parsing None:
		elif Value.lower()=="none":
			Value=None

		#Parsing numbers
		else:
			#Parsing Integer
			try:
				Value=int(Value)
			except ValueError:
				pass

			#Parsing Float
			if type(Value)!=int:
				try:
					Value=float(Value)
				except ValueError:
					pass

		return Key, Value

	def GetParam(self, ent, key):
		return self.EntDict[ent][key]

	def GetParams(self, ent):
		return self.EntDict[ent]

	def Create(self, Identifyer, Type, Interactive, Team=None):
		shared.DPrint(8,0,"Creating Entity: "+Type+" : "+str(Interactive))
		ent=Entity(Identifyer, Type, Team, Interactive)
		return ent

	def Destroy(self, Identifyer):
		pass

class Entity():
 	def __init__(self, Identifyer, Type, Team, Interactive):
 		EntImporter=1.0
 		self.ID=Identifyer
 		self.Team=Team
 		self.Type=Type
 		self.text=None

 		DPrint(8,0,"Loading Entity: "+str(self.Type))
 		try:
 			self.params=shared.EntityHandeler.GetParams(self.Type)
 			self.filever=self.params["version"]
	 		DPrint(8,0,"	EntityFile v."+str(self.filever))
	 		DPrint(8,0,"	Mesh: "+str(self.params["mesh"]))
			self.mesh=shared.render3dScene.sceneManager.createEntity(Interactive+str(Identifyer), self.params["mesh"])
			self.shadows=self.params["shadows"]
			self.mesh.setCastShadows(self.shadows)
			self.node=shared.render3dScene.sceneManager.getSceneNode("EntNode").createChildSceneNode(Interactive+"Node_"+str(Identifyer))
			self.node.attachObject(self.mesh)
			self.meshturret=None
			self.nodeturret=None
			if not self.params["meshturret"]==None:
				DPrint(8,0,"	MeshTurret")
				self.meshturret=shared.render3dScene.sceneManager.createEntity(Interactive+str(Identifyer)+"-turret", self.params["meshturret"])
				self.meshturret.setCastShadows(self.shadows)
				self.nodeturret=self.node.createChildSceneNode(Interactive+"Node-Turret_"+str(Identifyer))
				self.nodeturret.attachObject(self.meshturret)
				
			self.meshes=[]
			self.meshnodes=[]
			if not self.params["addmesh"]==None:
				for x in range(0, self.params["addmesh"]):
					y=x+1
					DPrint(8,0,"	AddMesh: "+str(y))
					mesh=shared.render3dScene.sceneManager.createEntity(Interactive+str(Identifyer)+"-addmesh"+str(y), self.params["mesh"+str(y)])
					mesh.setCastShadows(self.shadows)
					node=self.node.createChildSceneNode(Interactive+"Node-Mesh"+str(y)+"_"+str(Identifyer))
					node.attachObject(mesh)
					self.meshes.append(mesh)
					self.meshnodes.append(node)
			self.movepart=[]
			self.movepartnode=[]
	 		if not self.params["moveeff"]==None:
	 			DPrint(8,0,"	MoveEffect")
	 			movepart=shared.render3dScene.sceneManager.createParticleSystem("moveeff0-"+str(self.ID),self.params["moveeff"])
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
					DPrint(8,0,"	AddMoveEffect: "+str(y))
					movepart=shared.render3dScene.sceneManager.createParticleSystem("moveeff"+str(y)+"-"+str(self.ID),self.params["moveeff"+str(y)])
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
				DPrint(8,0,"	DieEffect")
				dieeff=shared.render3dScene.sceneManager.createParticleSystem("dieeff0-"+str(self.ID),self.params["dieeff"])
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
					DPrint(8,0,"	ActEffect: "+str(y))
					actpart=shared.render3dScene.sceneManager.createParticleSystem("acteff"+str(y)+"-"+str(self.ID),self.params["acteff"+str(y)])
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
					DPrint(8,0,"	Light: "+str(y))
					light=shared.render3dScene.sceneManager.createLight("light"+str(y)+"-"+str(self.ID))
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
				DPrint(8,0,"	MoveAnimation")
				self.moveanim=self.mesh.getAnimationState(self.params["moveanim"])
				self.moveanim.setLoop(True)

			self.deadanim=None
			if not self.params["deadanim"]==None:
				DPrint(8,0,"	DeadAnimation")
				self.deadanim=self.mesh.getAnimationState(self.params["deadanim"])

			self.idleanim=None
			if not self.params["idleanim"]==None:
				DPrint(8,0,"	IdleAnimation")
				self.idleanim=self.mesh.getAnimationState(self.params["idleanim"])
				self.idleanim.setLoop(True)

			self.idlehurtanim=None
			if not self.params["idlehurtanim"]==None:
				DPrint(8,0,"	IdleHurtAnimation")
				self.idlehurtanim=self.mesh.getAnimationState(self.params["idlehurtanim"])
				self.idlehurtanim.setLoop(True)

			self.movehurtanim=None
			if not self.params["movehurtanim"]==None:
				DPrint(8,0,"	MoveHurtAnimation")
				self.movehurtanim=self.mesh.getAnimationState(self.params["movehurtanim"])
				self.movehurtanim.setLoop(True)

			self.addidleanim=[]
			if not self.params["addidleanim"]==None:
				for x in range(0, self.params["addidleanim"]):
					y=x+1
					DPrint(8,0,"	AddIdleAnimation: "+str(y))
					idleanim=self.mesh.getAnimationState(self.params["idleanim"+str(y)])
					self.addidleanim.append(idleanim)

			self.actanim=[]
			if not self.params["actanim"]==None:
				for x in range(0, self.params["actanim"]):
					y=x+1
					DPrint(8,0,"	ActAnimation: "+str(y))
					actanim=self.mesh.getAnimationState(self.params["actanim"+str(y)])
					self.actanim.append(actanim)

			self.animtime=self.params["animtime"]

			#Some defines:
			self.hurtidle=False
			self.hurtmove=False
			self.curranim=None

			self.error=False
		except:
			DPrint(8,4,"Entity loading FAILED!")
			DPrint(8,0,format_exc())
			self.error=True
			try:
				if EntImporter>self.filever:
					DPrint(8,3,"Entity File is outdated! "+str(EntImporter)+">"+str(self.filever))
				else:
					DPrint(8,3,"Entity File has errors. Please nag the creator to fix it.")
			except:
				DPrint(8,3,"Entity File is corrupt! Please try to redownload the entity, or contact the creator")

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
		self.node.detachObject(self.mesh)
		shared.render3dScene.sceneManager.destroyEntity(self.mesh.getName())
		shared.render3dScene.sceneManager.destroySceneNode(self.node.getName())
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

	def SetPosition(self, x, y, z):
		self.node.setPosition(x, y, z)
		return self.node.getPosition()

	def Translate(self, x, y, z):
		self.node.translate(x, y, z)
		return self.node.getPosition()

	def Rotate(self, x, y, z):
		self.node.rotate((1,0,0),ogre.Degree(x))
		self.node.rotate((0,1,0),ogre.Degree(y))
		self.node.rotate((0,0,1),ogre.Degree(z))
		return self.node.getOrientation()

	def Think(self):
		if self.error!=True:
			if self.curranim!=None and self.animtime!=None:
				self.curranim.addTime(self.animtime)

	def __del__(self):
		shared.DPrint(1,5,"Entity gc'd: "+str(self.ID))