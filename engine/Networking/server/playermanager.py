#Serverside Playermanager

from twisted.internet import reactor
from engine import debug, shared
from player import Player

class PlayerManager():
	def __init__(self):
		shared.PlayerManager=self
		shared.objectManager.addEntry(0,2, self)
		self.PlayerCount=0
		self.PDict={}

		self.brandwidthsaver=[]

	def HI(self, Username, Extras, Protocol=None):
		if not self.getFromProto(Protocol):
			self.PlayerCount+=1
			self.Broadcast(2, "HI", [Username, str(self.PlayerCount), Extras])
			self.PDict[self.PlayerCount]=Player(self.PlayerCount, Username, Protocol, Extras)
			reactor.callLater(1, self.PDict[self.PlayerCount].Setup)
			return [str(self.PlayerCount)]
		else:
			Protocol.sendMethod(3, "SA", ["-1", "0", "You are already in the game."])

	def LP(self, Protocol=None):
		foolist=[]
		for x in self.PDict:
			foolist.append({"uid":self.PDict[x].UID, "username":self.PDict[x].username, "info":self.PDict[x].PlayerInfo})

		return [foolist]

	def req_moveunit(self, selected, x, y, z, Protocol=None):
		if selected!="0":
			self.brandwidthsaver=selected

		## IF PLAYER OWNS ALL UNITS CHECK HERE! ! !
		## Tempoary testing workaround (All players could move all units)
		shared.UnitManager.massMove(self.brandwidthsaver, (x, y, z))


	def Broadcast(self, obj, method, args):
		for x in self.PDict:
			self.PDict[x].Protocol.sendMethod(obj, method, args)

	def getFromUID(self, uid):
		try:
			return self.PDict[uid]
		except:
			return False

	def getFromProto(self, proto):
		try:
			for x in self.PDict:
				if self.PDict[x].Protocol==proto:
					return self.PDict[x]
			return False
		except:
			return None