#Mapeditor GUI - Decorations

from engine import shared, debug

class PropertiesGUI():
	def __init__(self):
		self.root = shared.renderguiGUI.windowManager.getWindow("Root")
		self.layout = shared.renderguiGUI.windowManager.loadWindowLayout("Properties.layout")

		self.root.addChildWindow(self.layout)

	def b_Map(self, evt):
		pass

	def b_Terrain(self, evt):
		pass

	def b_Water(self, evt):
		pass

	def b_Players(self, evt):
		pass

	def b_Save(self, evt):
		pass

	def b_Load(self, evt):
		pass