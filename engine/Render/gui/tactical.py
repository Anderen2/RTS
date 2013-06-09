
from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class Tactical():
	def __init__(self):
		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

		self.Window = self.windowManager.getWindow("Root/Tactical")
		self.Background = self.windowManager.getWindow("Root/Tactical/BG")
		self.Buttons = []

		#Tacticalbuttons
		foo=["0","1","2","3","4"]
		for x in foo:
			bar=self.windowManager.getWindow("Root/Tactical/BG/"+x)
			bar.subscribeEvent(bar.EventMouseButtonDown, self, "Tact"+x+"_Mclick")
			self.Buttons.append(bar)

		shared.renderGUI.registerLayout(self.Window)

	def Tact0_Mclick(self, evt):
 		pass

 	def Tact1_Mclick(self, evt):
 		pass

 	def Tact2_Mclick(self, evt):
 		pass

 	def Tact3_Mclick(self, evt):
 		pass

 	def Tact4_Mclick(self, evt):
 		pass