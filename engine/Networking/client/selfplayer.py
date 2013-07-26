#Clientside SelfPlayer
#This class defines how the player speaks his moves to the server, aswell as translates incoming messages regarding the player or his units
from twisted.internet import reactor
from random import randrange

from engine import shared, debug
from engine.Networking import sh_netObject, sh_netMethod

class SelfPlayer():
	def __init__(self):
		self.username="Anderen2"+str(randrange(0,100,1))
		self.team=randrange(1,2,1)
		self.PickledExtras={"team":self.team, "land":"Of the dead"}
		self.UID=None

		self.Units=[]
		self.brandwidthsaver=[]

		#Player join Handshake
		shared.DPrint("SelfPlayer", 0, "Sending Join Handshake..")
		shared.protocol.sendMethod(2, "HI", [self.username, self.PickledExtras])
		shared.client.RetMeBack(self.recv_HI, "HI")

	### RECIEVE / Incoming messages (Server Request)

	def recv_HI(self, method, UID):
		shared.DPrint("SelfPlayer", 0, "Server is joined.")
		self.UID=int(UID)

	### TRANSMITT / Outgoing messages (Client Request)

	def MoveUnits(self, selected, pos):
		if selected!=self.brandwidthsaver:
			juicypickle=selected
		else:
			juicypickle="0"
		shared.protocol.sendMethod(2, "req_moveunit", [juicypickle, pos[0], pos[1], pos[2]])

	def AddGroup(self, persistent, unitids):
		pickledunits = unitids
		persistent = str(int(persistent))
		shared.protocol.sendMethod(5, "req_newgroup", [persistent, pickledunits])