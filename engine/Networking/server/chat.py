#Serverside chat
import pickle
from twisted.internet import reactor
from engine import debug, shared
from traceback import print_exc

class ChatManager():
	def __init__(self):
		shared.ChatManager=self
		shared.objectManager.addEntry(0,3, self)
		self.Channels=[] #Public, Echo, Team 1 - inf
		self.createBaseChannels()

	def createBaseChannels(self):
		self.createChannel("loop", "Loopback-channel")
		self.createChannel("Public", "Public Channel")

	def createChannel(self, channelname, desc):
		self.Channels.append(Channel(channelname, desc, len(self.Channels)))

	def addMember(self, uid, cid):
		if not uid in self.Channels[cid].members:
			channel = self.Channels[cid]
			
			#Notify the members of the channel
			channel.broadcast("NCU", [cid, uid])

			#Add him serverside
			channel.members.append(uid) 

			#Add him clientside
			player = shared.PlayerManager.getFromUID(uid)
			player.Protocol.sendMethod(3, "AC", [cid, channel.name, channel.desc, channel.members])

		else:
			print("Member "+str(uid)+" already in channel "+str(cid)+"!")

	def serverSay(self, message, channel=1):
		ch = self.getFromCID(channel)
		ch.sendMessage(-1, message)

	def systemSay(self, message, channel=1):
		ch = self.getFromCID(channel)
		ch.sendMessage(-2, message)

	def LC(self, Protocol=None):
		"""List Channels"""
		player=shared.PlayerManager.getFromProto(Protocol)

		channels = {}

		for x in self.Channels:
			if player.UID in x.members:
				channels[x.CID]=[x.name, x.desc, x.members]

		Protocol.sendMethod(3, "LC", [channels])

	def SA(self, cid, mesg, Protocol=None):
		"""Incoming chatmessage"""
		player=shared.PlayerManager.getFromProto(Protocol)
		cid=int(cid)

		try:
			channel=self.Channels[cid]
		except:
			print("Player: "+player.username+" ("+str(player.UID)+") tried to talk in non-exsistant channel: "+str(cid))
			return None

		if player.UID in channel.members:
			channel.sendMessage(player.UID, mesg)
		else:
			print("Player: "+player.username+" ("+str(player.UID)+") tried to talk in non-member channel: "+channel.name+" ("+str(channel.CID)+")")

	def getFromCID(self, CID):
		for x in self.Channels:
			if x.CID == CID:
				return x
		return False
			
class Channel():
	def __init__(self, name, desc, cid):
		self.name=name
		self.desc=desc
		self.CID=cid
		self.members=[]

	def sendMessage(self, fromuid, mesg):
		for x in self.members:
			try:
				shared.PlayerManager.getFromUID(x).Protocol.sendMethod(3, "SA", [str(fromuid), str(self.CID), mesg])
			except:
				self.members.remove(x)
				print_exc()

	def broadcast(self, method, data):
		for x in self.members:
			try:
				shared.PlayerManager.getFromUID(x).Protocol.sendMethod(3, method, data)
			except:
				self.members.remove(x)
				print_exc()