#MainModule - Render
#Submodules: render3d, rendergui, renderio, renderphys
import render3d, rendergui, renderio, renderphys, renderconsole
from twisted.internet import reactor
from engine import shared, debug
from engine.Lib.hook import Hook
from time import gmtime, sleep, time
from traceback import print_exc
import ogre.renderer.OGRE as ogre

shared.DPrint(1,1,"Imported..")

global QUITTIMER
QUITTIMER=None #Set this to a time in secounds if you want the game to automaticly quit. 0 or None disables it.

class RenderApplication(object):
	#This class setups and starts all rendermodules
	def __init__(self, bare=False):
		shared.DPrint("Render",1,"Initializing")

		#Bare defines if this module should setup things or not.
		#If BARE==True only initialization will be done, and setup will be handeled elsewhere
		#Mostly only affects renderGUI and renderScene
		self.BARE=bare
		self.PROFILING = True

		self.renderqueue=[]

	def PowerUp(self):
		self.createRoot()
		self.setupEssentials()
		self.defineResources()
		self.setupRenderSystem()
		self.createRenderWindow()
		self.initializeResourceGroups()
		self.initializeInputSystem()
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

	def setupEssentials(self):
		self.Hook = Hook(self)
		self.Hook.new("OnRenderFrame", 1) #Deltatime
 
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
		self.renderwindow = self.root.initialise(True, "YARTS: v. 0E-inf")
 
	def initializeResourceGroups(self):
		shared.DPrint("Render",1,"Initializing Resource Groups")
		ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
		ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()

	def initializeInputSystem(self):
		shared.DPrint("Render",1,"Initializing InputSystem")
		shared.renderioInput=renderio.Input()
 
	def setupScene(self):
		shared.DPrint("Render",1,"Setting up scene")
		shared.render3dScene=render3d.Scene()
		shared.FowManager=None
		if not self.BARE:
			shared.FowManager=True
			shared.render3dScene.Setup()
			shared.render3dScene.FowSetup()
			shared.render3dScene.MinimapSetup()
		 
	def setupInputSystem(self):
		if not self.BARE:
			shared.DPrint("Render",1,"Setting up InputSystem")
			shared.renderioInput.Setup()
 
	def setupCEGUI(self):
		shared.DPrint("Render",1,"Setting up GUI")
		shared.renderGUI=rendergui.GUI()
		if not self.BARE:
			shared.renderGUI.Setup()

	def setupDebuggingTools(self):
		shared.DPrint("Render",1,"Setting up DBGTools")
		shared.console = renderconsole.Console(self.root)
		shared.console.addLocals({'root':self.root})
		#shared.console.show()

	def createFrameListener(self):
		shared.DPrint("Render",1,"Creating Framelisteners")
		self.renderlistener = RenderListener()
		#self.pframeListener.showDebugOverlay(True)

		#self.renderqueue.append(self.renderlistener)
		reactor.callLater(1, self.renderlistener.frameRenderingQueued)

		self.renderqueue.append(shared.DirectorManager)

	def renderHook(self):
		self.deltatime=time()-self.alphatime
		self.alphatime=time()
		#print(self.deltatime)

		#Old updatemethod (Still used by some low-level engine modules)
		try:
			for x in self.renderqueue:
				if self.PROFILING:
					starttime = time()

					if not x.frameRenderingQueued(self.deltatime):
						reactor.stop()
						print_exc()

					endtime = time()
					timeused = endtime - starttime

					valueExists = False
					for pro_value in shared.Profile:
						if pro_value[0] == str(x):
							valueExists = (pro_value, (str(x), timeused))

					if valueExists:
						indx = shared.Profile.index(valueExists[0])
						shared.Profile[indx] = valueExists[1]
					else:
						shared.Profile.append((str(x), timeused))

				else:
					if not x.frameRenderingQueued(self.deltatime):
						reactor.stop()
						print_exc()
		except:
			reactor.stop()
			print_exc()

		#New updatemethod, uses hooks instead
		if self.Hook.call("OnRenderFrame", self.deltatime) == False:
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
		self.weu = ogre.WindowEventUtilities()

		reactor.callLater(0,self.renderHook)

		self.alphatime=time()

		global QUITTIMER
		if QUITTIMER!=0 and QUITTIMER!=None:
			reactor.callLater(QUITTIMER, lambda: shared.DPrint("Render", 5, "Game killed due to QUITTIMER!"))
			reactor.callLater(QUITTIMER, lambda: reactor.stop())
 
	def cleanUp(self): #This cleanup function needs to be cleaned up! No pun intended
		shared.DPrint("Render",2,"Cleaning up!")
		shared.renderioInput.inputManager.destroyInputObjectKeyboard(shared.renderioInput.Keyboard)
		shared.renderioInput.inputManager.destroyInputObjectMouse(shared.renderioInput.Mouse)
		try:
			shared.renderioInput.inputManager.destroyInputObjectJoyStick(self.joystick)
		except:
			pass
		shared.DPrint("Render",2,"Shutting down root render object")
		self.root.shutdown()
		shared.DPrint("Render",2,"Destroying InputSystem")
		shared.renderioInput.inputManager.destroyInputSystem(shared.renderioInput.inputManager)
		shared.renderioInput.inputManager = None

class RenderListener(ogre.FrameListener):
	#This class has functions which is needed/runs each frame
	def __init__(self):
		ogre.FrameListener.__init__(self)
		self.scene=shared.render3dScene
		self.input=shared.renderioInput
		self.gui=shared.renderGUI
		self.RT=shared.renderRoot.getAutoCreatedWindow()
		self.FPS=0
		# self.FPSc=0
		# self.FPSt=0
		# self.FPSs=0
		# self.FPSsample=2
		# self.FPStable=range(0,self.FPSsample)
	def frameRenderingQueued(self):
		reactor.callLater(2, self.frameRenderingQueued)
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
		if debug.GUISTATS:
			RT = shared.renderRoot.getAutoCreatedWindow()
			shared.gui['debug'].FPScounter.setText(str(int(RT.getLastFPS()))+"|"+str(int(RT.getWorstFPS())))
			shared.gui['debug'].DIVcounter.setText(str(int(RT.getTriangleCount()))+"|"+str(int(RT.getBatchCount())))
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