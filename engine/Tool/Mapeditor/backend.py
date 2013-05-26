#Mapeditor Backend
#This is the glue that keeps all the stuff together
#Glues the director, the guis and the mapedior(Main Module)

from engine import shared, debug

class MapeditorBackend():
	def __init__(self):
		debug.ACC("dec_add", self.Add, info="Add a decorator to the map", args=1)
		debug.ACC("dec_remove", self.Remove, info="", args=1)
		debug.ACC("dec_mod", self.Modify, info="", args=2)
		debug.ACC("tool_select", self.Select, info="", args=0)
		debug.ACC("tool_move", self.Move, info="", args=0)
		debug.ACC("tool_rot", self.Rotate, info="", args=0)
		debug.ACC("tool_dupe", self.Duplicate, info="", args=0)

	#Directorevents
	def newSelection(self, selection):
		pass

	def rightClick_with_selection(self, pos):
		pass

	def rightClick_on_Unit(self, data):
		pass
	
	#RenderIO Events (When a tool is selected)
	def MousePressed(self, id):
		if shared.toolManager.CurrentTool!=0:
			shared.toolManager.CurrentToolClass.MousePressed()

	def MouseReleased(self, id):
		if shared.toolManager.CurrentTool!=0:
			shared.toolManager.CurrentToolClass.MouseReleased()

	#GUI Events
	#	Decoratorevents
	def Add(self, data):
		shared.decHandeler.Create(data)

	def Remove(self, data):
		shared.decHandeler.Delete(int(data))

	def Modify(self, data, properties):
		pass

	#	Toolsevents
	def Select(self):
		shared.toolManager.setTool(0)

	def Move(self):
		shared.toolManager.setTool(1)

	def Rotate(self):
		shared.toolManager.setTool(2)

	def Duplicate(self):
		shared.toolManager.setTool(3)

	#	PropertiesEvents
	def Map(self, data):
		pass

	def Terrain(self, data):
		pass

	def Water(self, data):
		pass

	def Players(self, data):
		pass

	def Save(self):
		pass

	def Load(self):
		pass