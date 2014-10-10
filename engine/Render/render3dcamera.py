#Render3dExtension - render3dcamera
#Classes for handeling camera control
#Highlevel module camera

from ogre.renderer.OGRE import Degree, Vector3, Vector2, Quaternion
from engine.Lib.hook import Hook
from engine import debug, shared

#Camera QueryFlag
MASK_CAMERA = 1 << 5

class Camera():
	def __init__(self, root, scene):
		self.root=root
		shared.DPrint("Camera",1,"Camera: Creating camera")
		self.camera = scene.sceneManager.createCamera("Camera")
		self.camera.nearClipDistance = 10
		self.camera.setFarClipDistance(100000000)
		self.camera.setQueryFlags(MASK_CAMERA)

		print("LOD: !!!!!!!")
		print(self.camera.getLodBias())

		self.camera.setLodBias(100)
		self.camNode=scene.sceneManager.getRootSceneNode().createChildSceneNode("CamNode",(0,0,0))

		self.pitchnode=self.camNode.createChildSceneNode('PitchNode1')
		self.pitchnode.attachObject(self.camera)

		self.viewPort = self.root.getAutoCreatedWindow().addViewport(self.camera)

		self.rotate = 0.13
		self.move = 250

		self.camNode.setPosition(1649.85, 1229.42, 1183.86) #GET THIS FROM MAPFILE LATER (HARDCODE)
		#self.camera.setOrientation(Quaternion(0.0, 0.6989771127700806, 0.0, -0.7151437401771545))

		#Hooks
		self.Hook = Hook(self)
		self.Hook.new("OnMove", 1)
		self.Hook.new("OnRotate", 1)
		self.Hook.new("OnSetPos", 2)

	def Move(self, direction, delta):
		transVector = Vector3(0, 0, 0)

		transVector.x = direction[0]*self.move
		transVector.y = direction[1]*self.move
		transVector.z = direction[2]*self.move

		# print(direction[2]*self.move)
		# print(direction)
		# print(transVector)

		self.Hook.call("OnMove", self.camNode.orientation * transVector * delta)

		self.camNode.translate(self.camNode.orientation * transVector * delta)
		print(self.camNode.getPosition())

	def SetPos(self, pos):
		#Sets the camera's scenenode position. Translate is used to translate relative movement to world coordinates
		self.camNode.translate(pos)
		self.Hook.call("OnMove", pos)

	def setAbsolutePos(self, pos):
		self.camNode.setPosition(pos)
		self.Hook.call("OnSetPos", pos)

	def set2DPos(self, pos):
		prev = self.camNode.getPosition()
		prev = (prev.x, prev.z)
		self.camNode.setPosition(pos[0], self.camNode.getPosition().y, pos[1])
		self.Hook.call("OnSetPos", pos, prev)

	def Rotate(self, relativemousepos):
		self.camNode.yaw(Degree(-self.rotate * relativemousepos[0]).valueRadians())
		self.camNode.getChild(0).pitch(Degree(-self.rotate * relativemousepos[1]).valueRadians())
		wad = self.camNode.getOrientation()
		print(wad.x, wad.y, wad.z, wad.w)
		self.Hook.call("OnRotate", relativemousepos)

	def getDimensions(self):
		return (self.viewPort.getActualWidth(), self.viewPort.getActualHeight())