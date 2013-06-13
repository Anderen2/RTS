#Serverside Player
import pickle
from twisted.internet import reactor
from engine import debug, shared

class Player():
	def __init__(self, UID, Username, Protocol, PickledExtras):
		self.PlayerInfo=pickle.loads(PickledExtras)
		self.UID=UID
		self.username=Username
		self.team = self.PlayerInfo["team"]
		self.Protocol=Protocol

	def Setup(self):
		shared.ChatManager.addMember(self.UID, 1)