
from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class Debug():
	def __init__(self):
		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

		rootwindow=self.windowManager.getWindow("Root")
		self.FPScounter = self.windowManager.createWindow("TaharezLook/StaticText", "FPScounter")
		self.FPScounter.setText("999")
		self.FPScounter.setPosition(CEGUI.UVector2(CEGUI.UDim(0.5, 0), CEGUI.UDim(0, 0)))
		self.FPScounter.setSize(CEGUI.UVector2(CEGUI.UDim(0.11, 0), CEGUI.UDim(0.05, 0)))
		rootwindow.addChildWindow(self.FPScounter)

		self.DIVcounter = self.windowManager.createWindow("TaharezLook/StaticText", "DIVcounter")
		self.DIVcounter.setText("999")
		self.DIVcounter.setPosition(CEGUI.UVector2(CEGUI.UDim(0.3, 0), CEGUI.UDim(0, 0)))
		self.DIVcounter.setSize(CEGUI.UVector2(CEGUI.UDim(0.11, 0), CEGUI.UDim(0.05, 0)))
		rootwindow.addChildWindow(self.DIVcounter)

		#shared.renderGUI.registerLayout(self.FPScounter)
		#shared.renderGUI.registerLayout(self.DIVcounter)

		self.GuiStats(debug.GUISTATS)
		debug.ACC("dbg_stats", self.GuiStats, info="Show/Hide Debug Stats\nUsage: 1/0", args=1)

	def GuiStats(self, foo):
		if type(foo)==str:
			foo=int(foo)
		if foo:
			self.FPScounter.show()
			self.DIVcounter.show()
		else:
			self.FPScounter.hide()
			self.DIVcounter.hide()
