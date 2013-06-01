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

		OkBtn=shared.renderguiGUI.windowManager.getWindow("Popup/OK")
		CancelBtn=shared.renderguiGUI.windowManager.getWindow("Popup/Cancel")

		OkBtn.subscribeEvent(OkBtn.EventMouseButtonDown, self, "b_OK")
		CancelBtn.subscribeEvent(CancelBtn.EventMouseButtonDown, self, "b_Cancel")

		shared.globalGUI.registerLayout(self.layout)
		shared.renderioInput.takeKeyFocus("popupgui")


	def b_OK(self, evt):
		print("1")
		data=""
		shared.renderioInput.looseKeyFocus("popupgui")
		print("2")
		#self.ret(evt, data)

	def b_Cancel(self, evt):
		shared.renderioInput.looseKeyFocus("popupgui")
		self.ret(evt, data)

	def b_Close(self, evt):
		shared.renderioInput.looseKeyFocus("popupgui")
		self.ret(evt, data)