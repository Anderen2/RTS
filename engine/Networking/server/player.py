#Serverside Player
from twisted.internet import reactor
from engine import debug, shared

class Player():
	def __init__(self, UID, Username, Team, Extras, Protocol):
		self.PlayerInfo=Extras
		self.UID=UID
		self.username=Username
		self.team = self.PlayerInfo["team"]
		self.Protocol=Protocol

		self.Units=[]
		self.persistentgroups=[]

	def Setup(self):
		shared.ChatManager.addMember(self.UID, 1)

	def addUnit(self, unit):
		self.Units.append(unit)

	def changeTeam(self, team):
		self.team = team
		shared.PlayerManager.Broadcast(2, "recv_chteam", [self.UID, self.team])

	def Think(self, delta):
		for unit in self.Units:
			unit._think(delta)