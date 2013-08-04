#Serverside Playermanager

from time import time
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

		#Player Thinking
		self.lastframe=time()
		self.ThinkPlayers()

	#### CLIENT REQUESTS

	def HI(self, Username, Team, Extras, Protocol=None):
		if not self.getFromProto(Protocol):
			self.PlayerCount+=1
			self.Broadcast(2, "HI", [self.PlayerCount, Username, Team, Extras])
			self.PDict[self.PlayerCount]=Player(self.PlayerCount, Username, Team, Extras, Protocol)
			reactor.callLater(1, self.PDict[self.PlayerCount].Setup)
			return [self.PlayerCount]
		else:
			Protocol.sendMethod(3, "SA", ["-1", "0", "You are already in the game."])

	def LP(self, Protocol=None):
		foolist=[]
		for x in self.PDict:
			foolist.append({"uid":self.PDict[x].UID, "username":self.PDict[x].username, "team":self.PDict[x].team, "info":self.PDict[x].PlayerInfo})

		return [foolist]

	def req_changeteam(self, team, Protocol=None):
		### Trigger for Gamemode handeling here!
		Player = self.getFromProto(Protocol)
		Player.changeTeam(team)


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

	def ThinkPlayers(self):
		reactor.callLater(0, self.ThinkPlayers)
		deltatime = time()-self.lastframe
		self.lastframe=time()

		for pid, player in self.PDict.iteritems():
			player.Think(deltatime)