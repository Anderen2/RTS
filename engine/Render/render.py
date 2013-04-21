#MainModule - Render
#Submodules: render3d, rendergui, renderio, renderphys
import render3d, rendergui, renderio, renderphys, renderconsole
from twisted.internet import reactor
from engine import shared
from time import gmtime, sleep, time
from traceback import print_exc
import ogre.renderer.OGRE as ogre

shared.DPrint(1,1,"Imported..")

QUITTIMER=360 #Set this to a time in secounds if you want the game to automaticly quit. 0 or None disables it.

class RenderApplication(object):
	#This class setups and starts all rendermodules
	def __init__(self):
		shared.DPrint("Render",1,"Initializing")

	def PowerUp(self):
		self.createRoot()
		self.defineResources()
		self.setupRenderSystem()
		self.createRenderWindow()
		self.initializeResourceGroups()
		self.setupScene()
		self.setupInputSystem()
		self.setupCEGUI()
		self.setupDebuggingTools()
		self.createFrameListener()
		self.startRenderLoop()
		#self.cleanUp()

	def createRoot(self):
		shared.DPrint("Render",1,"Creating Root")
		self.root = ogre.Root()
		shared.renderRoot=self.root
 
	def defineResources(self):
		shared.DPrint("Render",1,"Defining Resources")
		cf = ogre.ConfigFile()
		cf.load("resources.cfg")

		seci = cf.getSectionIterator()
		while seci.hasMoreElements():
			secName = seci.peekNextKey()
			settings = seci.getNext()
			for item in settings:
				typeName = item.key
				archName = item.value
				ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName)

	def setupRenderSystem(self):
		shared.DPrint("Render",1,"Setting up RenderSystem")
		if not self.root.restoreConfig() and not self.root.showConfigDialog():
			raise Exception("User canceled the config dialog! -> Application.setupRenderSystem()")
 
	def createRenderWindow(self):
		shared.DPrint("Render",1,"Creating renderwindow")
		self.root.initialise(True, "YARTS: v. alpha-alpha")
 
	def initializeResourceGroups(self):
		shared.DPrint("Render",1,"Initializing Resource Groups")
		ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
		ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
 
	def setupScene(self):
		shared.DPrint("Render",1,"Setting up scene")
		shared.render3dScene=render3d.Scene()
		shared.render3dScene.Setup()
		 
	def setupInputSystem(self):
		shared.DPrint("Render",1,"Setting up I/O")
		shared.renderioInput=renderio.Input()
		shared.renderioInput.Setup()
 
	def setupCEGUI(self):
		shared.DPrint("Render",1,"Setting up GUI")
		shared.renderguiGUI=rendergui.GUI()
		shared.renderguiGUI.Setup()

	def setupDebuggingTools(self):
		shared.DPrint("Render",1,"Setting up DBGTools")
		shared.console = renderconsole.Console(self.root)
		shared.console.addLocals({'root':self.root})
		#shared.console.show()

	def createFrameListener(self):
		shared.DPrint("Render",1,"Creating Framelisteners")
		self.renderlistener = RenderListener()
		#self.pframeListener.showDebugOverlay(True)
		self.renderqueue=[]

		self.renderqueue.append(self.renderlistener)
		self.renderqueue.append(shared.renderioInput)
		self.renderqueue.append(shared.unitHandeler)
		self.renderqueue.append(shared.DirectorManager)

	def renderHook(self):
		self.deltatime=time()-self.alphatime
		self.alphatime=time()
		#print(self.deltatime)

		try:
			for x in self.renderqueue:
				if not x.frameRenderingQueued(self.deltatime):
					reactor.stop()
		except:
			reactor.stop()
			print_exc()

		#if not self.root.window.isClosed():
		if True:
			self.weu.messagePump()

			#if self.root.window.isActive():
			if True:
				self.root.renderOneFrame()
		else:
			reactor.stop()
		reactor.callLater(0,self.renderHook)

	def startRenderLoop(self):
		shared.DPrint("Render",1,"Starting renderloop")
		#self.root.startRendering()
		shared.unitHandeler.PowerUp()
		self.weu = ogre.WindowEventUtilities()
		reactor.callLater(0,self.renderHook)

		self.alphatime=time()

		global QUITTIMER
		if QUITTIMER!=0 or QUITTIMER!=None:
			reactor.callLater(QUITTIMER, lambda: reactor.stop())
 
	def cleanUp(self): #This cleanup function needs to be cleaned up! No pun intended
		shared.DPrint("Render",2,"Cleaning up!")
		shared.renderioInput.inputManager.destroyInputObjectKeyboard(shared.renderioInput.Keyboard)
		shared.renderioInput.inputManager.destroyInputObjectMouse(shared.renderioInput.Mouse)
		try:
			shared.renderioInput.inputManager.destroyInputObjectJoyStick(self.joystick)
		except:
			pass
		#shared.renderioInput.InputManager.destroyInputSystem(shared.renderioInput.inputManager)
		#self.inputManager = None

class RenderListener(ogre.FrameListener):
	#This class has functions which is needed/runs each frame
	def __init__(self):
		ogre.FrameListener.__init__(self)
		self.scene=shared.render3dScene
		self.input=shared.renderioInput
		self.gui=shared.renderguiGUI
		self.RT=shared.renderRoot.getAutoCreatedWindow()
		self.FPS=0
		# self.FPSc=0
		# self.FPSt=0
		# self.FPSs=0
		# self.FPSsample=2
		# self.FPStable=range(0,self.FPSsample)
	def frameRenderingQueued(self, evt):
		# if self.FPSt!=gmtime()[5]:
		# 	if self.FPSs==self.FPSsample:
		# 		self.FPSs=0
		# 	self.FPStable[self.FPSs]=self.FPSc
		# 	self.FPSt=gmtime()[5]
		# 	self.FPSs=self.FPSs+1
		# 	self.FPSc=0
		# else:
		# 	self.FPSc=self.FPSc+1
		# self.FPS=sum(self.FPStable)/self.FPSsample
		# #print(self.FPStable)
		self.gui.FPScounter.setText(str(int(self.RT.getLastFPS()))+"|"+str(int(self.RT.getWorstFPS())))
		self.gui.DIVcounter.setText(str(int(self.RT.getTriangleCount()))+"|"+str(int(self.RT.getBatchCount())))
		# self.FPS=self.FPS+1
		# if self.FPS>60:
		# 	tt=gmtime()[5]+1
		# 	while gmtime()[5]!=tt:
		# 		pass
		#print self.FPStable
		return True

class Unit():
	def __init__():
		pass