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
		shared.render.Hook.Add("OnRenderFrame", self.ThinkPlayers)

	def getFromUID(self, uid):
		if int(uid)==int(shared.SelfPlayer.UID):
			return shared.SelfPlayer
		try:
			return self.PDict[int(uid)]
		except:
			print_exc()
			return False


	#### REQUESTS
		
	#### SERVERUPDATES / COMMANDS

	def recv_playerlist(self, method, playerlist):
		shared.DPrint("PlayerManager", 0, "Got Playerlist")
		self.playerlist=playerlist
		shared.DPrint("PlayerManager", 0, "Current players: "+str(len(self.playerlist)))

		for x in self.playerlist:
			if x["uid"]!=shared.SelfPlayer.UID:
				self.PDict[x["uid"]]=Player(x["uid"], x["username"], x["team"], x["info"])
				shared.DPrint("PlayerManager", 1, "Player "+x["username"]+" ("+str(x["uid"])+")"+" joined the game")

	def getPlayersInTeam(self, team):
		for pid, player in self.PDict.iteritems():
			if player.team == team:
				yield player

	def recv_chteam(self, ID, team, Protocol=None):
		player = self.getFromUID(ID)
		if player == shared.SelfPlayer:
			for player in self.getPlayersInTeam(team):
				#NEED TO GET ALL NODES BELONGING TO PLAYER
				shared.FowManager.convertNode()

		player.team = team
		shared.DPrint("PlayerManager", 1, "Player "+player.username+" ("+str(ID)+")"+" changed team to "+str(player.team))


	def HI(self, ID, username, team, extras, Protocol=None):
		self.playerlist.append({"uid":ID, "username":username, "info":extras})
		self.PDict[ID]=Player(ID, username, team, extras)
		shared.DPrint("PlayerManager", 1, "Player "+username+" ("+str(ID)+")"+" joined the game!")

	#### EVENTS

	def ThinkPlayers(self, deltatime):
		shared.SelfPlayer.Think(deltatime)
		for pid, player in self.PDict.iteritems():
			player.Think(deltatime)