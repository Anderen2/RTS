
from engine import shared, debug
import ogre.gui.CEGUI as CEGUI
from string import split

class UnitInfo():
	def __init__(self):
		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

		self.Window = self.windowManager.getWindow("Root/UnitInfo")
		self.NoSel = self.windowManager.loadWindowLayout("NoSel.layout")
		self.UnitQueue = self.windowManager.loadWindowLayout("UnitQueue.layout")

		self.Window.addChildWindow(self.UnitQueue)
		self.Window.addChildWindow(self.NoSel)

		shared.renderGUI.registerLayout(self.Window)

		#self.Window.removeChildWindow("Root/UnitInfo/BG/UnitQueue")
		self.UnitQueue.hide()

		self.queuedActions = []
		self.queuedActionWindows = []
		self.currentGroup = None
		self.currentView = self.NoSel

		self.loadImageset()

	def loadImageset(self):
		#Load minimap
		self.Imageset=CEGUI.ImagesetManager.getSingleton().createFromImageFile("actionimages", "./actionimages.png")
		self.Imageset.defineImage("move", CEGUI.Vector2(0,0), CEGUI.Size(128,128), CEGUI.Vector2(0,0))

	def updateQueue(self):
		self.queuedActions = self.currentGroup.actionQueue[:]
		# for action in self.currentGroup.actionQueue:
		# 	self.queuedActions.append(action)

		borderh=0
		borderv=0
		btnh=0.25
		btnv=0.22

		fv=borderv
		fh=borderh
		column=0
		row=0

		for actionwindow in self.queuedActionWindows:
			actionwindow.destroy()

		self.queuedActionWindows = []

		for action, data in self.queuedActions:
			if column>3:
				column=0
				row+=1

			fh = borderh+column*(btnh)
			fv = borderv+row*(btnv)

			#print action
			queueImage = action.queueImage
			if queueImage==None:
				continue
			name = action.name
			desc = action.description

			current = len(self.queuedActionWindows)
			self.queuedActionWindows.append(self.windowManager.createWindow("TaharezLook/Button", "Root/UnitInfo/UnitQueue/"+str(current)))
			self.queuedActionWindows[current].setPosition(CEGUI.UVector2(CEGUI.UDim(fh, 0), CEGUI.UDim(fv, 0)))
			self.queuedActionWindows[current].setSize(CEGUI.UVector2(CEGUI.UDim(btnh, 0), CEGUI.UDim(btnv, 0)))
			self.queuedActionWindows[current].setProperty("NormalImage","set:actionimages image:"+queueImage)
			self.queuedActionWindows[current].setTooltipText(name+"\n\t"+desc)
			self.queuedActionWindows[current].subscribeEvent(self.queuedActionWindows[current].EventMouseButtonDown, self, "queue_Click")
			self.UnitQueue.addChildWindow(self.queuedActionWindows[current])

			shared.renderGUI.registerLayout(self.queuedActionWindows[current])

			column+=1

	def groupSelected(self, group):
		self.currentView.hide()
		self.currentView = self.UnitQueue
		self.currentView.show()
		for action, data in group.actionQueue:
			print action.queueImage

		self.currentGroup = group
		self.updateQueue()

	def noSelection(self):
		self.currentView.hide()
		self.currentView = self.NoSel
		self.currentView.show()

	def queue_Click(self, evt):
		if evt.button==CEGUI.LeftButton:
			#Show the action (If its a buildaction, show build-progress, if its a move action, pan and highlight a waypoint node, etc)
			pass
		elif evt.button==CEGUI.RightButton:
			#Cancel the action
			self.currentGroup.guiCancelAction(int(str(evt.window.getName()).split("/")[3]))
		elif evt.button==CEGUI.MiddleButton:
			#Do some magic
			pass