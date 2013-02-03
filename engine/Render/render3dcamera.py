#Render3dExtension - render3dcamera
#Classes for handeling camera controll
#Highlevel module camera

from engine import debug, shared

class Camera():
	def __init__(self, root, scene):
		self.root=root
		shared.DPrint("Camera",1,"Camera: Creating camera")
		self.camera = scene.sceneManager.createCamera("Camera")
		self.camera.nearClipDistance = 2

		self.camNode=scene.sceneManager.getRootSceneNode().createChildSceneNode("CamNode",(0,0,0))

		self.wtfNode=self.camNode.createChildSceneNode('PitchNode1')
		self.wtfNode.attachObject(self.camera)

		self.viewPort = self.root.getAutoCreatedWindow().addViewport(self.camera)

		self.rotate = 0.13
		self.move = 250
		self.sheit=None

	def Move(self, direction, delta):
		transVector = ogre.Vector3(0, 0, 0)
		if direction=="W":
			transVector.z -= self.move
		if direction=="S":
			transVector.z += self.move
		if direction=="A":
			transVector.x -= self.move
		if direction=="D":
			transVector.x += self.move
		if direction=="Q":
			transVector.y += self.move
		if direction=="E":
			transVector.y -= self.move
		self.camNode.translate(self.camNode.orientation * transVector * delta)

	def SetPos(self, array):
		#Sets the camera's scenenode position. Translate is used to translate relative movement to world coordinates (I think.)
		self.camNode.translate(array)