import ogre.gui.CEGUI as CEGUI
from string import split

from engine import shared, debug
from engine.Render.gui import chat, debugGUI, gameinfo, minimap, moneybar, options, powerbar, tactical, unitinfo, unitopt

class GUI():
	def __init__(self):
		shared.DPrint("RenderGUI",1,"Setting up CEGUI")

		self.MoveInterface=None
		shared.gui={}

		# CEGUI setup
		if CEGUI.Version__.startswith("0.6"):
			self.renderer = CEGUI.OgreCEGUIRenderer(renderWindow, ogre.RENDER_QUEUE_OVERLAY, False, 3000, self.sceneManager)
			self.system = CEGUI.System(self.renderer)
			CEGUI.SchemeManager.getSingleton().loadScheme("TaharezLookSkin.scheme")
			CEGUI.SchemeManager.getSingleton().loadScheme("VanillaSkin.scheme")
			CEGUI.SchemeManager.getSingleton().loadScheme("WindowsLook.scheme")
		else:
			self.renderer = CEGUI.OgreRenderer.bootstrapSystem()
			self.system = CEGUI.System.getSingleton()
			CEGUI.SchemeManager.getSingleton().create("TaharezLookSkin.scheme")
			CEGUI.SchemeManager.getSingleton().create("VanillaSkin.scheme")
			CEGUI.SchemeManager.getSingleton().create("WindowsLook.scheme")

		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

	def Setup(self):
		shared.DPrint("RenderGUI",1,"Setting up layout")

		#Setup varibles
		self.globalpha=0.9
		self.upperalpha=0.5
		self.hackhz, self.hackvz = shared.render3dCamera.getDimensions()
		self.IgnoreMe=["Root/UnitOpt/BG/Actions","Root/UnitOpt/BG/Upgrades"]
		self.IgnoreMyParent=["Root/Chat/BG", "Root/Chat", "Root/GameInfo/BG", "Root/GameInfo"]

		#Loading Layouts
		self.sheet = CEGUI.WindowManager.getSingleton().loadWindowLayout("RTS.layout")
		self.system.setGUISheet(self.sheet)

		#Setup Defaults
		self.system.setDefaultMouseCursor("TaharezLook", "MouseArrow")
		self.system.setDefaultFont("BlueHighway-12")
		CEGUI.MouseCursor.getSingleton().setImage("TaharezLook", "MouseArrow")

		self.root = self.windowManager.getWindow("Root")

		#Create the rest of the gui elements
		self.CreateGuiElements()

	def iterChilds(self, window):
		element=self.windowManager.getWindow(window)
		childcount=element.getChildCount()
		if childcount!=0:
			for x in xrange(0, childcount):
				yield element.getChildAtIdx(x)
		else:
			pass


	def CreateGuiElements(self):
		self.root.subscribeEvent(self.root.EventMouseMove, self, "MouseMoving")
		shared.DPrint("RenderGUI",1,"Creating GUI elements")

		shared.gui['chat']=chat.Chat()
		shared.gui['debug']=debugGUI.Debug()
		shared.gui['gameinfo']=gameinfo.GameInfo()
		shared.gui['minimap']=minimap.Minimap()
		shared.gui['moneybar']=moneybar.Moneybar()
		shared.gui['options']=options.Options()
		shared.gui['powerbar']=powerbar.Powerbar()
		shared.gui['tactical']=tactical.Tactical()
		shared.gui['unitinfo']=unitinfo.UnitInfo()
		shared.gui['unitopt']=unitopt.UnitOpt()

	def createDebugOnly(self):
		# self.root = self.windowManager.getWindow("Root")
		# self.root.subscribeEvent(self.root.EventMouseMove, self, "MouseMoving")
		shared.DPrint("RenderGUI",1,"Creating Debug Only")
		shared.gui['debug']=debugGUI.Debug()
		
	def registerLayout(self, layout):
		shared.DPrint("globalgui", 0, "Registering new guielement..")
		layout.subscribeEvent(layout.EventMouseEnters, self, "W_Menter")
		layout.subscribeEvent(layout.EventMouseLeaves, self, "W_Mleave")
		layout.subscribeEvent(layout.EventMouseButtonDown, self, "W_Mclick")
		layout.subscribeEvent(layout.EventMouseButtonUp, self, "W_Mrelease")
		layout.subscribeEvent(layout.EventMouseMove, self, "MouseMoving")
		try:
			foobar=self.windowManager.getWindow(layout.getName()+"/BG")
			foobar.setProperty("Image","set:guibgset image:guibgs")
		except:
			print(layout.getName()+" has no background!")

		for y in self.iterChilds(layout.getName()):
			y.subscribeEvent(y.EventMouseEnters, self, "W_Menter")
			y.subscribeEvent(y.EventMouseLeaves, self, "W_Mleave")
			y.subscribeEvent(y.EventMouseButtonDown, self, "W_Mclick")
			y.subscribeEvent(y.EventMouseButtonUp, self, "W_Mrelease")
			y.subscribeEvent(y.EventMouseMove, self, "MouseMoving")
			for z in self.iterChilds(y.getName()):
				z.subscribeEvent(z.EventMouseEnters, self, "W_Menter")
				z.subscribeEvent(z.EventMouseLeaves, self, "W_Mleave")
				z.subscribeEvent(z.EventMouseButtonDown, self, "W_Mclick")
				z.subscribeEvent(z.EventMouseButtonUp, self, "W_Mrelease")
				z.subscribeEvent(z.EventMouseMove, self, "MouseMoving")
				for l in self.iterChilds(z.getName()):
					l.subscribeEvent(l.EventMouseEnters, self, "W_Menter")
					l.subscribeEvent(l.EventMouseLeaves, self, "W_Mleave")
					l.subscribeEvent(l.EventMouseButtonDown, self, "W_Mclick")
					l.subscribeEvent(l.EventMouseButtonUp, self, "W_Mrelease")
					l.subscribeEvent(l.EventMouseMove, self, "MouseMoving")

	def MouseMoving(self, evt):
		UDim=CEGUI.UDim
		if self.MoveInterface!=None:
			mousePos = CEGUI.MouseCursor.getSingleton().getPosition()
			self.MoveInterfaceMCVec=(mousePos.d_x, mousePos.d_y)
			self.MoveInterfaceMRVec=(mousePos.d_x/self.hackhz, mousePos.d_y/self.hackvz)
			self.MoveInterfacePRVec=(evt.window.getXPosition(),evt.window.getYPosition())
			self.MoveInterfaceSZVec=(evt.window.getWidth(),evt.window.getHeight())
			self.MoveInterfaceLoVec=(self.MoveInterfaceMRVec[0]-UDim(self.MoveInterfaceSZVec[0]).d_scale,self.MoveInterfaceMRVec[1]-UDim(self.MoveInterfaceSZVec[1]).d_scale)
			self.MoveInterface.setPosition( CEGUI.UVector2( CEGUI.UDim(0,mousePos.d_x), CEGUI.UDim(0,mousePos.d_y) ))

	def W_Mclick(self, evt):
		UDim=CEGUI.UDim
		if evt.button==CEGUI.MiddleButton:
			CEGUI.System.getSingleton().setDefaultMouseCursor("TaharezLook", "MouseMoveCursor")
			shared.DPrint("RenderGUI",0,"Clicked: "+str(evt.window.getName()))

			winname=str(evt.window.getName())

			if "/" in winname:
				foo=split(winname, "/")
				self.MoveInterface = self.windowManager.getWindow("Root/"+foo[1])
			else:
				self.MoveInterface = evt.window

			mousePos = CEGUI.MouseCursor.getSingleton().getPosition()
			self.MoveInterfaceMCVec=(mousePos.d_x, mousePos.d_y)
			self.MoveInterfaceMRVec=(mousePos.d_x/self.hackhz, mousePos.d_y/self.hackvz)
			self.MoveInterfacePRVec=(evt.window.getXPosition(),evt.window.getYPosition())
			self.MoveInterfaceSZVec=(evt.window.getWidth(),evt.window.getHeight())
			self.MoveInterfaceLoVec=(self.MoveInterfaceMRVec[0]-UDim(self.MoveInterfaceSZVec[0]).d_scale,self.MoveInterfaceMRVec[1]-UDim(self.MoveInterfaceSZVec[1]).d_scale)
			if self.MoveInterface!=None:
				self.MoveInterface.setAlpha(0.20)

	def W_Mrelease(self,evt):
		if evt.button==CEGUI.MiddleButton:
			if self.MoveInterface!=None:
				self.MoveInterface.setAlpha(self.globalpha)
			CEGUI.System.getSingleton().setDefaultMouseCursor("TaharezLook", "MouseArrow")
			self.MoveInterface=None

	def W_Menter(self, evt):
		self.OldInterface=shared.renderioInput.CurrentMiceInterface
		shared.renderioInput.CurrentMiceInterface=1
		
		shared.DPrint("RenderGUI",0,"Entered: "+str(evt.window.getName()))
		if not evt.window.getName() in self.IgnoreMe:
			if not evt.window.getParent().getName() in self.IgnoreMyParent:
				evt.window.setAlpha(0.50)
		self.ActiveWindow=evt.window
 
 	def W_Mleave(self, evt):
 		if shared.renderioInput.CurrentMiceInterface==1:
 			if self.OldInterface!=1:
 				shared.renderioInput.CurrentMiceInterface=self.OldInterface
 			else:
 				shared.renderioInput.CurrentMiceInterface=2
 		if not evt.window.getName() in self.IgnoreMe:
			if not evt.window.getParent().getName() in self.IgnoreMyParent:
 				evt.window.setAlpha(1)
 		self.ActiveWindow=None

 	def HideAll(self):
		self.root.hide()

	def ShowAll(self):
		self.root.show()

	debug.ACC("gui_hideall", HideAll, info="Hide all the gui elements", args=0)
	debug.ACC("gui_showall", ShowAll, info="Show all the gui elements", args=0)