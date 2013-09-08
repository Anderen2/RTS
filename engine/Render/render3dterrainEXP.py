#render3dTerrain
#Functions related to modifying and getting realtime data from the terrain

import ctypes
from engine import shared, debug
import ogre.renderer.OGRE as ogre
import ogre.renderer.ogreterrain as ogreterrain

def Clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

class Terrain():
	def __init__(self, sceneManager):
		self.Material=None
		self.sceneManager = sceneManager

		#Setup temporary terrain (Is this really nessecary?)
		#if self.Material==None:
		#	self.createTerrainMaterial("2048.png", {"terr_rock-dirt.jpg":"alphamap.png", "grass_1024.jpg":"alphamap2.png"})
		#print(dir(ogreterrain))
		print("START")
		self.terrainGlobals = ogreterrain.TerrainGlobalOptions()
		self.terrainGroup = ogreterrain.TerrainGroup(self.sceneManager, ogreterrain.Terrain.ALIGN_X_Z, 129, 2049) #Scene, Orientation, Batchsize, Terrain Size
		self.terrainGroup.setFilenameConvention("BasicTutorial3Terrain", "dat")
		self.terrainGroup.setOrigin(ogre.Vector3(0, 0, 0))
		  
		self.configureTerrainDefaults("light")
		  
		self.defineTerrain(0, 0)
		  
		self.terrainGroup.loadAllTerrains(True)

		# if (self.terrainsImported):
		# 	it = self.terrainGroup.getTerrainIterator()
		# 	for t in it:
		self.initBlendMaps(self.terrainGroup.getTerrain(0,0))


		#matProfile = ogreterrain.TerrainMaterialGenerator().getActiveProfile().generate(self.terrainGroup.getTerrain(0,0))
		#matProf2 = self.terrainGlobals.getDefaultMaterialGenerator().getActiveProfile()
		#print(dir(matProf2))
		self.terrainGroup.getTerrain(0,0).setHeightAtPoint(1,1,0)
		self.terrainGroup.getTerrain(0,0).setHeightAtPoint(50,50,1000)
		self.terrainGroup.getTerrain(0,0).dirty()
		self.terrainGroup.getTerrain(0,0).updateGeometry()

		self.terrainGroup.freeTemporaryResources()
		  
	def configureTerrainDefaults(self, light):
		self.terrainGlobals.setMaxPixelError(8)
		self.terrainGlobals.setCompositeMapDistance(100) #Distance before texture gets fucked up
		#self.terrainGlobals.setLightMapDirection(light.getDerivedDirection())
		#self.terrainGlobals.setCompositeMapAmbient(self.sceneManager.getAmbientLight())
		#self.terrainGlobals.setCompositeMapDiffuse(light.getDiffuseColour())
	
		# Configure default import settings for if we use imported image
		defaultimp = self.terrainGroup.getDefaultImportSettings()
		#defaultimp.terrainSize = 100
		#defaultimp.worldSize = 10
		defaultimp.inputScale = 200 #Height of terrain
		defaultimp.minBatchSize = 33
		defaultimp.maxBatchSize = 65

		layer0 = ogreterrain.Terrain.LayerInstance()
		layer0.worldSize == 256 #I have no idea
		layer0.textureNames.append("grass_1024.jpg")
		#layer0.textureNames.append("terr_dirt-grass.jpg")
		#layer0.textureNames.append("Circle.png")
		defaultimp.layerList.append(layer0)

		layer1 = ogreterrain.Terrain.LayerInstance()
		layer1.worldSize == 256 #I have no idea
		layer1.textureNames.append("terr_rock-dirt.jpg")
		#layer0.textureNames.append("Dirt.jpg")
		defaultimp.layerList.append(layer1)

		layer2 = ogreterrain.Terrain.LayerInstance()
		layer2.worldSize == 256 #I have no idea
		#layer2.textureNames.append("terr_rock6.jpg")
		layer2.textureNames.append("terr_rock-dirt.jpg")
		defaultimp.layerList.append(layer2)

		layer3 = ogreterrain.Terrain.LayerInstance()
		layer3.worldSize == 256 #I have no idea
		layer3.textureNames.append("terr_rock6.jpg")
		#layer3.textureNames.append("terr_rock-dirt.jpg")
		defaultimp.layerList.append(layer3)

		# textures
		# layer0 = ogreterrain.Terrain.LayerInstance()
		# layer0.worldSize = 100
		# layer0.textureNames.append("dirt_grayrocky_diffusespecular.dds")
		# layer0.textureNames.append("dirt_grayrocky_normalheight.dds")
		# defaultimp.layerList.append(layer0)

		# layer1 = ogreterrain.Terrain.LayerInstance()
		# layer1.worldSize = 30
		# layer1.textureNames.append("grass_green-01_diffusespecular.dds")
		# layer1.textureNames.append("grass_green-01_normalheight.dds")
		# defaultimp.layerList.append(layer1)

		# layer2 = ogreterrain.Terrain.LayerInstance()
		# layer2.worldSize = 200
		# layer2.textureNames.append("growth_weirdfungus-03_diffusespecular.dds")
		# layer2.textureNames.append("growth_weirdfungus-03_normalheight.dds")
		# defaultimp.layerList.append(layer2)
		  
	def defineTerrain(self, x, y):
		filename = self.terrainGroup.generateFilename(x, y)
		RGM = ogre.ResourceGroupManager.getSingleton()
		if ( RGM.resourceExists(self.terrainGroup.getResourceGroup(), filename) ):
			self.terrainGroup.defineTerrain(x, y)
		else :
			#img = self.getTerrainImage((x % 2) != 0, (y%2) != 0)
			img = self.getTerrainImage(False, False)
			self.terrainGroup.defineTerrain(x, y, img)
			self.terrainsImported = True
					 
	def getTerrainImage(self, flipX, flipY):
		img = ogre.Image()
		img.load("high.png", ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME)
		if flipX:
			img.flipAroundY()
		if flipY:
			img.flipAroundX() 
		return img
				
	def initBlendMaps(self, terrain):
		blendMap0 = terrain.getLayerBlendMap(1)
		blendMap1 = terrain.getLayerBlendMap(2)
		minHeight0 = 0
		fadeDist0 = 40.0
		minHeight1 = 40.0
		fadeDist1 = 150.0

		print("Variables")

		pBlend1 = blendMap1.getBlendPointer()    # returns the address of the buffer
		size = terrain.getLayerBlendMapSize() * terrain.getLayerBlendMapSize()
		print("getBlendPointer and getLayerBlendMapSize")
		blend_data=(ctypes.c_float * size).from_address(pBlend1)
		index = 0
		print("from_address")
		for y in range(terrain.getLayerBlendMapSize()):
			for x in range( terrain.getLayerBlendMapSize() ):
				# using ctypes
				tx = ctypes.c_float(0.0)
				ty = ctypes.c_float(0.0)
					 
				blendMap0.convertImageToTerrainSpace(x, y, ctypes.addressof(tx), ctypes.addressof(ty))
				#print("convertImageToTerrainSpace")
				height = terrain.getHeightAtTerrainPosition(tx.value, ty.value)
				#print("getHeightAtTerrainPosition")

				val = (height - minHeight0) / fadeDist0
				val = Clamp(val, 0, 1)

				val = (height - minHeight1) / fadeDist1
				val = Clamp(val, 0, 1)
				blend_data [index] = val
				index += 1
		print("Forloop")
		blendMap0.dirty()
		blendMap1.dirty()
		print("Dirty socks")
		blendMap0.update()
		blendMap1.update()
		print("Updates")

	def createTerrainMaterial(self, base, splatting):
		return False
		shared.DPrint("R3DTerrain", 0, "Creating Terrain Material")
		if self.Material!=None:
			self.Material.removeAllTechniques()
			Technique=self.Material.createTechnique()
			basePass=Technique.createPass()
		else:
			self.Material = ogre.MaterialManager.getSingleton().create("Template/Terrain",ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME) 

		Technique=self.Material.getTechnique(0)
		basePass=Technique.getPass(0)
		baseTexture = basePass.createTextureUnitState()
		baseTexture.setTextureName(base)
		baseTexture.setTextureScale(1, 1)

		for texture, alphamap in splatting.iteritems():
			splattingPass = Technique.createPass()
			splattingPass.setLightingEnabled(False)
			splattingPass.setSceneBlending(ogre.SBT_TRANSPARENT_ALPHA)
			splattingPass.setDepthFunction(ogre.CMPF_EQUAL)

			alphamapTexture = splattingPass.createTextureUnitState()
			alphamapTexture.setTextureName(alphamap)
			alphamapTexture.setAlphaOperation(ogre.LBX_SOURCE1, ogre.LBS_TEXTURE, ogre.LBS_TEXTURE)
			alphamapTexture.setColourOperationEx(ogre.LBX_SOURCE2, ogre.LBS_TEXTURE, ogre.LBS_TEXTURE)

			detailTexture = splattingPass.createTextureUnitState()
			detailTexture.setTextureName(texture)
			detailTexture.setTextureScale(0.07, 0.07)
			detailTexture.setColourOperationEx(ogre.LBX_BLEND_DIFFUSE_ALPHA, ogre.LBS_TEXTURE, ogre.LBS_CURRENT)

		# lightingPass = Technique.createPass()
		# lightingPass.setAmbient(1,1,1)
		# lightingPass.setDiffuse(1,1,1,1)
		# lightingPass.setDepthFunction(ogre.CMPF_EQUAL)
		# lightingPass.setSceneBlending(ogre.SBF_ZERO, ogre.SBF_ONE_MINUS_SOURCE_COLOUR )

	def createTerrainCFG(self, terraincfg):
		shared.DPrint("R3DTerrain", 0, "Creating Terrain Config")
		Comment="# Automaticly generated from current map. Do NOT mod this file manually, your changes will only be overwritten!"
		PageSource="Heightmap"
		HeightmapImage=terraincfg["Heightmap"]["Heightmap File"]
		PageSize=str(terraincfg["Heightmap"]["PageSize"])
		TileSize=str(terraincfg["Heightmap"]["TileSize"])
		MaxPixelError="30000"
		PageWorldX=str(terraincfg["Heightmap"]["Scale"][0])
		PageWorldZ=str(terraincfg["Heightmap"]["Scale"][1])
		MaxHeight=str(terraincfg["Heightmap"]["Height"])
		MaxMipMapLevel="5"
		LODMorphStart="0.05"
		CustomMaterialName="Template/Terrain"

		cfgBuffer=Comment+"\nPageSource="+PageSource+"\nHeightmap.image="+HeightmapImage+"\nPageSize="+PageSize+"\nTileSize="+TileSize+"\nMaxPixelError="+MaxPixelError+"\nPageWorldX="+PageWorldX+"\nPageWorldZ="+PageWorldZ+"\nMaxHeight="+MaxHeight+"\nMaxMipMapLevel="+MaxMipMapLevel+"\nLODMorphStart="+LODMorphStart+"\n# YARTS Autoconfig End\n"

		cfgFile=open("./media/terrain2.cfg", "w")
		cfgFile.write(cfgBuffer)
		cfgFile.flush()
		cfgFile.close()

	def RldTerrain(self):
		shared.DPrint("R3DTerrain", 0, "Reloading Terrain Geometry")
		try:
			pass
			#self.sceneManager.setWorldGeometry("terrain2.cfg")
		except:
			print_exc()

	def getHeightAtPos(self, x, z):
		Raytrace=ogre.Ray()
		Raytrace.setOrigin((x,1000,z))
		Raytrace.setDirection(ogre.Vector3().NEGATIVE_UNIT_Y)
		self.raySceneQuery=shared.render3dScene.sceneManager.createRayQuery(Raytrace)
		for queryResult in self.raySceneQuery.execute():
			if queryResult.worldFragment is not None:  
				return 1000-queryResult.distance
