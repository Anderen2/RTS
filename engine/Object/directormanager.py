#Mainmodule - DirectorManager
#This module keeps track of the different directors, and allows you to append units on an director

from engine import shared, debug
from ogre.renderer.OGRE import FrameListener

class DirectorManager(FrameListener):
	def __init__(self):
		FrameListener.__init__(self)
		shared.DPrint("dir",0, "Initializing Directors..")
		
		from directors import Net, Simple, Mapeditor
		#self.DirDemo=Demo.Director()
		self.DirNet=Net.Director()
		self.Simple=Simple.Director()
		self.Mapeditor=Mapeditor.Director()

		self.CurrentDirector=None
		self.actionQueueing=False

		debug.ACC("dirinit", self.Init, args=1, info="Initialize an director")
		debug.ACC("diraction", self.Action, args=1, info="Start directing with an director")
		#self.Init("Simple")

	def Init(self, director):
		#Get Michael Bay ready to direct the scene
		if director=="Demo":
			self.DirDemo.Init()
		elif director=="Net":
			self.DirNet.Init()
		elif director=="Simple":
			self.Simple.Init()
		elif director=="Mapeditor":
			self.Mapeditor.Init()
		else: 
			shared.DPrint("dir",1,"Director "+director+" not found")
			return ("Director "+director+" not found")
		shared.DPrint("dir",1,"Director "+director+" Initialized")

	def Action(self, director):
		#Action! Start directing the scene
		if director=="Demo":
			self.DirDemo.Action()
			self.CurrentDirector=self.DirDemo
		elif director=="Net":
			self.DirNet.Action()
			self.CurrentDirector=self.DirNet
		elif director=="Simple":
			self.Simple.Action()
			self.CurrentDirector=self.Simple
		elif director=="Mapeditor":
			self.Mapeditor.Action()
			self.CurrentDirector=self.Mapeditor
		else: 
			shared.DPrint("dir",1,"Director "+director+" not found")
			return ("Director "+director+" not found")
		shared.DPrint("dir",1,"Director "+director+" actionized")

	def SelectedEvent(self, sellist):
		shared.DPrint("dir", 0, "Updating Selections...")
		if self.CurrentDirector!=None:
			self.CurrentDirector.evt_selected(sellist, self.actionQueueing)
		else:
			shared.DPrint("dir", 0, "No directors are initialized!")
		if debug.AABB:
			pass

	def MovementEvent(self, pos):
		if self.CurrentDirector!=None:
			self.CurrentDirector.evt_moveclick(pos, self.actionQueueing)
			shared.WaypointManager.ShowTime(0, pos, 1)

	def ActionEvent(self, data):
		if self.CurrentDirector!=None:
			self.CurrentDirector.evt_actionclick(data, self.actionQueueing)

	def frameRenderingQueued(self, evt):
		if self.CurrentDirector!=None:
			self.CurrentDirector.Frame()
		return True