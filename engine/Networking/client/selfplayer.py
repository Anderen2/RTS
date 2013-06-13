#Clientside SelfPlayer
import pickle
from twisted.internet import reactor
from random import randrange

from engine import shared, debug
from engine.Networking import sh_netObject, sh_netMethod

class SelfPlayer():
	def __init__(self):
		self.username="Anderen2"+str(randrange(0,100,1))
		self.team=randrange(1,2,1)
		self.PickledExtras={"team":self.team, "land":"Of the dead"}
		self.ID=None

		self.brandwidthsaver=[]

		#Player join Handshake
		shared.DPrint("SelfPlayer", 0, "Sending Join Handshake..")
		shared.protocol.sendMethod(2, "HI", [self.username, pickle.dumps(self.PickledExtras)])
		shared.client.RetMeBack(self.recv_HI, "HI")

	def recv_HI(self, method, ID):
		shared.DPrint("SelfPlayer", 0, "Server is joined.")
		self.ID=ID

	def MoveUnits(self, selected, pos):
		if selected!=self.brandwidthsaver:
			juicypickle=pickle.dumps(selected)
		else:
			juicypickle="0"
		shared.protocol.sendMethod(2, "req_moveunit", [juicypickle, pos[0], pos[1], pos[2]])
