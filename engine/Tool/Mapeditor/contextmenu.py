#ContextMenu
#The contextmenu is an modular and eventdriven menu which appear near the mousecursor.
#The menu that appear differs with the object clicked or the button used to 'click' it
#All the menumodules lies in ./context/

import ogre.renderer.OGRE as ogre
import ogre.gui.CEGUI as CEGUI

from engine.Tool.Mapeditor.context import dec, ground, tools, unit
from engine import debug, shared
from engine.Render.render3dcamera import MASK_CAMERA
from engine.Render.render3dwater import MASK_WATER
from engine.Render.render3dent import MASK_UNIT, MASK_DECO, MASK_OTHER, MASK_GADGET
from engine.Render.render3dterrain import MASK_TERRAIN

class Menu():
	def __init__(self):
		self.windowManager = CEGUI.WindowManager.getSingleton()
		self.root = self.windowManager.getWindow("Root")
		self.raySceneQuery = shared.render3dScene.sceneManager.createRayQuery(ogre.Ray())

		self.contexts=[tools.contextTools(), dec.contextDec(), ground.contextGround(), unit.context()]
		self.options=["Hide gui", "Close"]
		self.optfunc=[self.sHideGui, self.sClose]
		self.listboxitems=[]
		self.CurrentContext=1

		self.listbox=None

		#Making myself a memoryleak:
		self.listboxcount=0 #This is really ridiculous, but actually nessesary due to a CEGUI Crash


		#self.createListbox()
		#self.updateOptions()

	def createListbox(self):
		if self.listbox!=None:
			self.listbox.hide()
		self.listbox=None
		self.listbox=self.windowManager.createWindow("Vanilla/Listbox", "ContextMenu"+str(self.listboxcount))
		self.listbox.setText("Selection Options")
		self.listbox.setSize(CEGUI.UVector2(CEGUI.UDim(0.15, 0), CEGUI.UDim(0.2, 0)))
		self.root.addChildWindow(self.listbox)

		#Nessessary unnessesary copy from globalgui.py
		self.listbox.setAlpha(0.5)
		self.listbox.subscribeEvent(self.listbox.EventMouseEnters, shared.globalGUI, "W_Menter")
		self.listbox.subscribeEvent(self.listbox.EventMouseLeaves, shared.globalGUI, "W_Mleave")
		self.listbox.subscribeEvent(self.listbox.EventMouseButtonDown, shared.globalGUI, "W_Mclick")
		self.listbox.subscribeEvent(self.listbox.EventMouseButtonUp, shared.globalGUI, "W_Mrelease")
		self.listbox.subscribeEvent(self.listbox.EventMouseMove, shared.globalGUI, "MouseMoving")
		for y in shared.globalGUI.iterChilds(self.listbox.getName()):
			y.subscribeEvent(y.EventMouseEnters, shared.globalGUI, "W_Menter")
			y.subscribeEvent(y.EventMouseLeaves, shared.globalGUI, "W_Mleave")
			for z in shared.globalGUI.iterChilds(y.getName()):
				z.subscribeEvent(z.EventMouseEnters, shared.globalGUI, "W_Menter")
				z.subscribeEvent(z.EventMouseLeaves, shared.globalGUI, "W_Mleave")


		self.listbox.subscribeEvent(self.listbox.EventSelectionChanged, self, "menuClick")
		self.listboxcount+=1

	def updateOptions(self):
		#self.listbox.resetList()
		#self.listboxitems=[] #This will be an memory leak, but CEGUI crashes if the pointer to an listbox item gets destroyed

		# for x in self.listboxitems:
		# 	self.listbox.removeItem(x)
		# 	#print("Item removed.")
		self.createListbox()

		if self.CurrentContext!=None:
			for x in self.contexts[self.CurrentContext].options:
				self.listboxitems.append(CEGUI.ListboxTextItem(x))
				self.listbox.addItem(self.listboxitems[len(self.listboxitems)-1])

		for x in self.options:
			self.listboxitems.append(CEGUI.ListboxTextItem(x))
			self.listbox.addItem(self.listboxitems[len(self.listboxitems)-1])


	def rightClick(self):
		#print("!!! - rightClick")
		if shared.toolManager.CurrentTool!=0:
			shared.render3dSelectStuff.clearSelection()
			shared.render3dSelectStuff.startSelection(CEGUI.MouseCursor.getSingleton().getPosition())
			shared.render3dSelectStuff.endSelection()
			#print("!!! - Selection")

		self.contextCheck()
		#print("!!! - ContentCheck")
		self.updateOptions()
		#print("!!! - updateOptions")
		mousePos = CEGUI.MouseCursor.getSingleton().getPosition()
		self.rightclickpos=mousePos
		self.listbox.setPosition(CEGUI.UVector2(CEGUI.UDim(0, mousePos.d_x), CEGUI.UDim(0, mousePos.d_y)))
		self.listbox.show()
		#print("!!! - show")

	def middleClick(self):
		self.active=True
		self.CurrentContext=0
		self.updateOptions()
		mousePos = CEGUI.MouseCursor.getSingleton().getPosition()
		self.listbox.setPosition(CEGUI.UVector2(CEGUI.UDim(0, mousePos.d_x), CEGUI.UDim(0, mousePos.d_y)))
		self.listbox.show()

	def hide(self):
		self.active=False
		#print("!!! - HIDE")
		if shared.toolManager.CurrentTool!=0:
			shared.render3dSelectStuff.clearSelection()
		self.listbox.hide()

	def menuClick(self, evt):
		shared.globalGUI.resetMiceInterface()
		if self.listbox.getFirstSelectedItem()!=None:
			selected=self.listbox.getFirstSelectedItem().getText()
			if selected in self.options:
				self.optfunc[self.options.index(selected)]()
			elif self.CurrentContext!=None:
				self.contexts[self.CurrentContext].optfunc[self.contexts[self.CurrentContext].options.index(selected)]()
			else:
				shared.DPrint("contextmenu", 4, "Item "+str(selected)+" is not in context or default list!")
		self.hide() #This has to be here!

	def sHideGui(self):
		pass

	def sClose(self):
		self.hide()

	def contextCheck(self):
		self.dimh, self.dimv = shared.render3dCamera.getDimensions()
		self.CurrentContext=None
		#print("Raybeens")
		mousePos = CEGUI.MouseCursor.getSingleton().getPosition()
		mouseRay = shared.render3dCamera.camera.getCameraToViewportRay(mousePos.d_x / float(self.dimh),
													  mousePos.d_y / float(self.dimv))
		self.raySceneQuery.setRay(mouseRay)
		self.raySceneQuery.setSortByDistance(True)
		self.raySceneQuery.setQueryMask(MASK_WATER | MASK_TERRAIN | MASK_DECO | MASK_OTHER | MASK_UNIT)
		result = self.raySceneQuery.execute()
		found = False
		if len(result)>0:
			for item in result:
				print "____________________________________"
				print item.movable.getName()
				print item.movable.getMovableType()

				if "dec" in item.movable.getName():
					self.CurrentContext=1
					found = True
					print("Decorator")
					break

				elif item.movable.getName()[0:5] == "Water":
					self.CurrentContext=2
					found = True
					break

				elif "unit" in item.movable.getName():
					self.CurrentContext=3
					found = True
					print("Decorator")
					break

				else:
					self.CurrentContext=None

		if len(result)>0 and found == False:
			for item in result:
				if str(item.movable.getMovableType())=="OgreTerrainNodeMovable" or "Unnamed" in str(item.movable.getMovableType):
					self.CurrentContext=2
					print("Terrain")
					break