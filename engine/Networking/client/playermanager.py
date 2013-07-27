#Clientside Playermanager
from traceback import print_exc
from time import time
from engine import debug, shared
from twisted.internet import reactor

from player import Player
import selfplayer

class PlayerManager():
	def __init__(self):
		shared.PlayerManager=self
		shared.objectManager.addEntry(0, 2, self)

		#Set up this persons player
		shared.DPrint("PlayerManager", 0, "Creating SelfPlayer..")
		shared.SelfPlayer=selfplayer.SelfPlayer()

		#Get initial player data
		self.playerlist={}
		shared.DPrint("PlayerManager", 0, "Requesting Playerlist")
		shared.protocol.sendMethod(2, "LP", [])
		shared.client.RetMeBack(self.recv_playerlist, "LP")

		#Initialize the clientside versions of the players in the game
		self.PDict={}

		#Start thinking!
		self.lastframe=time()
		self.ThinkPlayers()

	def getFromUID(self, uid):
		print(str(uid) +"|=|"+ str(shared.SelfPlayer.UID))
		if int(uid)==int(shared.SelfPlayer.UID):
			return shared.SelfPlayer
		try:
			return self.PDict[int(uid)]
		except:
			print_exc()
			return False
		
	def recv_playerlist(self, method, playerlist):
		shared.DPrint("PlayerManager", 0, "Got Playerlist")
		self.playerlist=playerlist
		shared.DPrint("PlayerManager", 0, "Current players: "+str(len(self.playerlist)))

		for x in self.playerlist:
			if x["uid"]!=shared.SelfPlayer.UID:
				self.PDict[x["uid"]]=Player(x["uid"], x["username"], x["info"])
				shared.DPrint("PlayerManager", 1, "Player "+x["username"]+" ("+str(x["uid"])+")"+" joined the game")


	def HI(self, username, ID, extras, Protocol=None):
		self.playerlist.append({"uid":ID, "username":username, "info":extras})
		self.PDict[ID]=Player(ID, username, extras)
		shared.DPrint("PlayerManager", 1, "Player "+username+" ("+str(ID)+")"+" joined the game!")

	def ThinkPlayers(self):
		reactor.callLater(0, self.ThinkPlayers)
		deltatime = time()-self.lastframe
		self.lastframe=time()

		shared.SelfPlayer.Think(deltatime)
		for pid, player in self.PDict.iteritems():
			player.Think(deltatime)