#Serverside chat
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
			self.Channels[cid].members.append(uid)
		else:
			print("Member "+str(uid)+" already in channel "+str(cid)+"!")

	def SA(self, cid, mesg, Protocol=None):
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