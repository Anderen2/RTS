#Mapeditor GUI - Popups

from engine import shared, debug

class PopupGUI():
	def __init__(self, poptype, ret, info="Popup"):
		self.root = shared.renderguiGUI.windowManager.getWindow("Root")
		self.layout = shared.renderguiGUI.windowManager.loadWindowLayout(poptype+".layout")

		self.poptype=poptype
		self.ret=ret

		self.layout.setProperty("Text", info)

		self.root.addChildWindow(self.layout)

		self.layout.subscribeEvent(self.layout.EventMouseEnters, shared.globalgui, "W_Menter")
		self.layout.subscribeEvent(self.layout.EventMouseLeaves, shared.globalgui, "W_Mleave")


	def b_OK(self, evt):
		self.ret(evt)

	def b_Cancel(self, evt):
		pass

	def b_Close(self, evt):
		del self