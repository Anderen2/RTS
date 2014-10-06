#Clientside SelfPlayer
#This class defines how the player speaks his moves to the server, aswell as translates incoming messages regarding the player or his units
from twisted.internet import reactor
from random import randrange

from engine import shared, debug
from engine.Networking import sh_netObject, sh_netMethod

class SelfPlayer():
	def __init__(self):
		self.username="Anderen2"+str(randrange(0,100,1))
		self.team=0
		self.color=(randrange(0,255), randrange(0,255), randrange(0,255))
		self.Extras={"team":self.team, "land":"Of the dead", "color":self.color}
		self.UID=None
		self.yourself = True

		self.Units=[]
		self.brandwidthsaver=[]

		#Player join Handshake
		shared.DPrint("SelfPlayer", 0, "Sending Join Handshake..")
		shared.protocol.sendMethod(2, "HI", [self.username, self.team, self.Extras])
		shared.client.RetMeBack(self.recv_HI, "HI")

		#Console Commands
		debug.ACC("self_chteam", self.requestChangeTeam, info="Request to change team", args=1)

	def Think(self, delta):
		for unit in self.Units:
			unit._think(delta)

	### RECIEVE / Incoming messages (Server Request)

	def recv_HI(self, method, UID):
		shared.DPrint("SelfPlayer", 0, "Server is joined.")
		self.UID=int(UID)

	### TRANSMITT / Outgoing messages (Client Request)

	def requestChangeTeam(self, team):
		team = int(team)
		shared.protocol.sendMethod(2, "req_changeteam", [team])