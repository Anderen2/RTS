
from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class GameInfo():
	def __init__(self):
		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

		self.Window=self.windowManager.getWindow("Root/GameInfo")
		self.Background=self.windowManager.getWindow("Root/GameInfo/BG")

		#Gameinfo
		self.Title=self.windowManager.getWindow("Root/GameInfo/BG/Title")
		self.Title.subscribeEvent(self.Title.EventMouseEnters, self, "GameInfo_Menter")
		self.Title.subscribeEvent(self.Title.EventMouseLeaves, self, "GameInfo_Mleave")
		self.Title.subscribeEvent(self.Title.EventMouseButtonDown, self, "GameInfo_TitleClick")

		self.Log=self.windowManager.getWindow("Root/GameInfo/BG/History")
		self.Log.subscribeEvent(self.Log.EventMouseEnters, self, "GameInfo_Menter")
		self.Log.subscribeEvent(self.Log.EventMouseLeaves, self, "GameInfo_Mleave")

		self.Window.setAlpha(0.2)

		shared.renderGUI.registerLayout(self.Window)

	def GameInfo_Menter(self, evt):
		if self.Background.getAlpha()!=0:
			self.Background.setAlpha(1)

	def GameInfo_Mleave(self, evt):
		if self.Background.getAlpha()!=0:
			self.Background.setAlpha(0.2)

	def GameInfo_TitleClick(self, evt):
		if evt.button==CEGUI.LeftButton:
			print("This is a beta..")
			shared.DPrint("RenderGUI",0,"Beta: Wth?")

		elif evt.button==CEGUI.RightButton:
			if self.Background.getAlpha()!=0:
				self.Log.hide()
				self.Title.setInheritsAlpha(False)
				self.Background.setAlpha(0)
			else:
				self.Log.show()
				self.Title.setInheritsAlpha(True)
				self.Background.setAlpha(1)