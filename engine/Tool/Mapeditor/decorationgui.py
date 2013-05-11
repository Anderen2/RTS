#Mapeditor GUI - Decorations

from engine import shared, debug
from engine.Tool.Mapeditor import popupgui
import ogre.gui.CEGUI as CEGUI

class DecorationGUI():
	def __init__(self):

		#Bad habbit, but fuckit
		WM = shared.renderguiGUI.windowManager

		self.root = shared.renderguiGUI.windowManager.getWindow("Root")
		self.layout = shared.renderguiGUI.windowManager.loadWindowLayout("Decoration.layout")

		self.root.addChildWindow(self.layout)

		Add=WM.getWindow("Deco/Add")
		Add.subscribeEvent(Add.EventMouseButtonDown, self, "_Add")

		Mod=WM.getWindow("Deco/Mod")
		Mod.subscribeEvent(Mod.EventMouseButtonDown, self, "_Mod")

		RM=WM.getWindow("Deco/RM")
		RM.subscribeEvent(RM.EventMouseButtonDown, self, "_RM")

		AddRecent=WM.getWindow("Deco/AddRecent")
		AddRecent.subscribeEvent(AddRecent.EventMouseButtonDown, self, "_AddRecent")

	def _Add(self, evt):
		print("Addign")
		popup=popupgui.PopupGUI("Textbox",self.AddAnswer,"Enter entity name")

	def AddAnswer(self, data):
		print(data)
		del popup

	def _RM(self, evt):
		print("Removing")

	def _Mod(self, evt):
		print("Modding")

	def _AddRecent(self, evt):
		print("Recenting")

	