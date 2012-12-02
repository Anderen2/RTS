#Director - Net
#Networked Director

from engine import shared, debug

class Director():
	def __init__(self):
		self.Active=False

	def Init(self):

		self.gotoX=None
		self.gotoY=None
		self.gotoz=None

	def Action(self):
		self.Cast=[]
		self.UnitAdd("plane")
		self.Active=True

	def UnitGo(self, x, z):
		self.gotoX=x
		self.gotoZ=z

	def UnitAim(self, x, y, z):
		for actor in self.Cast:
			actor._look(x, y, z)

	def UnitPri(self):
		pass

	def UnitSec(self):
		pass

	def UnitAdd(self, name):
		self.Cast.append(shared.unitManager.CreateMov(4, 0, 0, "plane"))

	def UnitDelAll(self):
		pass

	def Frame(self):
		if self.Active:
			#This will get executed each frame
			if self.gotoX!=None:
				x=self.gotoX
				z=self.gotoZ
				for actor in self.Cast:
					print actor
					print (x, z)
					print (float(x), float(z))
					dist=actor._movetowards(float(x), float(z))
					if dist==0:
						self.gotoX=None
					print dist