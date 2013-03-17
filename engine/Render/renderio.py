#Rendermodule - renderio
#Handles Input/Output devices

from time import time
from engine import shared
from ogre.renderer.OGRE import FrameListener, Degree, Vector3, Vector2
from ogre.gui.CEGUI import System, MouseCursor, LeftButton, RightButton, MiddleButton
import ogre.io.OIS as OIS
from string import split

def convertButton(oisID):
	"""Convert mousebutton ID from OIS to CEGUI"""
	if oisID == OIS.MB_Left:
		return LeftButton
	elif oisID == OIS.MB_Right:
		return RightButton
	elif oisID == OIS.MB_Middle:
		return MiddleButton
	else:
		return LeftButton

class Input(FrameListener, OIS.MouseListener, OIS.KeyListener):
	def __init__(self):
		#The three below lines are required because ogre3d is a C++ port (More I don't know)
		FrameListener.__init__(self)
		OIS.MouseListener.__init__(self)
		OIS.KeyListener.__init__(self)

		#Get the pointers to different required stuff
		self.root=shared.renderRoot
		self.scene=shared.render3dScene
		self.camera=shared.render3dCamera
		self.selectobj=shared.render3dSelectStuff

	def Setup(self):
		"""This function runs at SetupTime, and makes everything ready for Input/Output fun"""
		#Try to use shared.DPrint as much as possible when debugging stuff. More info about this is in the module Shared
		shared.DPrint("RenderIO",1,"Setting up OIS")
		#The 4 lines below tells OIS what window to capture input from
		renderWindow = self.root.getAutoCreatedWindow()
		windowHandle = renderWindow.getCustomAttributeInt("WINDOW")
		paramList = [("WINDOW", str(windowHandle))]
		self.inputManager = OIS.createPythonInputSystem(paramList)

		#These 2 lines say that you want to capture i/o from the keyboard and the mice, the last argument means that you want "ois buffered input" (Google it if you want more info)
		self.Keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, True)
		self.Mouse = self.inputManager.createInputObjectMouse(OIS.OISMouse, True)
		#These 2 lines just specifies which class instance it should call functions from (mouseMoved, mousePressed, keyPressed, etc), in this case, its this class
		self.Mouse.setEventCallback(self)
		self.Keyboard.setEventCallback(self)

		#This tries to enable a joystic controller, if its availible (I havent worked at all at this, would be nice if it worked!)
		try:
			self.Joystick = self.inputManager.createInputObjectJoyStick(OIS.OISJoyStick, False)
			shared.DPrint("RenderIO",1,"Joystick found and enabled")
		except:
			self.Joystick=False
			shared.DPrint("RenderIO",1,"Joystick not found")

		#Setup Different Varibles
		self.Settings()

	def Settings(self):
		shared.DPrint("RenderIO",1,"Defining Settings")
		self.camkeys={"forward":OIS.KC_W, "backward":OIS.KC_S, "left":OIS.KC_A, "right":OIS.KC_D, "up":OIS.KC_Q, "down":OIS.KC_E}
		self.keys=self.camkeys
		self.keys.update({"camstear":OIS.KC_LMENU, "multisel":OIS.KC_LCONTROL, "console":OIS.KC_F12})
		self.rotate = 0.13

		self.mousespeed = 1

		self.Delta=0
		self.dclicktimer=0
		self.dclickpos=0

		self.CtrlHold=False #Multiselection
		self.LMBSel=False

		#The current active interface for Keyboard (0=Render, 1=Gui, 2=Console)
		self.CurrentKeyInterface=0

		#The current active interface for mice (0=Render(CamStear), 1=Gui) !!!Replaces the self.CamStear value!!!
		self.CurrentMiceInterface=1

		##!!HACKISH SOLUTION!!##
		#Window height and length
		#Needs to be replaced with a real solution
		shared.DPrint("renderio", 0, str(self.camera.getDimensions()))
		self.hackhz, self.hackvz = self.camera.getDimensions()

	def frameRenderingQueued(self, timesincelastframe):
		"""This function has to be named this. Everything in this function gets called each frame, which means 60 times a secound, do not pollute it!"""
		#Read the current mouse and keyboard state
		self.Keyboard.capture()
		self.Mouse.capture()

		#Calculate movement with DeltaTime (Google it)
		self.Delta=timesincelastframe

		#Camera movement
		if self.CurrentKeyInterface==0:
			for x, y in self.camkeys.iteritems():
				if self.Keyboard.isKeyDown(y):
					if x=="forward":
						shared.render3dCamera.Move((0,0,-1), self.Delta)
					elif x=="backward":
						shared.render3dCamera.Move((0,0,1), self.Delta)
					elif x=="left":
						shared.render3dCamera.Move((-1,0,0), self.Delta)
					elif x=="right":
						shared.render3dCamera.Move((1,0,0), self.Delta)
					elif x=="up":
						shared.render3dCamera.Move((0,1,0), self.Delta)
					elif x=="down":
						shared.render3dCamera.Move((0,-1,0), self.Delta)

		#Multiselection
		self.CtrlHold=self.Keyboard.isKeyDown(self.keys["multisel"])

		#The application will exit if this returns false, therefor ESC closes the game.
		return not self.Keyboard.isKeyDown(OIS.KC_ESCAPE)

	def mouseMoved(self, evt):
		#Allows you to manually control the camera with the mouse if you hold the Alt key down
		if self.CurrentMiceInterface==0:
			self.camera.Rotate((evt.get_state().X.rel, evt.get_state().Y.rel))
		
		if self.CurrentMiceInterface==1:
			System.getSingleton().injectMouseMove(evt.get_state().X.rel*self.mousespeed, evt.get_state().Y.rel*self.mousespeed) #GUI Events

			#Allows you to select multiple stuff by dragging (Moving mouse while holding LMB)
			if self.LMBSel==True:
				self.selectobj.moveSelection(MouseCursor.getSingleton().getPosition())

		shared.render3dCamera.Move((0, evt.get_state().Z.rel/480, 0), 1)

		shared.DPrint("renderio", 0, evt.get_state().Z.rel)


	def mousePressed(self, evt, id):
		mousePos = MouseCursor.getSingleton().getPosition()
		if self.CurrentMiceInterface==1:
			System.getSingleton().injectMouseButtonDown(convertButton(id)) #GUI Events

			#Selectionstuff
			if id==OIS.MB_Left:
				if self.dclicktimer>time()-0.2 and self.dclickpos==mousePos.d_x:
					shared.DPrint("renderio", 0 ,"Doubleclick")
					self.dclicktimer=0
					self.dclickpos=0
				else:
					shared.DPrint("renderio", 0, "Leftmouse")
					self.dclicktimer=time()
					self.dclickpos=mousePos.d_x

					if not self.CtrlHold:
						self.selectobj.clearSelection() #Removes everything thats currently selected if you use LMB without holding down Ctrl

					#Starts selection process
					self.LMBSel=True
					self.selectobj.startSelection(MouseCursor.getSingleton().getPosition())

			if id==OIS.MB_Right:
				shared.DPrint("renderio", 0, "Rightmouse")
				self.selectobj.actionClick(mousePos.d_x / float(self.hackhz), mousePos.d_y / float(self.hackvz))

			if id==OIS.MB_Middle:
				shared.DPrint("renderio", 0, "Middlemouse")

	def mouseReleased(self, evt, id):
		if self.CurrentMiceInterface==1:
			System.getSingleton().injectMouseButtonUp(convertButton(id)) #GUI Events

			if id==OIS.MB_Left:
				MouseCursor.getSingleton().show()
				if self.LMBSel:
					self.selectobj.endSelection() #Ends selection process
					self.LMBSel=False

	def keyPressed(self, evt):
		if self.CurrentKeyInterface==1:
			#GUI Events
			ceguiSystem = System.getSingleton()
			ceguiSystem.injectKeyDown(evt.key)
			ceguiSystem.injectChar(evt.text)

		if self.CurrentKeyInterface==2:
			#Console Events
			if shared.console.visible:
				if evt.key!=self.keys["console"]:
					shared.console.keyPressed(evt)

		#Global Keys:
		if evt.key==self.keys["console"]:
			if shared.console.visible:
				shared.console.hide()
				self.CurrentKeyInterface=0
			else:
				shared.console.show()
				self.CurrentKeyInterface=2

		if evt.key==self.keys["camstear"]:
			self.CurrentMiceInterface=0
			MouseCursor.getSingleton().hide()


	def keyReleased(self, evt):
		#GUI Events
		if self.CurrentKeyInterface==1:
			System.getSingleton().injectKeyUp(evt.key)

		if evt.key==self.keys["camstear"]:
			self.CurrentMiceInterface=1
			MouseCursor.getSingleton().show() #Show mousecursor