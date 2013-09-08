#Render3dEnt Extension - render3denteff
#Classes for handeling Entity "Effects"

from engine import shared, debug
from engine.shared import DPrint
from engine.shared import Vector

class BuildEffect():
	def __init__(self, ent):
		self.ent = ent

	def Start(self):
		self.meshname = self.ent.params["mesh"]
		#Create new mesh at the buildsite
		#Position according to terrain
		#Use an material to color it transparent green
		#Position self.ent directly below ground
		#Calculate progress-step according to ground elevation and entity height

	def UpdateProgress(self, progress):
		#Update self.ent's elevation according to progress*progress-step
		