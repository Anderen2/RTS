#render3dTerrain
#Functions related to modifying and getting realtime data from the terrain

from engine import shared, debug
import ogre.renderer.OGRE as ogre

class Terrain():
	def __init__(self, sceneManager):
		self.Material=None
		self.sceneManager = sceneManager

		#Setup temporary terrain (Is this really nessecary?)
		if self.Material==None:
			self.createTerrainMaterial("2048.png", {"terr_rock-dirt.jpg":"alphamap.png", "grass_1024.jpg":"alphamap2.png"})
		self.sceneManager.setWorldGeometry("terrain.cfg")

		debug.ACC("r.t_reload", self.RldTerrain, info="Reload the terrain", args=0)

	def createTerrainMaterial(self, base, splatting):
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
			self.sceneManager.setWorldGeometry("terrain2.cfg")
		except:
			print_exc()

	def getHeightAtPos(self, x, z):
		Raytrace=ogre.Ray()
		Raytrace.setOrigin((x,1000,z))
		Raytrace.setDirection(ogre.Vector3().NEGATIVE_UNIT_Y)
		self.raySceneQuery=shared.render3dScene.sceneManager.createRayQuery(Raytrace)
		for queryResult in self.raySceneQuery.execute():
			if queryResult.worldFragment is not None:  
				return queryResult.distance
