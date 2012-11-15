#Mainmodule - DirectorManager
#This module keeps track of the different directors, and allows you to append units on an director

from engine import shared, debug
from ogre.renderer.OGRE import FrameListener

class DirectorManager(FrameListener):
	def __init__(self):
		shared.DPrint("dir",0, "Initializing Directors..")
		
		from directors import Simple
		#self.DirDemo=Demo.Director()
		#self.DirNet=Net.Director()
		self.Simple=Simple.Director()

		debug.ACC("dirinit", self.Init, args=1, info="Initialize an director")
		debug.ACC("diraction", self.Action, args=1, info="Start directing with an director")

	def Init(self, director):
		#Get Michael Bay ready to direct the scene
		if director=="Demo":
			self.DirDemo.Init()
		elif director=="Net":
			self.DirNet.Init()
		elif director=="Simple":
			self.Simple.Init()

	def Action(self, director):
		#Action! Start directing the scene
		if director=="Demo":
			self.DirDemo.Action()
		elif director=="Net":
			self.DirNet.Action()
		elif director=="Simple":
			self.Simple.Action()