
from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class Chat():
	def __init__(self):
		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

		self.Window = self.windowManager.getWindow("Root/Chat")
		self.Background = self.windowManager.getWindow("Root/Chat/BG")
		self.Title = self.windowManager.getWindow("Root/Chat/BG/Title")
		self.Textfield = self.windowManager.getWindow("Root/Chat/BG/Type")
		self.Log = self.windowManager.getWindow("Root/Chat/BG/History")
		self.Scroll = self.windowManager.getWindow("Root/Chat/BG/History__auto_vscrollbar__")

		self.Title.subscribeEvent(self.Title.EventMouseEnters, self, "Chat_Menter")
		self.Title.subscribeEvent(self.Title.EventMouseLeaves, self, "Chat_Mleave")
		self.Title.subscribeEvent(self.Title.EventMouseButtonDown, self, "Chat_TitleClick")

		self.Textfield.subscribeEvent(self.Textfield.EventMouseEnters, self, "Chat_Menter")
		self.Textfield.subscribeEvent(self.Textfield.EventMouseLeaves, self, "Chat_Mleave")

		self.Scroll.subscribeEvent(self.Scroll.EventMouseEnters, self, "Chat_Menter")
		self.Scroll.subscribeEvent(self.Scroll.EventMouseLeaves, self, "Chat_Mleave")

		self.Log.subscribeEvent(self.Log.EventMouseEnters, self, "Chat_Menter")
		self.Log.subscribeEvent(self.Log.EventMouseLeaves, self, "Chat_Mleave")
		self.Log.setReadOnly(True)

		self.Window.setAlpha(0.2)

		shared.renderGUI.registerLayout(self.Window)

	def setChatLog(self, log):
		self.Log.setText(log)

	def Chat_TitleClick(self, evt):
		if evt.button==CEGUI.LeftButton:
			evt.window.setText("Chat: Team")

		elif evt.button==CEGUI.RightButton:
			if self.Background.getAlpha()!=0:
				self.Textfield.hide()
				self.Log.hide()
				self.Title.setInheritsAlpha(False)
				self.Background.setAlpha(0)

			else:
				self.Textfield.show()
				self.Log.show()
				self.Title.setInheritsAlpha(True)
				self.Background.setAlpha(1)

	def Chat_Menter(self, evt):
		if self.Background.getAlpha()!=0:
			self.Window.setAlpha(1)

	def Chat_Mleave(self, evt):
		if self.Background.getAlpha()!=0:
			self.Window.setAlpha(0.2)