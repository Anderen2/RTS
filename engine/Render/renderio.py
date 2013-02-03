#Rendermodule - renderio
#Handles Input/Output devices

from engine import shared
from ogre.renderer.OGRE import FrameListener, Degree, Vector3, Vector2
from ogre.gui.CEGUI import System, MouseCursor, LeftButton, RightButton, MiddleButton
import ogre.io.OIS as OIS
from string import split

def convertButton(oisID):
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
		self.UnitHandeler=shared.unitHandeler

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
		self.rotate = 0.13
		self.move = 250

		self.mousespeed = 1

		self.CamStear=False
		self.Delta=0

		self.WHold=False
		self.AHold=False
		self.SHold=False
		self.DHold=False
		self.QHold=False
		self.EHold=False
		self.CtrlHold=False
		self.LMBSel=False

		#The current active interface for Keyboard (0=Render, 1=Gui, 2=Console)
		self.CurrentKeyInterface=0

		#The current active interface for mice (0=Render(CamStear), 1=Gui) !!!Replaces the self.CamStear value!!!
		self.CurrentMiceInterface=1

		##!!HACKISH SOLUTION!!##
		#Window height and length
		#Needs to be replaced with a real solution
		self.hackhz=1024
		self.hackvz=768

	def frameRenderingQueued(self, timesincelastframe):
		"""This function has to be named this. Everything in this function gets called each frame, which means 60 times a secound, do not pollute it!"""
		#Read the current mouse and keyboard state
		self.Keyboard.capture()
		self.Mouse.capture()

		#Calculate movement with DeltaTime (Google it)
		self.Delta=timesincelastframe

		#Movement
		transVector = Vector3(0, 0, 0)

		if self.WHold:
			transVector.z -= self.move
		if self.SHold:
			transVector.z += self.move
		if self.AHold:
			transVector.x -= self.move
		if self.DHold:
			transVector.x += self.move
		if self.QHold:
			transVector.y += self.move
		if self.EHold:
			transVector.y -= self.move

		#See render3d's Camera Class for more infomation about this
		self.camera.SetPos(self.camera.camNode.orientation * transVector * (self.Delta))

		#The application will exit if this returns false, therefor ESC closes the game.
		return not self.Keyboard.isKeyDown(OIS.KC_ESCAPE)

	def mouseMoved(self, evt):
		#Allows you to manually control the camera with the mouse if you hold the Alt key down
		if self.CurrentMiceInterface==0:
			self.camera.camNode.yaw(Degree(-self.rotate * evt.get_state().X.rel).valueRadians())
			self.camera.camNode.getChild(0).pitch(Degree(-self.rotate * evt.get_state().Y.rel).valueRadians())
		
		if self.CurrentMiceInterface==1:
			#GUI Events
			System.getSingleton().injectMouseMove(evt.get_state().X.rel, evt.get_state().Y.rel)

			#Allows you to select multiple stuff by dragging (Moving mouse while holding LMB)
			if self.LMBSel==True:
				mousePos = MouseCursor.getSingleton().getPosition()
				self.selectobj.mStart.x = mousePos.d_x / float(self.hackhz)
				self.selectobj.mStart.y = mousePos.d_y / float(self.hackvz)
				self.selectobj.mRect.setCorners(self.selectobj.mStart, self.selectobj.mStop)

	def mousePressed(self, evt, id):
		if self.CurrentMiceInterface==1:
			#GUI Events
			System.getSingleton().injectMouseButtonDown(convertButton(id))

			#Selectionstuff
			if id==OIS.MB_Left:
				if not self.CtrlHold:
					#Removes everything thats currently selected if you use LMB without holding down Ctrl
					shared.DPrint(4,0,"Cleared all selections")
					for x in self.selectobj.CurrentSelection:
						unitID=int(split(x.getName(),"_")[1])
						shared.unitHandeler.Get(unitID)._deselected()
					self.selectobj.CurrentSelection=[]

				#Starts selection process
				self.LMBSel=True
				mousePos = MouseCursor.getSingleton().getPosition()
				self.selectobj.mStart.x = mousePos.d_x / float(self.hackhz)
				self.selectobj.mStart.y = mousePos.d_y / float(self.hackvz)
				self.selectobj.mStop = Vector2(self.selectobj.mStart.x+0.00001, self.selectobj.mStart.y+0.00001)
				self.selectobj.mSelecting = True
				self.selectobj.mRect.clear()
				self.selectobj.mRect.setVisible(True)
				self.selectobj.mRect.setCorners(self.selectobj.mStart, self.selectobj.mStop)

			if id==OIS.MB_Right:
				mousePos = MouseCursor.getSingleton().getPosition()
				self.selectobj.actionClick(mousePos.d_x / float(self.hackhz), mousePos.d_y / float(self.hackvz))

	def mouseReleased(self, evt, id):
		if self.CurrentMiceInterface==1:
			#GUI Events
			System.getSingleton().injectMouseButtonUp(convertButton(id))

			if id==OIS.MB_Left:
				#Ends selection process
				MouseCursor.getSingleton().show()
				if self.LMBSel:
					self.selectobj.performSelection(self.selectobj.mStart, self.selectobj.mStop)
					self.selectobj.mSelecting = False
					self.selectobj.mRect.setVisible(False)
					self.selectobj.LMBSel=False

	def keyPressed(self, evt):
		if self.CurrentKeyInterface==0:
			#Camera movement
			if evt.key==OIS.KC_W:
				self.WHold=True
			if evt.key==OIS.KC_S:
				self.SHold=True
			if evt.key==OIS.KC_A:
				self.AHold=True
			if evt.key==OIS.KC_D:
				self.DHold=True
			if evt.key==OIS.KC_Q:
				self.QHold=True
			if evt.key==OIS.KC_E:
				self.EHold=True
				
		if self.CurrentKeyInterface==1:
			#GUI Events
			ceguiSystem = System.getSingleton()
			ceguiSystem.injectKeyDown(evt.key)
			ceguiSystem.injectChar(evt.text)

		if self.CurrentKeyInterface==2:
			if shared.console.visible:
				if evt.key!=OIS.KC_GRAVE:
					shared.console.keyPressed(evt)

		#Global Keys:
		if evt.key==OIS.KC_F12: #Changed from GRAVE ( | ) due to linux compatibility
			if shared.console.visible:
				shared.console.hide()
				self.CurrentKeyInterface=0
			else:
				shared.console.show()
				self.CurrentKeyInterface=2

		if evt.key==OIS.KC_LMENU:
			self.CurrentMiceInterface=0
			MouseCursor.getSingleton().hide()

		#Global Render Keys
		if evt.key==OIS.KC_LCONTROL:
			self.CtrlHold=True

	def keyReleased(self, evt):
		#GUI Events
		if self.CurrentKeyInterface==1:
			System.getSingleton().injectKeyUp(evt.key)

		#Camera movement
		if self.CurrentKeyInterface==0:
			if evt.key==OIS.KC_W:
				self.WHold=False
			if evt.key==OIS.KC_S:
				self.SHold=False
			if evt.key==OIS.KC_A:
				self.AHold=False
			if evt.key==OIS.KC_D:
				self.DHold=False
			if evt.key==OIS.KC_Q:
				self.QHold=False
			if evt.key==OIS.KC_E:
				self.EHold=False

		#Global Render Keys
		if evt.key==OIS.KC_LCONTROL:
			self.CtrlHold=False

		if evt.key==OIS.KC_LMENU:
			self.CurrentMiceInterface=1
			#Show mousecursor
			MouseCursor.getSingleton().show()