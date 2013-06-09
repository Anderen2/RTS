
from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class UnitOpt():
	def __init__(self):
		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

		self.Window=self.windowManager.getWindow("Root/UnitOpt")
		self.Background=self.windowManager.getWindow("Root/UnitOpt/BG")
		self.Actions=self.windowManager.getWindow("Root/UnitOpt/BG/Actions")
		self.Upgrades=self.windowManager.getWindow("Root/UnitOpt/BG/Upgrades")

		#Create "ActionButtons"
		self.actionbuttons=range(14)
		space=0.01380952380952381
		borderv=0.028
		btnh=0.12904761904761903
		btnv=0.46333333333333333
		fv=borderv
		fh=space
		foo=0
		#Top row
		while foo<7:
			fh=space+foo*(btnh+space)
			self.actionbuttons[foo] = self.windowManager.createWindow("TaharezLook/Button", "Root/UnitOpt/BG/Actions/"+str(foo))
			self.actionbuttons[foo].setText("Act "+str(foo))
			self.actionbuttons[foo].setPosition(CEGUI.UVector2(CEGUI.UDim(fh, 0), CEGUI.UDim(fv, 0)))
			self.actionbuttons[foo].setSize(CEGUI.UVector2(CEGUI.UDim(btnh, 0), CEGUI.UDim(btnv, 0)))
			self.actionbuttons[foo].subscribeEvent(self.actionbuttons[foo].EventMouseButtonDown, self, "Act_Mclick")
			self.Actions.addChildWindow(self.actionbuttons[foo])
			foo+=1

		fv=borderv+btnv+space
		fh=space
		foo=0
		#Bottom row
		while foo<7:
			fh=space+foo*(btnh+space)
			self.actionbuttons[foo] = self.windowManager.createWindow("TaharezLook/Button", "Root/UnitOpt/BG/Actions/"+str(foo+7))
			self.actionbuttons[foo].setText("Act "+str(foo+7))
			self.actionbuttons[foo].setPosition(CEGUI.UVector2(CEGUI.UDim(fh, 0), CEGUI.UDim(fv, 0)))
			self.actionbuttons[foo].setSize(CEGUI.UVector2(CEGUI.UDim(btnh, 0), CEGUI.UDim(btnv, 0)))
			self.actionbuttons[foo].subscribeEvent(self.actionbuttons[foo].EventMouseButtonDown, self, "Act_Mclick")
			self.Actions.addChildWindow(self.actionbuttons[foo])
			foo+=1

		#Create "UpgradeImages"
		self.upgradeimages=range(9)
		borderh=0.036923076923076925
		borderv=0.028
		btnh=0.3076923076923077
		btnv=0.31
		fv=borderv
		fh=borderh
		bar=0
		foobar=0
		while bar<3:
			foo=0
			while foo<3:
				fh=borderh+foo*(btnh)
				self.upgradeimages[foo] = self.windowManager.createWindow("TaharezLook/StaticImage", "Root/UnitOpt/BG/Upgrades/"+str(foobar))
				#self.upgradeimages[foo].setText("U"+str(foobar))
				self.upgradeimages[foo].setPosition(CEGUI.UVector2(CEGUI.UDim(fh, 0), CEGUI.UDim(fv, 0)))
				self.upgradeimages[foo].setSize(CEGUI.UVector2(CEGUI.UDim(btnh, 0), CEGUI.UDim(btnv, 0)))
				self.upgradeimages[foo].subscribeEvent(self.upgradeimages[foo].EventMouseButtonDown, self, "Upg_Mclick")
				self.Upgrades.addChildWindow(self.upgradeimages[foo])
				foo+=1
				foobar+=1
			fv=borderv+btnv+bar*(btnv)
			bar+=1

		shared.renderGUI.registerLayout(self.Window)

	def Act_Mclick(self, evt):
 		if evt.button==CEGUI.LeftButton:
	 		action=str(evt.window.getName())
	 		baction=action[24:]
	 		print baction

	def Upg_Mclick(self, evt):
		pass