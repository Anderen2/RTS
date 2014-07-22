#render3dTerrain
#Functions related to modifying and getting realtime data from the terrain

from engine import shared, debug
import ogre.renderer.OGRE as ogre
import ogre.renderer.ogreterrain as ogreterrain
from traceback import print_exc
from platform import system as platform

def Clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

# Terrain Queryflag:
MASK_TERRAIN = 1 << 0

class Terrain():
	def __init__(self, sceneManager):
		self.Material=None
		self.sceneManager = sceneManager

		self.terrainGlobals = ogreterrain.TerrainGlobalOptions()
		debug.ACC("t_set", self.setHeightAtPos, args=4, info="Set height at pos. \nUsage: X Y Z Height")
		debug.ACC("t_sw", self.setHeightAtWPos, args=3, info="Set height at worldpos. \nUsage: X Y Height")
		debug.ACC("t_crater", self.createCrater, args=4, info="Create an crater. \nUsage: X Y Height Width")

	def configureTerrainDefaults(self, light, base, splatting):
		self.terrainGlobals.setMaxPixelError(32) # Level Of Detail at distance ## FUTURE GFX OPTION! 
		self.terrainGlobals.setCompositeMapDistance(100) #Distance before texture gets fucked up (Irrelevant now with the custom material)

		defaultimp = self.terrainGroup.getDefaultImportSettings()

		defaultimp.inputScale = self.MaxHeight #Height of terrain
		defaultimp.minBatchSize = 3 #Minimum polycount @ each batch
		defaultimp.maxBatchSize = 33 #Maximum polycount @ each batch (Not really polycount, but close enough)
		  
	def defineTerrain(self, x, y):
		img = ogre.Image()
		img.load(self.HeightmapImage, ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME)
		self.terrainGroup.defineTerrain(x, y, img)
		self.terrainsImported = True

	def createTerrainMaterial(self, base, splatting):
		shared.DPrint("R3DTerrain", 0, "Creating Terrain Material")
		self.Material = self.TerrainMaterial
		if self.Material!=None:
			self.Material.removeAllTechniques()
			Technique=self.Material.createTechnique()
			basePass=Technique.createPass()

		Technique=self.Material.getTechnique(0)
		basePass=Technique.getPass(0)
		baseTexture = basePass.createTextureUnitState()
		baseTexture.setTextureName(base)
		baseTexture.setTextureScale(1, 1)

		if platform() != "L1inux": #FGLRX/Catalyst on Linux is so shitty that they broke blendmaps in their latest driver (So if we are running linux, only use basetexture (FIXED)) ## FUTURE GFX OPTION!
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

	def createTerrainCFG(self, terraincfg):
		shared.DPrint("R3DTerrain", 0, "Creating Terrain Config")
		self.HeightmapImage = terraincfg["Heightmap"]["Heightmap File"]
		self.MaxHeight = terraincfg["Heightmap"]["Height"]
		self.PageWorldX = terraincfg["Heightmap"]["Scale"][0]
		self.PageWorldZ = terraincfg["Heightmap"]["Scale"][1]
		self.TerrainSize = terraincfg["Heightmap"]["Size"]
		#self.PageSize = 1500
		self.TileSize = terraincfg["Heightmap"]["TileSize"]

		self.terrainGroup = ogreterrain.TerrainGroup(self.sceneManager, ogreterrain.Terrain.ALIGN_X_Z, 257, self.TerrainSize) #Scene, Orientation, Batchsize, Terrain Size ## FUTURE GFX OPTION! (Batchsize)
		self.terrainGroup.setFilenameConvention("BasicTutorial3Terrain", "dat")
		self.terrainGroup.setOrigin(ogre.Vector3(0, 0, 0))

		self.configureTerrainDefaults("light", None, None)

		self.defineTerrain(0, 0)
		self.terrainGroup.loadAllTerrains(True)

	def LoadTerrain(self):
		shared.DPrint("R3DTerrain", 0, "Loading Terrain Geometry")
		try:
			pass
		except:
			print_exc()

		self.terrainGroup.getTerrain(0,0).setPosition(ogre.Vector3(self.TerrainSize/2, 0, self.TerrainSize/2))
		self.TerrainMaterial = self.terrainGroup.getTerrain(0,0).getMaterial()
		self.TerrainEnt = self.terrainGroup.getTerrain(0,0)
		self.TerrainEnt.setQueryFlags(MASK_TERRAIN)

		#self.terrainGroup.getTerrain(0,0).setHeightAtPoint(50,50,1000)
		#self.terrainGroup.getTerrain(0,0).dirty()
		#self.terrainGroup.getTerrain(0,0).updateGeometry()

		self.terrainGroup.freeTemporaryResources()
		

	def getHeightAtPos(self, x, z):
		return self.TerrainEnt.getHeightAtWorldPosition(int(x), 1000, int(z))
		
	def setHeightAtPos(self, x, y, z, h):
		terrainpos = ogre.Vector3()
		self.TerrainEnt.getTerrainPosition(float(x), float(y), float(z), terrainpos)
		print x,y,z
		print terrainpos
		self.TerrainEnt.setHeightAtPoint(long(x), long(y), float(h))
		self.terrainGroup.getTerrain(0,0).dirty()
		self.terrainGroup.getTerrain(0,0).updateGeometry()

	def setHeightAtWPos(self, x, y, h):
		x = float(x)
		y = float(y)
		h = int(h)

		TX = 0
		TY = 255

		WX = float(x/1500) * 255 ## (HARDCODE)
		WY = float(y/1500) * 255 ## (HARDCODE)

		RX = WX
		RY = TY - WY

		self.setHeightAtPos(RX, RY, 0, h)

	def createCrater(self, x, y, h, w): #Work In Progress (Not working ATM!)
		x = int(x)
		y = int(y)
		h = int(h)
		w = int(w)

		changelist = [(x,y)]

		#Add horizontal and vertical positions
		for a in xrange(w):
			print a
			changelist.append((x+a, y))
			changelist.append((x-a, y))
			changelist.append((x, y+a))
			changelist.append((x, y-a))

		#Add the other positions
		for a in xrange(w-1):
			changelist.append((x+a, y+a))
			changelist.append((x+a, y-a))
			changelist.append((x-a, y-a))
			changelist.append((x-a, y+a))

		for pos in changelist:
			self.setHeightAtWPos(pos[0], pos[1], h)
