#Base Mapeditor Class

from string import split
from engine import shared, debug
from engine.Tool.Mapeditor import decorationgui, toolsgui, propertiesgui
import ogre.gui.CEGUI as CEGUI

class MapeditorGUI():
	def __init__(self):
		shared.globalgui=self
		self.globalpha=0.9
		self.upperalpha=0.5
	
	def Setup(self):
		self.hackhz, self.hackvz = shared.render3dCamera.getDimensions()

		self.sheet = CEGUI.WindowManager.getSingleton().loadWindowLayout("empty.layout")
		shared.renderguiGUI.system.setGUISheet(self.sheet)

		#Defaults
		shared.renderguiGUI.system.setDefaultMouseCursor("TaharezLook", "MouseArrow")
		shared.renderguiGUI.system.setDefaultFont("BlueHighway-12")
		CEGUI.MouseCursor.getSingleton().setImage("TaharezLook", "MouseArrow")

		#Create rest of GUI elements
		self.DecorationGUI=decorationgui.DecorationGUI()
		PropertiesGUI=propertiesgui.PropertiesGUI()
		ToolsGUI=toolsgui.ToolsGUI()

		#Loop through all the GUI elements to add window movement
		print("!"*20)
		print(shared.renderguiGUI.windowManager.getWindow("Root").getChildCount())

		for x in self.iterChilds("Root"):
			x.setAlpha(0.5)
			x.subscribeEvent(x.EventMouseEnters, self, "W_Menter")
			x.subscribeEvent(x.EventMouseLeaves, self, "W_Mleave")
			x.subscribeEvent(x.EventMouseButtonDown, self, "W_Mclick")
			x.subscribeEvent(x.EventMouseButtonUp, self, "W_Mrelease")
			x.subscribeEvent(x.EventMouseMove, self, "MouseMoving")
			for y in self.iterChilds(x.getName()):
				y.subscribeEvent(y.EventMouseEnters, self, "W_Menter")
				y.subscribeEvent(y.EventMouseLeaves, self, "W_Mleave")
				for z in self.iterChilds(y.getName()):
					z.subscribeEvent(z.EventMouseEnters, self, "W_Menter")
					z.subscribeEvent(z.EventMouseLeaves, self, "W_Mleave")
			print(x)

	def iterChilds(self, window):
		element=shared.renderguiGUI.windowManager.getWindow(window)
		childcount=element.getChildCount()
		if childcount!=0:
			for x in xrange(0, childcount):
				yield element.getChildAtIdx(x)
		else:
			pass

	def MouseMoving(self, evt):
		pass

	def W_Menter(self, evt):
		print evt.window.getName()
		print split("name", "a")
		if "/" in str(evt.window.getName()):
			parentwindow=split(str(evt.window.getName()),"/")[0]
			shared.renderguiGUI.windowManager.getWindow(parentwindow).setAlpha(1)
		else:
			evt.window.setAlpha(1)

		self.OldInterface=shared.renderioInput.CurrentMiceInterface
		shared.renderioInput.CurrentMiceInterface=1

	def W_Mleave(self, evt):
		if "/" in str(evt.window.getName()):
			parentwindow=split(str(evt.window.getName()),"/")[0]
			shared.renderguiGUI.windowManager.getWindow(parentwindow).setAlpha(0.5)
		else:
			evt.window.setAlpha(0.5)

		if shared.renderioInput.CurrentMiceInterface==1:
 			if self.OldInterface!=1:
 				shared.renderioInput.CurrentMiceInterface=self.OldInterface
 			else:
 				shared.renderioInput.CurrentMiceInterface=2

	def W_Mclick(self, evt):
		pass

	def W_Mrelease(self, evt):
		pass