
from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class Moneybar():
	def __init__(self):
		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

		self.Window = self.windowManager.getWindow("Root/Money")
		self.Background = self.windowManager.getWindow("Root/Money/BG")
		self.Text = self.windowManager.getWindow("Root/Money/BG/Text")

		self.Text.setProperty("Text", "$ 9001")
		self.Text.subscribeEvent(self.Text.EventMouseButtonDown, self, "Cash_Mclick")

		shared.renderGUI.registerLayout(self.Window)

	def Cash_Mclick(self, evt):
 		if evt.button==CEGUI.LeftButton:
 			print("Its over ninethousaaaaaaaaaaaannnddd!")