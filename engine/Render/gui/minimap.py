
from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class Minimap():
	def __init__(self):
		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

		self.Window = self.windowManager.getWindow("Root/Map")
		self.Background = self.windowManager.getWindow("Root/Map/BG")
		self.Image = self.windowManager.getWindow( "Root/Map/BG/Image")

	def Initialize(self):
		self.RttImageset = CEGUI.ImagesetManager.getSingleton().create("RttImageset", shared.MinimapManager.ceguiTexture)
		#self.RttImageset.defineImage("RTT_Minimap", CEGUI.Rect(0.0, 0.0, CEGUI.Size(300, 300)), CEGUI.Vector2(0.0, 0.0))
		self.RttImageset.defineImage("RTT_Minimap", CEGUI.Vector2(0,0), CEGUI.Size(300, 300), CEGUI.Vector2(0,0))
		#self.RttImageset.defineImage("RTT_Minimap",CEGUI.Rect(0.0, 0.0, ceguiTexture.getSize().d_width, ceguiTexture.getSize().d_height), CEGUI.Vector2(0.0, 0.0))
		#self.BasicImage.setTexture("RTT_Minimap")

		#Load minimap
		self.Imageset=CEGUI.ImagesetManager.getSingleton().createFromImageFile("minimapset", "./minimap4.png")
		self.Imageset.defineImage("minimap", CEGUI.Vector2(0,0), CEGUI.Size(300,300),CEGUI.Vector2(0,0))

		#Minimap
		self.Image.setProperty("Image","set:RttImageset image:RTT_Minimap")
		self.Image.subscribeEvent(self.Image.EventMouseEnters, self, "Map_Menter")
		self.Image.subscribeEvent(self.Image.EventMouseLeaves, self, "Map_Mleave")
		self.Image.subscribeEvent(self.Image.EventMouseButtonDown, self, "Map_Mclick")
		self.Image.subscribeEvent(self.Image.EventMouseButtonUp, self, "Map_Mrelease")

		shared.renderGUI.registerLayout(self.Window)

		# self.test = MinimapUnit(0)

		#Load VisibilityImage:
		self.Imageset=CEGUI.ImagesetManager.getSingleton().createFromImageFile("minimapVisibility", "./minimapVisibility.png")
		self.Imageset.defineImage("minimapVisibility", CEGUI.Vector2(0,0), CEGUI.Size(16,16),CEGUI.Vector2(0,0))

		#self.Visibility0 = MinimapVisibility(0, 0.3, 0.3)
		#self.Visibility1 = MinimapVisibility(1, 0.35, 0.35)
		#self.Visibility2 = MinimapVisibility(2, 0.39, 0.39)

	def Map_Menter(self, evt):
		pass

	def Map_Mleave(self, evt):
		pass

	def Map_Mclick(self, evt):
		sTW = CEGUI.CoordConverter.screenToWindow(self.Image, evt.position)
		size = self.Image.getSize().asAbsolute(self.Image.getPixelSize())
		print(sTW.d_y)
		pos = ((sTW.d_x/size.d_x), 1-(sTW.d_y/size.d_y))
		realpos = (shared.Map.size*pos[1], shared.Map.size*pos[0])
		print(realpos)

		if evt.button == CEGUI.LeftButton:
			camdim = shared.render3dCamera.getDimensions()
			#campos = ((camdim[1]/2)+realpos[0], (camdim[0]/2)+realpos[1])
			campos = (realpos[0]-camdim[1]/2, realpos[1])
			print campos
			shared.render3dCamera.set2DPos(campos)
			
			


	def Map_Mrelease(self, evt):
		pass