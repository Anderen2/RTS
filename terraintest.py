import sys
sys.path.insert(0,'..')
import PythonOgreConfig

import ogre.renderer.OGRE as ogre
import ogre.renderer.ogreterrain as ogreterrain
import SampleFramework as sf
import ctypes as ctypes

def Clamp ( val, low, high ):
		 if val < low: return low
		 if val > high: return high
		 return val

class TerrainApplication(sf.Application):

	def _chooseSceneManager(self):
		# self.sceneManager = self.root.createSceneManager("TerrainSceneManager")
		self.sceneManager = self.root.createSceneManager(ogre.ST_GENERIC)

	def _createScene(self):
		sceneManager = self.sceneManager
		  
		# setting up the camera.
		camera = self.camera
		camera.setPosition(1683, 100, 2116)
		camera.lookAt(1963, 50, 1660)
		camera.setNearClipDistance(0.1)
		camera.setFarClipDistance(50000)
	
		if (self.root.getRenderSystem().getCapabilities().hasCapability(ogre.RSC_INFINITE_FAR_PLANE)):
			camera.setFarClipDistance(0)
 
		self.materialManager = ogre.MaterialManager.getSingleton()
		self.materialManager.setDefaultTextureFiltering(ogre.TFO_ANISOTROPIC)
		self.materialManager.setDefaultAnisotropy(7)
 
		lightdir = ogre.Vector3(0.55, -0.3, 0.75)
		lightdir.normalise()
		  
		light = self.sceneManager.createLight("tstLight")
		light.setType(ogre.Light.LT_DIRECTIONAL)
		light.setDirection(lightdir)
		light.setDiffuseColour(ogre.ColourValue(1.0, 1.0, 1.0))
		light.setSpecularColour(ogre.ColourValue(0.4, 0.4, 0.4))
 
		sceneManager.AmbientLight = 0.2, 0.2, 0.2
			  
		self.terrainGlobals = ogreterrain.TerrainGlobalOptions()
		self.terrainGroup = ogreterrain.TerrainGroup(self.sceneManager, ogreterrain.Terrain.ALIGN_X_Z, 513, 12000)
		self.terrainGroup.setFilenameConvention("BasicTutorial3Terrain", "dat")
		self.terrainGroup.setOrigin(ogre.Vector3(0, 0, 0))
		  
		self.configureTerrainDefaults(light)
		  
		self.defineTerrain(0, 0)
		  
		self.terrainGroup.loadAllTerrains(True)

		if (self.terrainsImported):
			it = self.terrainGroup.getTerrainIterator()
			for t in self.terrainGroup.getTerrainIterator():
				self.initBlendMaps(t.instance)

		self.terrainGroup.freeTemporaryResources()
		  
	def configureTerrainDefaults(self, light):
		self.terrainGlobals.setMaxPixelError(8)
		self.terrainGlobals.setCompositeMapDistance(3000)
		self.terrainGlobals.setLightMapDirection(light.getDerivedDirection())
		self.terrainGlobals.setCompositeMapAmbient(self.sceneManager.getAmbientLight())
		self.terrainGlobals.setCompositeMapDiffuse(light.getDiffuseColour())
	
		# Configure default import settings for if we use imported image
		defaultimp = self.terrainGroup.getDefaultImportSettings()
		defaultimp.terrainSize = 513
		defaultimp.worldSize = 12000
		defaultimp.inputScale = 600
		defaultimp.minBatchSize = 33
		defaultimp.maxBatchSize = 65

		# textures
		layer0 = ogreterrain.Terrain.LayerInstance()
		layer0.worldSize = 100
		layer0.textureNames.append("dirt_grayrocky_diffusespecular.dds")
		layer0.textureNames.append("dirt_grayrocky_normalheight.dds")
		defaultimp.layerList.append(layer0)

		layer1 = ogreterrain.Terrain.LayerInstance()
		layer1.worldSize = 30
		layer1.textureNames.append("grass_green-01_diffusespecular.dds")
		layer1.textureNames.append("grass_green-01_normalheight.dds")
		defaultimp.layerList.append(layer1)

		layer2 = ogreterrain.Terrain.LayerInstance()
		layer2.worldSize = 200
		layer2.textureNames.append("growth_weirdfungus-03_diffusespecular.dds")
		layer2.textureNames.append("growth_weirdfungus-03_normalheight.dds")
		defaultimp.layerList.append(layer2)
		  
	def defineTerrain(self, x, y):
		filename = self.terrainGroup.generateFilename(x, y)
		RGM = ogre.ResourceGroupManager.getSingleton()
		if ( RGM.resourceExists(self.terrainGroup.getResourceGroup(), filename) ):
			self.terrainGroup.defineTerrain(x, y)
		else :
			img = self.getTerrainImage((x % 2) != 0, (y%2) != 0)
			self.terrainGroup.defineTerrain(x, y, img)
			self.terrainsImported = True
					 
	def getTerrainImage(self, flipX, flipY):
		img = ogre.Image()
		img.load("terrain.png", ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME)
		if flipX:
			img.flipAroundY()
		if flipY:
			img.flipAroundX() 
		return img
				
	def initBlendMaps(self, terrain):
		blendMap0 = terrain.getLayerBlendMap(1)
		blendMap1 = terrain.getLayerBlendMap(2)
		minHeight0 = 70
		fadeDist0 = 40.0
		minHeight1 = 70
		fadeDist1 = 15.0

		pBlend1 = blendMap1.getBlendPointer()    # returns the address of the buffer
		size = terrain.getLayerBlendMapSize() * terrain.getLayerBlendMapSize()
		blend_data=(ctypes.c_float * size).from_address(pBlend1)
		index = 0
		for y in range(terrain.getLayerBlendMapSize()):
			for x in range( terrain.getLayerBlendMapSize() ):
				# using ctypes
				tx = ctypes.c_float(0.0)
				ty = ctypes.c_float(0.0)
					 
				blendMap0.convertImageToTerrainSpace(x, y, ctypes.addressof(tx), ctypes.addressof(ty))
				height = terrain.getHeightAtTerrainPosition(tx.value, ty.value)
				val = (height - minHeight0) / fadeDist0
				val = Clamp(val, 0, 1)

				val = (height - minHeight1) / fadeDist1
				val = Clamp(val, 0, 1)
				blend_data [index] = val
				index += 1
					 
		blendMap0.dirty()
		blendMap1.dirty()
		blendMap0.update()
		blendMap1.update()        

if __name__ == '__main__':
	try:
		application = TerrainApplication()
		application.go()
	except ogre.OgreException, e:
		print e