#Render3dExtension - render3ddebug
#Classes for rendering various useful debug stuff

from engine import shared, debug
from engine.shared import DPrint
import ogre.renderer.OGRE as ogre
import render3dshapes as Shape
from ogre.io.OIS import KC_F2 

MASK_NONE = 1 << 16

class aStarView():
	def __init__(self):
		self.status = False
		self.basemat = ogre.MaterialManager.getSingleton().getByName("blah")
		self.basenode=shared.render3dScene.sceneManager.getRootSceneNode().createChildSceneNode("astarview")
		self.aStarNodeShape=Shape.Tetra("astar", "blah", 8, True)
		self.ents = []
		self.entnodes = []
		self.entmats = []
		shared.renderioInput.registerKeyEvent(KC_F2, self.toggle, None)

	def toggle(self):
		if self.status:
			self.offline()
		else:
			self.online()

	def online(self):
		i = 0
		for node in shared.Pathfinder.aStarPath.totnodes:
			newent = shared.render3dScene.sceneManager.createEntity("astarent"+str(i), "astar")
			newmat = self.basemat.clone("astarnodemat"+str(i))
			if node.c<500:
				nodecost = float(float(node.c)/float(500))
				newmat.getTechnique(0).getPass(0).setAmbient(nodecost, float(float(1)-(nodecost*float(2))),0)
			elif node.c<1000:
				nodecost = float(float(node.c)/float(1000))
				newmat.getTechnique(0).getPass(0).setAmbient(float(float(1)-(nodecost)), 0, nodecost)
			else:
				nodecost = 0
				newmat.getTechnique(0).getPass(0).setAmbient(0, 0, 0)
			
			newmat.getTechnique(0).getPass(0).setDiffuse(0.5, 0.5, 0.5, 1)
			newent.setMaterial(newmat)
			newent.setQueryFlags(MASK_NONE)
			newnode = self.basenode.createChildSceneNode("astarnode"+str(i))
			newnode.attachObject(newent)
			nx, ny = shared.Pathfinder.aStarPath.convertLPosToWPos(node.x, node.y)
			newnode.setPosition(nx, shared.render3dTerrain.getHeightAtPos(nx, ny)+10, ny)

			self.ents.append(newent)
			self.entnodes.append(newnode)
			self.entmats.append(newmat)
			i+=1
		self.status = True

	def offline(self):
		for ent in self.ents:
			shared.render3dScene.sceneManager.destroyEntity(ent)
		self.ents = []

		for entnode in self.entnodes:
			shared.render3dScene.sceneManager.destroySceneNode(entnode)
		self.entnodes = []

		for entmat in self.entmats:
			ogre.MaterialManager.getSingleton().unload(entmat.getName())
			ogre.MaterialManager.getSingleton().remove(entmat.getName())
		self.entmats = []

		self.status = False