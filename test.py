#!/usr/bin/env python 
# This code is Public Domain. 
"""Python-Ogre Intermediate Tutorial 06: Final code """
 
import ogre.renderer.OGRE as ogre 
import SampleFramework as sf
import math
 
class ProjectiveDecalListener(sf.FrameListener):
   def __init__(self, win, cam, proj, decal):
 
      sf.FrameListener.__init__(self, win, cam)
 
      self.projectorNode = proj
      self.decalFrustum = decal
      self.anim = 0.0
 
   def frameStarted(self, evt):
      self.projectorNode.rotate(ogre.Vector3().UNIT_Y, ogre.Degree(evt.timeSinceLastFrame * 10))
      self.anim += evt.timeSinceLastFrame / 2
      if self.anim >= 1:
         self.anim -= 1
      self.decalFrustum.setFOVy(ogre.Degree(15 + math.sin(self.anim * 2 * math.pi) * 10))
      return sf.FrameListener.frameStarted(self, evt)
 
class TutorialApplication(sf.Application): 
   """Application class.""" 
 
   def _createScene(self):
      self.decalFrustum = ogre.Frustum()
      self.projectorNode = self.sceneManager.getRootSceneNode().createChildSceneNode("DecalProjectorNode")
 
      self.sceneManager.setAmbientLight((0.2, 0.2, 0.2))
 
      l = self.sceneManager.createLight("MainLight")
      l.setPosition(20, 80, 50)
 
      self.camera.setPosition(60, 200, 70)
      self.camera.lookAt(0, 0, 0)
 
      # 6 ogre heads, arranged in a circle
      for i in range(0, 6):
         headNode = self.sceneManager.getRootSceneNode().createChildSceneNode()
         ent = self.sceneManager.createEntity("head" + str(i), "ogrehead.mesh")
         headNode.attachObject(ent)
         angle = i * 2 * math.pi / 6
         headNode.setPosition(75 * math.cos(angle), 0, 75 * math.sin(angle))
 
      self.createProjector()
      for i in range(0, ent.getNumSubEntities()):
         self.makeMaterialReceiveDecal(ent.getSubEntity(i).getMaterialName())
 
   def createProjector(self):
      self.projectorNode.attachObject(self.decalFrustum)
      self.projectorNode.setPosition(0, 5, 0)
 
      self.filterFrustum = ogre.Frustum()
      self.filterFrustum.setProjectionType(ogre.PT_ORTHOGRAPHIC)
      filterNode = self.projectorNode.createChildSceneNode("DecalFilterNode")
      filterNode.attachObject(self.filterFrustum)
      filterNode.setOrientation(ogre.Quaternion(ogre.Degree(90), ogre.Vector3().UNIT_Y))
 
   def makeMaterialReceiveDecal(self, matName):
      mat = ogre.MaterialManager.getSingleton().getByName(matName)
      mPass = mat.getTechnique(0).createPass()
 
      mPass.setSceneBlending(ogre.SBT_TRANSPARENT_ALPHA)
      mPass.setDepthBias(1)
      mPass.setLightingEnabled(False)
 
      texState = mPass.createTextureUnitState("decal.png")
      texState.setProjectiveTexturing(True, self.decalFrustum)
      texState.setTextureAddressingMode(ogre.TextureUnitState.TAM_CLAMP)
      texState.setTextureFiltering(ogre.FO_POINT, ogre.FO_LINEAR, ogre.FO_NONE)
 
      texState = mPass.createTextureUnitState("decal_filter.png")
      texState.setProjectiveTexturing(True, self.filterFrustum)
      texState.setTextureAddressingMode(ogre.TextureUnitState.TAM_CLAMP)
      texState.setTextureFiltering(ogre.TFO_NONE)
 
   def _createFrameListener(self):
      self.frameListener = ProjectiveDecalListener(self.renderWindow, self.camera, self.projectorNode, self.decalFrustum)
      self.root.addFrameListener(self.frameListener)
      self.frameListener.showDebugOverlay(True)
 
if __name__ == '__main__': 
   ta = TutorialApplication() 
   ta.go()