#Mainmodule - DirectorManager
#This module keeps track of the different directors, and allows you to append units on an director

from engine import shared, debug
from ogre.renderer.OGRE import FrameListener

class DirectorManager(FrameListener):
	def __init__(self):
		shared.DPrint("dir",0, "Initializing Directors..")
		
		from directors import Demo, Net
		self.DirDemo=Demo.Director()
		self.DirNet=Net.Director()

	def Init(self, director):
		#Get Michael Bay ready to direct the scene
		if director=="Demo":
			self.DirDemo.Init()
		elif director=="Net":
			self.DirNet.Init()

	def Action(self, director):
		#Action! Start directing the scene
		if director=="Demo":
			self.DirDemo.Action()
		elif director=="Net":
			self.DirNet.Action()