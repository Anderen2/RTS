#GUIsubmodule - borders
#Classes for handeling GUI borders and corners
#By Anderen2 (Oct. 2014)

from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class Borders():
	def __init__(self):
		self.windowManager = CEGUI.WindowManager.getSingleton()
		self.root = self.windowManager.getWindow("Root")

		self.size = 0.003 #HARDCODE
		self.speed = 1.8 #HARDCODE

		self.move = False

		self.RVborder = self.windowManager.createWindow("Vanilla/VerticalScrollbar", "RightVerticalBorder")
		self.RVborder.setPosition(CEGUI.UVector2(CEGUI.UDim(0, 0), CEGUI.UDim(0, 0)))
		self.RVborder.setSize(CEGUI.UVector2(CEGUI.UDim(self.size, 0), CEGUI.UDim(1, 0)))
		self.RVborder.setAlpha(0)
		self.root.addChildWindow(self.RVborder)

		self.LVborder = self.windowManager.createWindow("Vanilla/VerticalScrollbar", "LeftVerticalBorder")
		self.LVborder.setPosition(CEGUI.UVector2(CEGUI.UDim(1-self.size, 0), CEGUI.UDim(0, 0)))
		self.LVborder.setSize(CEGUI.UVector2(CEGUI.UDim(self.size, 0), CEGUI.UDim(1, 0)))
		self.LVborder.setAlpha(0)
		self.root.addChildWindow(self.LVborder)

		self.THborder = self.windowManager.createWindow("Vanilla/HorizontalScrollbar", "TopVerticalBorder")
		self.THborder.setPosition(CEGUI.UVector2(CEGUI.UDim(0, 0), CEGUI.UDim(0, 0)))
		self.THborder.setSize(CEGUI.UVector2(CEGUI.UDim(1, 0), CEGUI.UDim(self.size, 0)))
		self.THborder.setAlpha(0)
		self.root.addChildWindow(self.THborder)

		self.BHborder = self.windowManager.createWindow("Vanilla/HorizontalScrollbar", "BottomVerticalBorder")
		self.BHborder.setPosition(CEGUI.UVector2(CEGUI.UDim(0, 0), CEGUI.UDim(1-self.size, 0)))
		self.BHborder.setSize(CEGUI.UVector2(CEGUI.UDim(1, 0), CEGUI.UDim(self.size, 0)))
		self.BHborder.setAlpha(0)
		self.root.addChildWindow(self.BHborder)

		self.TRCorner = self.windowManager.createWindow("Vanilla/VerticalScrollbarThumb", "TRCorner")
		self.TRCorner.setPosition(CEGUI.UVector2(CEGUI.UDim(0, 0), CEGUI.UDim(0, 0)))
		self.TRCorner.setSize(CEGUI.UVector2(CEGUI.UDim(self.size, 0), CEGUI.UDim(self.size, 0)))
		self.TRCorner.setAlpha(0)
		self.root.addChildWindow(self.TRCorner)

		self.TLCorner = self.windowManager.createWindow("Vanilla/VerticalScrollbarThumb", "TLCorner")
		self.TLCorner.setPosition(CEGUI.UVector2(CEGUI.UDim(1-self.size, 0), CEGUI.UDim(0, 0)))
		self.TLCorner.setSize(CEGUI.UVector2(CEGUI.UDim(self.size, 0), CEGUI.UDim(self.size, 0)))
		self.TLCorner.setAlpha(0)
		self.root.addChildWindow(self.TLCorner)

		self.BRCorner = self.windowManager.createWindow("Vanilla/VerticalScrollbarThumb", "BRCorner")
		self.BRCorner.setPosition(CEGUI.UVector2(CEGUI.UDim(0, 0), CEGUI.UDim(1-self.size, 0)))
		self.BRCorner.setSize(CEGUI.UVector2(CEGUI.UDim(self.size, 0), CEGUI.UDim(self.size, 0)))
		self.BRCorner.setAlpha(0)
		self.root.addChildWindow(self.BRCorner)

		self.BLCorner = self.windowManager.createWindow("Vanilla/VerticalScrollbarThumb", "BLCorner")
		self.BLCorner.setPosition(CEGUI.UVector2(CEGUI.UDim(1-self.size, 0), CEGUI.UDim(1-self.size, 0)))
		self.BLCorner.setSize(CEGUI.UVector2(CEGUI.UDim(self.size, 0), CEGUI.UDim(self.size, 0)))
		self.BLCorner.setAlpha(0)
		self.root.addChildWindow(self.BLCorner)

		self.RVborder.subscribeEvent(self.RVborder.EventMouseEnters, self, "RVEnter")
		self.RVborder.subscribeEvent(self.RVborder.EventMouseLeaves, self, "AllLeave")

		self.LVborder.subscribeEvent(self.LVborder.EventMouseEnters, self, "LVEnter")
		self.LVborder.subscribeEvent(self.LVborder.EventMouseLeaves, self, "AllLeave")

		self.THborder.subscribeEvent(self.THborder.EventMouseEnters, self, "THEnter")
		self.THborder.subscribeEvent(self.THborder.EventMouseLeaves, self, "AllLeave")

		self.BHborder.subscribeEvent(self.BHborder.EventMouseEnters, self, "BHEnter")
		self.BHborder.subscribeEvent(self.BHborder.EventMouseLeaves, self, "AllLeave")

		self.TRCorner.subscribeEvent(self.TRCorner.EventMouseEnters, self, "TREnter")
		self.TRCorner.subscribeEvent(self.TRCorner.EventMouseLeaves, self, "AllLeave")

		self.TLCorner.subscribeEvent(self.TLCorner.EventMouseEnters, self, "TLEnter")
		self.TLCorner.subscribeEvent(self.TLCorner.EventMouseLeaves, self, "AllLeave")
		
		self.BRCorner.subscribeEvent(self.BRCorner.EventMouseEnters, self, "BREnter")
		self.BRCorner.subscribeEvent(self.BRCorner.EventMouseLeaves, self, "AllLeave")

		self.BLCorner.subscribeEvent(self.BLCorner.EventMouseEnters, self, "BLEnter")
		self.BLCorner.subscribeEvent(self.BLCorner.EventMouseLeaves, self, "AllLeave")

		shared.render.Hook.Add("OnRenderFrame", self.Think)

	def AllLeave(self, evt):
		self.move = False

	def RVEnter(self, evt):
		self.move = (-1, 0, 0)

	def LVEnter(self, evt):
		self.move = (1, 0, 0)

	def THEnter(self, evt):
		self.move = (0, 0, -1)

	def BHEnter(self, evt):
		self.move = (0, 0, 1)

	def TREnter(self, evt):
		self.move = (-1, 0, -1)

	def TLEnter(self, evt):
		self.move = (1, 0, -1)

	def BREnter(self, evt):
		self.move = (-1, 0, 1)

	def BLEnter(self, evt):
		self.move = (1, 0, 1)

	def Think(self, delta):
		if self.move:
			shared.render3dCamera.Move(self.move, delta*self.speed)

	def ShowBorders(self):
		self.RVborder.setAlpha(1)
		self.LVborder.setAlpha(1)
		self.THborder.setAlpha(1)
		self.BHborder.setAlpha(1)
		self.TRCorner.setAlpha(1)
		self.TLCorner.setAlpha(1)
		self.BRCorner.setAlpha(1)
		self.BLCorner.setAlpha(1)