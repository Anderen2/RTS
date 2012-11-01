#!/usr/bin/env python 
# This code is Public Domain. 
"""Python-Ogre Intermediate Tutorial 05: Final code """
 
import ogre.renderer.OGRE as ogre 
import SampleFramework as sf
 
class TutorialApplication(sf.Application): 
	 """Application class.""" 
 
	 def createGrassMesh(self):
			width = 25.0
			height = 30.0
 
			mo = ogre.ManualObject("GrassObject")
			vec = ogre.Vector3(width / 2, 0, 0)
			rot = ogre.Quaternion()
			#rot.FromAngleAxis(ogre.Degree(60), ogre.Vector3.UNIT_Y)
 
			mo.begin("Examples/GrassBlades", ogre.RenderOperation.OT_TRIANGLE_LIST)
			for i in range(0, 3):
				 mo.position(-vec.x, height, -vec.z)
				 mo.textureCoord(0, 0)
				 mo.position(vec.x, height, vec.z)
				 mo.textureCoord(1, 0)
				 mo.position(-vec.x, 0, -vec.z)
				 mo.textureCoord(0, 1)
				 mo.position(vec.x, 0, vec.z)
				 mo.textureCoord(1, 1)
 
				 offset = i * 4
				 mo.triangle(offset, offset+3, offset+1)
				 mo.triangle(offset, offset+2, offset+3)
 
				 vec = rot * vec
			mo.end()
 
			mo.convertToMesh("GrassBladesMesh")
 
	 def _createScene(self):
			self.createGrassMesh()
			self.sceneManager.setAmbientLight((1, 1, 1))
 
			self.camera.setPosition(150, 50, 150)
			self.camera.lookAt(0, 0, 0)
 
			robot = self.sceneManager.createEntity("robot", "robot.mesh")
			self.sceneManager.getRootSceneNode().createChildSceneNode().attachObject(robot)
 
			plane = ogre.Plane()
			plane.normal = (0,1,0)
			plane.d = 0
 
			ogre.MeshManager.getSingleton().createPlane("floor",
																									ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME, plane,
																									450, 450,
																									10, 10,
																									True,
																									1, 50, 50,
																									(0,0,1))
			planeEnt = self.sceneManager.createEntity("plane", "floor")
			planeEnt.setMaterialName("Examples/GrassFloor")
			planeEnt.setCastShadows(False)
			self.sceneManager.getRootSceneNode().createChildSceneNode().attachObject(planeEnt)
 
			grass = self.sceneManager.createEntity("grass", "GrassBladesMesh")
			sg = self.sceneManager.createStaticGeometry("GrassArea")
 
			size = 375
			amount = 20
 
			sg.setRegionDimensions(ogre.Vector3(size, size, size))
			sg.setOrigin(ogre.Vector3(-size/2, 0, -size/2))
 
			import random
 
			for x in range(-size/2, size/2, size/amount):
				 for z in range(-size/2, size/2, size/amount):
						r = size / float(amount) / 2.0
						pos = ogre.Vector3(x + random.uniform(-r, r), 0,
															 z + random.uniform(-r, r))
						scale = ogre.Vector3(1, random.uniform(0.9, 1.1), 1)
						orientation = ogre.Quaternion()
						orientation.FromAngleAxis(ogre.Degree(random.uniform(0, 359)), (0,1,0))
						sg.addEntity(grass, pos, orientation, scale)
			sg.build()
 
if __name__ == '__main__': 
	 ta = TutorialApplication() 
	 ta.go()