
from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class UnitInfo():
	def __init__(self):
		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

		self.Window = self.windowManager.getWindow("Root/UnitInfo")
		self.NoSel = self.windowManager.loadWindowLayout("NoSel.layout")
		self.UnitQueue = self.windowManager.loadWindowLayout("UnitQueue.layout")

		self.Window.addChildWindow(self.UnitQueue)
		self.Window.addChildWindow(self.NoSel)

		shared.renderGUI.registerLayout(self.Window)

		self.Window.removeChildWindow("Root/UnitInfo/BG/UnitQueue")