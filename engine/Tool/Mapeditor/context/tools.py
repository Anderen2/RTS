#Tool Context Options

from engine import debug, shared

class contextTools():
	def __init__(self):
		self.options=["Select", "Move (Ground)", "Move (Y-Axis)", "Move (Free)", "Rotate (Z)", "Rotate (Y)", "Rotate (X)"]
		self.optfunc=[self.sSelect, self.sMoveGnd, self.sMoveY, self.sMoveFree, self.sRotateZ, self.sRotateY, self.sRotateX]

	def sSelect(self):
		shared.toolManager.setTool(0)

	def sMoveGnd(self):
		shared.toolManager.setTool(1)

	def sMoveY(self):
		shared.toolManager.setTool(1,1)

	def sMoveFree(self):
		shared.toolManager.setTool(1,2)

	def sRotateZ(self):
		shared.toolManager.setTool(2)

	def sRotateY(self):
		shared.toolManager.setTool(2,1)

	def sRotateX(self):
		shared.toolManager.setTool(2,2)