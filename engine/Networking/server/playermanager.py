#Serverside Playermanager

from time import time
from string import split
from twisted.internet import reactor
from engine import debug, shared
from player import Player

class PlayerManager():
	def __init__(self):
		shared.PlayerManager=self
		shared.objectManager.addEntry(0,2, self)
		self.PlayerCount=0
		self.PDict={}

		self.mapUnits = {}

		self.brandwidthsaver=[]

		#Add "None-player"
		self.PDict[-1]=Player(-1, "None", -1, {"land":"", "color":(1,1,1)}, None)

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
			if x!=-1:
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

	def CatchUp(self, ply):
		#Allows players joining late to get synced into the current game state
		shared.ChatManager.systemSay("Player %s joined the game" % ply.username)
		if shared.UnitManager.unitcount!=0:
			shared.ChatManager.systemSay("Player %s joined the game late, syncing state.." % ply.username)
			for unit in shared.UnitManager.generateAllUnits():
				attrib = unit.currentattrib.copy()
				attrib["pos"] = unit.GetPosition()
				ply.Protocol.sendMethod(4, "build", [unit.UnitID, unit._owner.UID, unit.ID, attrib])

	def SetupMapUnits(self, mapconfig):
		for ID, Content in mapconfig.iteritems():
			name = mapconfig[ID]["name"]
			playerid = int(mapconfig[ID]["pid"])
			pos = mapconfig[ID]["pos"]
			pos = (float(pos[0]), float(pos[1]), float(pos[2]))
			rot = mapconfig[ID]["rot"]
			attribs = mapconfig[ID]["attribs"]
			attributes = {}

			if attribs!="":
				print attribs
				attribs=split(attribs,";")
				print attribs
				for attrib in attribs:
					if attrib!="":
						foo = split(attrib, "=")
						print foo
						try:
							attributes[foo[0]]=int(foo[1])
						except:
							attributes[foo[0]]=foo[1]

			if not playerid in self.mapUnits:
				self.mapUnits[playerid] = []

			if playerid != -1: #If the unit is a prebuilt structure that should later be auto-provided
				unit = shared.UnitManager.preCreate(playerid, name, ID, pos, attribs=attributes)
				self.mapUnits[playerid].append(unit)
			else:
				unit = shared.UnitManager.preCreate(self.getFromUID(-1), name, ID, pos, attribs=attributes)
				self.mapUnits[playerid].append(unit)
				self.getFromUID(-1).addUnit(unit)

	def PlayerStartupUnits(self, player):
		print player.UID
		print self.mapUnits
		if player.UID in self.mapUnits:
			for unit in self.mapUnits[player.UID]:
				unit._owner=player
				player.addUnit(unit)

				attrib = unit.currentattrib.copy()
				attrib["pos"] = unit.GetPosition()
				player.Protocol.sendMethod(4, "build", [unit.UnitID, unit._owner.UID, unit.ID, attrib])


	def ThinkPlayers(self):

		#Ugly "vsync" below, keeps the playersimulation running at ~60FPS just as the client does

		deltatime = time()-self.lastframe
		self.lastframe=time()

		syncframe = time()

		for pid, player in self.PDict.iteritems():
			player.Think(deltatime)
		
		synctime = time() - syncframe

		waiter = 0.016666666666666666- synctime

		if waiter<0:
			waiter = 0

		#print(deltatime)

		reactor.callLater(waiter, self.ThinkPlayers)