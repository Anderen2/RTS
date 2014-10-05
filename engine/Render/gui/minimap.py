
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

		#self.test = MinimapUnit(0)

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
 		pass

 	def Map_Mrelease(self, evt):
 		pass

class MinimapUnit():

	def __init__(self, ID):
		self.windowManager = CEGUI.WindowManager.getSingleton()
		self.minimap = self.windowManager.getWindow("Root/Map/BG/Image")
		self.dot = self.windowManager.createWindow("Vanilla/StaticImage", "GreenDot")
		self.minimap.addChildWindow(self.dot)

		#Load Image:
		self.Imageset=CEGUI.ImagesetManager.getSingleton().createFromImageFile("minimapUnit", "./minimapGreenDot.png")
		self.Imageset.defineImage("minimapUnit", CEGUI.Vector2(0,0), CEGUI.Size(16,16),CEGUI.Vector2(0,0))
		self.dot.setProperty("Image","set:minimapUnit image:minimapUnit")
		self.dot.setProperty("FrameEnabled", "False")
		self.dot.setProperty("BackgroundEnabled", "False")

		self.dot.setPosition(CEGUI.UVector2(CEGUI.UDim(0.5, 0), CEGUI.UDim(0.5, 0)))
		self.dot.setSize(CEGUI.UVector2(CEGUI.UDim(0.05, 0), CEGUI.UDim(0.05, 0)))
		
class MinimapVisibility():
	def __init__(self, ID, x, y):
		self.windowManager = CEGUI.WindowManager.getSingleton()
		self.minimap = self.windowManager.getWindow("Root/Map/BG/Image")
		self.dot = self.windowManager.createWindow("Vanilla/StaticImage", "Visibility"+str(ID))
		self.minimap.addChildWindow(self.dot)

		
		self.dot.setProperty("Image","set:minimapVisibility image:minimapVisibility")
		self.dot.setProperty("FrameEnabled", "False")
		self.dot.setProperty("BackgroundEnabled", "False")

		self.dot.setPosition(CEGUI.UVector2(CEGUI.UDim(x, 0), CEGUI.UDim(y, 0)))
		self.dot.setSize(CEGUI.UVector2(CEGUI.UDim(0.1, 0), CEGUI.UDim(0.1, 0)))