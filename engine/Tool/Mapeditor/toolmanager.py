#Mapeditor Tool Manager
#This class manages the different tools
#TOOLS: 0=Select, 1=Move, 2=Rotate, 3=Duplicate

from engine import shared, debug
import movetool

class ToolManager():
	def __init__(self):
		self.CurrentTool=0

	def setTool(self, TID):
		shared.DPrint("ToolManager", 0, "Tool Selected: "+str(TID))
		self.CurrentTool=TID

		if TID!=0:
			#Change renderIO mouse hook to be Tool
			shared.renderioInput.CurrentMiceInterface=3
			#Create a instance of the new tool, delete all else
			#Make backend route the Toolclick's from renderio to the tool
			
		else:
			#Change renderIO mouse hook to be Gui(As the button is on a gui sheet)
			shared.renderioInput.CurrentMiceInterface=2
			self.CurrentToolClass=None

		if TID==1:
			self.CurrentToolClass=movetool.MoveTool()