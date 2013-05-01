#Clientside Playermanager
import pickle
from engine import debug, shared

from player import Player
import selfplayer

class PlayerManager():
	def __init__(self):
		shared.PlayerManager=self
		shared.objectManager.addEntry(0, 2, self)

		#Get initial player data
		self.playerlist={}
		shared.DPrint("PlayerManager", 0, "Requesting Playerlist")
		shared.protocol.sendMethod(2, "LP", [])
		shared.client.RetMeBack(self.recv_playerlist, "LP")

		#Set up this persons player
		shared.DPrint("PlayerManager", 0, "Creating SelfPlayer..")
		shared.SelfPlayer=selfplayer.SelfPlayer()

		#Initialize the clientside versions of the players in the game
		self.PDict={}
		
	def recv_playerlist(self, method, playerlist):
		shared.DPrint("PlayerManager", 0, "Got Playerlist")
		self.playerlist=pickle.loads(playerlist)

		for x in self.playerlist:
			self.PDict[x["uid"]]=Player(x["uid"], x["username"], x["info"])
			shared.DPrint("PlayerManager", 1, "Player "+x["username"]+" ("+str(x["uid"])+")"+" joined the game")


	def HI(self, username, ID, pickledextras):
		self.playerlist.append({"uid":ID, "username":username, "info":pickledextras})
		self.PDict[ID]=Player(ID, username, pickledextras)
		shared.DPrint("PlayerManager", 1, "Player "+username+" ("+str(ID)+")"+" joined the game!")