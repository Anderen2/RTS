#Render3dExtension - render3ddebug
#Classes for rendering various useful debug stuff

from engine import shared, debug
from engine.shared import DPrint
import ogre.renderer.OGRE as ogre
import render3dshapes as Shape

class aStarView():
	def __init__(self):
		self.status = False
		self.ents = []

	def toggle(self):
		pass

	def online(self):
		for node in shared.Pathfinder.aStarPath.totnodes:
			newent = 

	def offline(self):
		pass