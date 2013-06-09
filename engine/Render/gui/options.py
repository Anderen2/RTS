
from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class Options():
	def __init__(self):
		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

		self.Window = self.windowManager.getWindow("Root/Options")
		self.Background = self.windowManager.getWindow("Root/Options/BG")

		#Optionsbuttons:
		Options=[]
		for x in xrange(0, 5):
			Options.append(self.windowManager.getWindow("Root/Options/BG/"+str(x)))
			Options[x].subscribeEvent(Options[x].EventMouseButtonDown, self, "Opt"+str(x)+"_Mclick")

	
		Options[0].setProperty("NormalImage", "set:GuiSet image:arrowup")
		Options[0].setProperty("PushedImage", "set:GuiSet image:arrowup")

		Options[1].setProperty("NormalImage", "set:GuiSet image:bagdeinfo")
		Options[1].setProperty("PushedImage", "set:GuiSet image:bagdeinfo")

		Options[2].setProperty("NormalImage", "set:GuiSet image:build")
		Options[2].setProperty("PushedImage", "set:GuiSet image:build")
	
		Options[3].setProperty("NormalImage", "set:GuiSet image:user")
		Options[3].setProperty("PushedImage", "set:GuiSet image:user")
	
		Options[4].setProperty("NormalImage", "set:GuiSet image:arrowdown")
		Options[4].setProperty("PushedImage", "set:GuiSet image:arrowdown")

		shared.renderGUI.registerLayout(self.Window)
	
	def Opt0_Mclick(self, evt):
 		pass

 	def Opt1_Mclick(self, evt):
 		#Map/Aliances
 		if evt.button==CEGUI.LeftButton:
 			shared.unitHandeler.CreateMov(3,1,1,"robot")

 	def Opt2_Mclick(self, evt):
 		#Nearest free worker
 		if evt.button==CEGUI.LeftButton:
 			if self.windowManager.getWindow("Root/UnitInfo").isChild("Root/UnitInfo/BG/NoSel"):
 				self.windowManager.getWindow("Root/UnitInfo").removeChildWindow("Root/UnitInfo/BG/NoSel")
 				self.windowManager.getWindow("Root/UnitInfo").addChildWindow(self.UnitQueue)
 			else:
 				self.windowManager.getWindow("Root/UnitInfo").removeChildWindow("Root/UnitInfo/BG/UnitQueue")
 				self.windowManager.getWindow("Root/UnitInfo").addChildWindow(self.NoSel)

 	def Opt3_Mclick(self, evt):
 		#Pausemenu
 		if evt.button==CEGUI.LeftButton:
 			for x in range(1,10):
 				shared.unitHandeler.CreateMov(3,1,1,"robot")

 	def Opt4_Mclick(self, evt):
 		#Hide Gui
 		pass