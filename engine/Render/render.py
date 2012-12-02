#MainModule - Render
#Submodules: render3d, rendergui, renderio, renderphys
import render3d, rendergui, renderio, renderphys, console
from engine import shared
from time import gmtime, sleep
import ogre.renderer.OGRE as ogre

shared.DPrint(1,1,"Imported..")

class RenderApplication(object):
	#This class setups and starts all rendermodules
	def __init__(self):
		shared.DPrint(1,1,"Initializing")

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
		self.cleanUp()

	def createRoot(self):
		shared.DPrint(1,1,"Creating Root")
		self.root = ogre.Root()
		shared.renderRoot=self.root
 
	def defineResources(self):
		shared.DPrint(1,1,"Defining Resources")
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
		shared.DPrint(1,1,"Setting up RenderSystem")
		if not self.root.restoreConfig() and not self.root.showConfigDialog():
			raise Exception("User canceled the config dialog! -> Application.setupRenderSystem()")
 
	def createRenderWindow(self):
		shared.DPrint(1,1,"Creating renderwindow")
		self.root.initialise(True, "RTS Small Start")
 
	def initializeResourceGroups(self):
		shared.DPrint(1,1,"Initializing Resource Groups")
		ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
		ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
 
	def setupScene(self):
		shared.DPrint(1,1,"Setting up scene")
		shared.render3dScene=render3d.Scene()
		shared.render3dScene.Setup()
		 
	def setupInputSystem(self):
		shared.DPrint(1,1,"Setting up I/O")
		shared.renderioInput=renderio.Input()
		shared.renderioInput.Setup()
 
	def setupCEGUI(self):
		shared.DPrint(1,1,"Setting up GUI")
		shared.renderguiGUI=rendergui.GUI()
		shared.renderguiGUI.Setup()

	def setupDebuggingTools(self):
		shared.DPrint(1,1,"Setting up DBGTools")
		shared.console = console.Console(self.root)
		shared.console.addLocals({'root':self.root})
		#shared.console.show()
 
	def createFrameListener(self):
		shared.DPrint(1,1,"Creating Framelisteners")
		self.renderlistener = RenderListener()
		#self.pframeListener.showDebugOverlay(True)
		self.root.addFrameListener(self.renderlistener)
		self.root.addFrameListener(shared.renderioInput)
		self.root.addFrameListener(shared.unitHandeler)
		self.root.addFrameListener(shared.DirectorManager)
 
	def startRenderLoop(self):
		shared.DPrint(1,1,"Starting renderloop")
		self.root.startRendering()
		shared.unitHandeler.PowerUp()
 
	def cleanUp(self): #This cleanup function needs to be cleaned up! No pun intended
		shared.DPrint(1,2,"Cleaning up!")
		shared.renderioInput.inputManager.destroyInputObjectKeyboard(self.keyboard)
		shared.renderioInput.inputManager.destroyInputObjectMouse(self.mouse)
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