#Rendermodule - renderio
#Handles Input/Output devices

from time import time
from engine import shared, debug
from engine.Lib.hook import Hook
from ogre.renderer.OGRE import FrameListener, Degree, Vector3, Vector2
from ogre.gui.CEGUI import System, MouseCursor, LeftButton, RightButton, MiddleButton
import ogre.io.OIS as OIS
from string import split
from platform import architecture

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
		self.oldinf=0

		self.Hook = Hook(self)
		self.Hook.new("OnMousePressed", 2) #Key, Pos
		self.Hook.new("OnMouseReleased", 2) #Key, Pos
		self.Hook.new("OnMouseMove", 1) #Pos
		self.Hook.new("OnKeyPressed", 1) #Key
		self.Hook.new("OnKeyReleased", 1) #Key
		self.Hook.new("OnMouseStateChanged", 1) #State
		self.Hook.new("OnKeyStateChanged", 1) #State

		#Keys registred for outside functions
		self.regkeys = {}

	def SetupBare(self):
		shared.DPrint("RenderIO",1,"Setting up OIS")
		renderWindow = shared.renderRoot.getAutoCreatedWindow()

		if architecture()[0]=="64bit":
			windowHandle = renderWindow.getCustomAttributeUnsignedLong("WINDOW")
		else:
			windowHandle = renderWindow.getCustomAttributeInt("WINDOW")

		paramList = [("WINDOW", str(windowHandle))]
		self.inputManager = OIS.createPythonInputSystem(paramList)

		#Setup renderlistener
		shared.render.renderqueue.append(shared.renderioInput)

		#These 2 lines say that you want to capture i/o from the keyboard and the mice, the last argument means that you want "ois buffered input" (Google it if you want more info)
		self.Keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, True)
		self.Mouse = self.inputManager.createInputObjectMouse(OIS.OISMouse, True)
		#These 2 lines just specifies which class instance it should call functions from (mouseMoved, mousePressed, keyPressed, etc), in this case, its this class
		self.Mouse.setEventCallback(self)
		self.Keyboard.setEventCallback(self)

		self.Settings()

	def Setup(self):
		"""This function runs at SetupTime, and makes everything ready for Input/Output fun"""
		#Try to use shared.DPrint as much as possible when debugging stuff. More info about this is in the module Shared
		shared.DPrint("RenderIO",1,"Setting up OIS")
		#The 4 lines below tells OIS what window to capture input from
		renderWindow = shared.renderRoot.getAutoCreatedWindow()

		if architecture()[0]=="64bit":
			windowHandle = renderWindow.getCustomAttributeUnsignedLong("WINDOW")
		else:
			windowHandle = renderWindow.getCustomAttributeInt("WINDOW")
			
		paramList = [("WINDOW", str(windowHandle))]
		self.inputManager = OIS.createPythonInputSystem(paramList)

		#Setup renderlistener
		shared.render.renderqueue.append(shared.renderioInput)


		#These 2 lines say that you want to capture i/o from the keyboard and the mice, the last argument means that you want "ois buffered input" (Google it if you want more info)
		self.Keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, True)
		self.Mouse = self.inputManager.createInputObjectMouse(OIS.OISMouse, True)

		#Fix slow mousemovement for positive direction
		windowHeight = renderWindow.getHeight()
		windowWidth = renderWindow.getWidth()
		#self.inputManager.setWindowExtents(windowWidth, windowHeight)
		mState = self.Mouse.getMouseState()
		mState.width = windowWidth
		mState.height = windowHeight

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
		self.keys.update({"camstear":OIS.KC_LMENU, "multisel":OIS.KC_LSHIFT, "queueaction":OIS.KC_LCONTROL, "console":OIS.KC_F12})
		self.rotate = 0.13

		self.mousespeed = 1

		self.Delta=0
		self.dclicktimer=0
		self.dclickpos=0

		self.MultiSelection=False #Multiselection
		self.LMBSel=False

		#The current active interface for Keyboard (0=Render, 1=Gui, 2=Console)
		self.CurrentKeyInterface=0

		#The current active interface for mice (0=Render(CamStear), 1=Gui, 2=Selections, 3=MapMaker Tools)
		self.CurrentMiceInterface=2

		#The current window in focus
		self.CurrentFocus=None

		##!!HACKISH SOLUTION!!##
		#Window height and length
		#Needs to be replaced with a real solution
		shared.DPrint("renderio", 0, str(shared.render3dCamera.getDimensions()))
		self.hackhz, self.hackvz = shared.render3dCamera.getDimensions()

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
		self.MultiSelection=self.Keyboard.isKeyDown(self.keys["multisel"])

		#The application will exit if this returns false, therefor Shift-ESC closes the game.
		return not (self.Keyboard.isKeyDown(OIS.KC_ESCAPE) and self.Keyboard.isKeyDown(OIS.KC_LSHIFT))

	def mouseMoved(self, evt):
		self.Hook.call("OnMouseMove", (evt.get_state().X, evt.get_state().Y))

		if self.CurrentMiceInterface!=self.oldinf:
			#print self.CurrentMiceInterface
			self.oldinf=self.CurrentMiceInterface
		
		#Allows you to manually control the camera with the mouse if you hold the Alt key down
		if self.CurrentMiceInterface==0:
			shared.render3dCamera.Rotate((evt.get_state().X.rel, evt.get_state().Y.rel))
		
		if self.CurrentMiceInterface>0:
			System.getSingleton().injectMouseMove(evt.get_state().X.rel*self.mousespeed, evt.get_state().Y.rel*self.mousespeed) #GUI Events

			#Allows you to select multiple stuff by dragging (Moving mouse while holding LMB)
			if self.LMBSel==True:
				shared.render3dSelectStuff.moveSelection(MouseCursor.getSingleton().getPosition())

		#Scrollwheel zoom
		#shared.render3dCamera.Move((0, evt.get_state().Z.rel/480, 0), 1)

		if self.CurrentMiceInterface==3:
			#MapBuilder Tool Hooks
			shared.mapBackend.MouseMoved(evt.get_state().X, evt.get_state().Y)

	def mousePressed(self, evt, id):
		mousePos = MouseCursor.getSingleton().getPosition()
		self.Hook.call("OnMousePressed", id, mousePos)

		if self.CurrentMiceInterface==1:
			#This toggles automaticly in rendergui when you hover over a gui element
			System.getSingleton().injectMouseButtonDown(convertButton(id)) #GUI Events

		if self.CurrentMiceInterface==2:
			

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

					if not self.MultiSelection:
						shared.render3dSelectStuff.clearSelection() #Removes everything thats currently selected if you use LMB without holding down Ctrl

					#Starts selection process
					self.LMBSel=True
					shared.render3dSelectStuff.startSelection(MouseCursor.getSingleton().getPosition())

			if id==OIS.MB_Right:
				shared.DPrint("renderio", 0, "Rightmouse")
				shared.render3dSelectStuff.actionClick(mousePos.d_x / float(self.hackhz), mousePos.d_y / float(self.hackvz))

			if id==OIS.MB_Middle:
				shared.DPrint("renderio", 0, "Middlemouse")

				#Hackish solution, but working
				try:
					shared.mapBackend.MousePressed(id)
				except:
					pass

		if self.CurrentMiceInterface==3:
			#MapBuilder Tool Hooks
			shared.mapBackend.MousePressed(id)

	def mouseReleased(self, evt, id):
		mousePos = MouseCursor.getSingleton().getPosition()
		self.Hook.call("OnMouseReleased", id, mousePos)
		if self.CurrentMiceInterface==1:
			System.getSingleton().injectMouseButtonUp(convertButton(id)) #GUI Events

		if self.CurrentMiceInterface==2:
			if id==OIS.MB_Left:
				MouseCursor.getSingleton().show()
				if self.LMBSel:
					shared.render3dSelectStuff.endSelection() #Ends selection process
					self.LMBSel=False

		if self.CurrentMiceInterface==3:
			#MapBuilder Tool Hooks
			shared.mapBackend.MouseReleased(id)

	def registerKeyEvent(self, key, pressfunc, releasefunc, force=False):
		if not key in self.regkeys:
			shared.DPrint("renderio", 0, "Key: "+str(key)+" registred to functions: "+str((pressfunc, releasefunc)))
			self.regkeys[key]=(pressfunc, releasefunc)
		else:
			if force:
				shared.DPrint("renderio", 1, "Key: "+str(key)+" forcibly registred to functions: "+str((pressfunc, releasefunc)))
				self.regkeys[key]=(pressfunc, releasefunc)
			else:
				shared.DPrint("renderio", 2, "Key: "+str(key)+" tried to be bound to: "+str((pressfunc, releasefunc))+" but the key is already bound to: "+str(self.regkeys[key])+" !")

	def removeKeyEvent(self, key):
		if key in self.regkeys:
			del self.regkeys[key]
		else:
			shared.DPrint("renderio", 2, "Tried to remove unbounded key: "+str(key)+" !")


	def keyPressed(self, evt):
		self.Hook.call("OnKeyPressed", evt.key)
		if self.CurrentKeyInterface==1:
			#GUI Events
			ceguiSystem = System.getSingleton()
			ceguiSystem.injectKeyDown(evt.key)
			ceguiSystem.injectChar(evt.text)

		elif self.CurrentKeyInterface==2:
			#Console Events
			if shared.console.visible:
				if evt.key!=self.keys["console"]:
					shared.console.keyPressed(evt)

		else:
			#Registered keys
			if evt.key in self.regkeys:
				if self.regkeys[evt.key][0]!=None:
					self.regkeys[evt.key][0]() #Call the pressedfunction for the key

		#Global Keys:
		if evt.key==self.keys["console"]:
			if shared.console.visible:
				shared.console.hide()
				self.CurrentKeyInterface=0
			else:
				shared.console.show()
				self.CurrentKeyInterface=2

		if evt.key==self.keys["camstear"]:
			self.OldMiceInterface=self.CurrentMiceInterface
			self.CurrentMiceInterface=0
			MouseCursor.getSingleton().hide()

		#Grouprelated
		#if self.Keyboard.isKeyDown(self.keys["queueaction"]):
		if evt.key==self.keys["queueaction"]:
			print("IO: AQ TRUE")
			shared.DirectorManager.actionQueueing=True


	def keyReleased(self, evt):
		self.Hook.call("OnKeyReleased", evt.key)
		#GUI Events
		if self.CurrentKeyInterface==1:
			System.getSingleton().injectKeyUp(evt.key)

		else:
			#Registered keys
			if evt.key in self.regkeys:
				if self.regkeys[evt.key][1]!=None:
					self.regkeys[evt.key][1]() #Call the releasedfunction for the key

		if evt.key==self.keys["camstear"]:
			self.CurrentMiceInterface=self.OldMiceInterface
			if self.CurrentMiceInterface==0:
				self.CurrentMiceInterface=2
			MouseCursor.getSingleton().show() #Show mousecursor

		if evt.key==self.keys["queueaction"]:
			print("IO: AQ FALSE")
			shared.DirectorManager.actionQueueing=False

		if evt.key==OIS.KC_ESCAPE:
			try:
				shared.globalGUI.CancelCurrent()
			except:
				pass

	def takeKeyFocus(self, mod):
		if self.CurrentKeyInterface!=2:
			self.CurrentKeyInterface=1
			self.CurrentFocus=mod

	def looseKeyFocus(self, mod):
		if self.CurrentFocus==mod:
			self.CurrentKeyInterface=0
			self.CurrentFocus=None
		else:
			shared.DPrint("renderio", 2, "Module: "+str(mod)+" tried to loose other modules focus")