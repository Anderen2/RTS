#Tool Context Options

from engine import debug, shared
from traceback import print_exc

class contextTools():
	def __init__(self):
		self.options=["Select", "Move (Ground)", "Move (Y-Axis)", "Move (Gnd, Y-Lock)","Move (X/Z-Axis)", "Rotate (Z)", "Rotate (Y)", "Rotate (X)", "Save", "Load"]
		self.optfunc=[self.sSelect, self.sMoveGnd, self.sMoveY, self.sMoveGndYLock, self.sMoveXZ, self.sRotateZ, self.sRotateY, self.sRotateX, self.sSave, self.sLoad]

	def sSelect(self):
		shared.toolManager.setTool(0)

	def sMoveGnd(self):
		shared.toolManager.setTool(1)

	def sMoveY(self):
		shared.toolManager.setTool(1,1)

	def sMoveGndYLock(self):
		shared.toolManager.setTool(1,2)

	def sMoveXZ(self):
		shared.toolManager.setTool(1,3)

	def sRotateZ(self):
		shared.toolManager.setTool(2)

	def sRotateY(self):
		shared.toolManager.setTool(2,1)

	def sRotateX(self):
		shared.toolManager.setTool(2,2)

	def sSave(self):
		layout={"Save": {"Filename":"str", "Working Directory":"str", "None":"str"}}
		config={"Save": {"Filename":shared.Map.mapname, "Working Directory":shared.wd, "None":"none"}}
		shared.globalGUI.OptionsGUI.ask("Save Map", self.callbackSave, layout, config)

	def sLoad(self):
		layout={"Load": {"Filename":"str", "Working Directory":"str", "None":"str"}}
		config={"Load": {"Filename":"nice.map", "Working Directory":shared.wd, "None":"none"}}
		shared.globalGUI.OptionsGUI.ask("Load Map", self.callbackLoad, layout, config)

	def callbackSave(self,config):
		filename=config["Save"]["Filename"]
		workingdir=config["Save"]["Working Directory"]
		try:
			shared.Mapfile.Save(workingdir+filename)
			shared.Map.mapname = filename
		except:
			print("FAILED TO SAVE MAP!")
			print("FAILED TO SAVE MAP!")
			print("FAILED TO SAVE MAP!")
			print("FAILED TO SAVE MAP!")
			print("FAILED TO SAVE MAP!")
			print_exc()
			print("FAILED TO SAVE MAP!")
			print("FAILED TO SAVE MAP!")
			print("FAILED TO SAVE MAP!")
			print("FAILED TO SAVE MAP!")
			print("FAILED TO SAVE MAP!")

	def callbackLoad(self, config):
		filename=config["Load"]["Filename"]
		workingdir=config["Load"]["Working Directory"]
		shared.wd=workingdir

		shared.decHandeler._del() #Clear all decorations from the map
		shared.MapLoader.Load(filename).Setup() #Setup new map
		shared.Mapfile.Load() #Setup mapconfig for new map 