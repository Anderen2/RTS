#Mapeditor GUI - Decorations

from engine import shared, debug

class ToolsGUI():
	def __init__(self):
		self.root = shared.renderguiGUI.windowManager.getWindow("Root")
		self.layout = shared.renderguiGUI.windowManager.loadWindowLayout("Tools.layout")

		self.root.addChildWindow(self.layout)

	def b_Sel(self, evt):
		pass

	def b_Move(self, evt):
		pass

	def b_Rot(self, evt):
		pass

	def b_Dupl(self, evt):
		pass
