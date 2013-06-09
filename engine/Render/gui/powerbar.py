
from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class Powerbar():
	def __init__(self):
		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

		self.Window = self.windowManager.getWindow("Root/Power")
		self.Background = self.windowManager.getWindow("Root/Power/BG")
		self.Bar = self.windowManager.getWindow("Root/Power/BG/Bar")

		self.Bar.setProperty("CurrentProgress", "0.5")
		self.Bar.subscribeEvent(self.Bar.EventMouseButtonDown, self, "Pwr_Mclick")

		shared.renderGUI.registerLayout(self.Window)

	def Pwr_Mclick(self, evt):
 		if evt.button==CEGUI.LeftButton:
 			print("Overclock engaged!")