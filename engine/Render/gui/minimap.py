
from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class Minimap():
	def __init__(self):
		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

		self.Window = self.windowManager.getWindow("Root/Map")
		self.Background = self.windowManager.getWindow("Root/Map/BG")
		self.Image = self.windowManager.getWindow( "Root/Map/BG/Image")

		#Load minimap
		self.Imageset=CEGUI.ImagesetManager.getSingleton().createFromImageFile("minimapset", "./minimap.png")
		self.Imageset.defineImage("minimap", CEGUI.Vector2(0,0), CEGUI.Size(290,290),CEGUI.Vector2(0,0))

		#Minimap
		self.Image.setProperty("Image","set:minimapset image:minimap")
		self.Image.subscribeEvent(self.Image.EventMouseEnters, self, "Map_Menter")
		self.Image.subscribeEvent(self.Image.EventMouseLeaves, self, "Map_Mleave")
		self.Image.subscribeEvent(self.Image.EventMouseButtonDown, self, "Map_Mclick")
		self.Image.subscribeEvent(self.Image.EventMouseButtonUp, self, "Map_Mrelease")

		shared.renderGUI.registerLayout(self.Window)

	def Map_Menter(self, evt):
 		pass

 	def Map_Mleave(self, evt):
 		pass

 	def Map_Mclick(self, evt):
 		pass

 	def Map_Mrelease(self, evt):
 		pass