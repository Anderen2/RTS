#Clientside Chatmanager
import pickle
from engine import shared, debug

class ChatManager():
	def __init__(self):
		shared.ChatManager=self
		shared.objectManager.addEntry(0,3, self)

		self.channels=[]

		debug.ACC("net_say", self.ChatSay, info="Say something in chat\nUsage: net_say channel message", args=2)

	def SA(self, fromuid, cid, message, Protocol=None):
		username = shared.PlayerManager.getFromUID(fromuid)
		if username != False:
			username = username.username

		self.getFromCID(cid).Message(username, message)

	def AC(self, cid, channelname, desc, members, Protocol=None):
		"""AddChannel: We got added to a channel"""
		shared.DPrint("Chat", 1, "Added to channel: ["+str(cid)+"] "+channelname)
		self.channels.append(Channel(channelname, desc, int(cid), members=members))

	def NCU(self, cid, uid, Protocol=None):
		"""NewChannelUser: An new player got added to one of your channels"""
		shared.DPrint("Chat", 1, "Player: "+str(uid)+" added to channel: ["+str(cid)+"] ")
		self.getFromCID(cid).addMember(uid)

	def LC(self, channels, Protocol=None):
		"""ListChannels: Got Channel-list"""
		for CID, attr in channels.iteritems():
			self.channels.append(Channel(attr[0], attr[1], int(CID), members=attr[2]))

	def ChatSay(self, channel, mesg):
		shared.protocol.sendMethod(3, "SA", [channel, str(mesg)])

	def getFromCID(self, CID):
		for x in self.channels:
			if x.CID == int(CID):
				return x
		return False

class Channel():
	def __init__(self, name, desc, cid, members=[]):
		self.name = name
		self.desc = desc
		self.CID = cid
		self.members = []
		self.chatlog = []
		self.chatstring = ""

	def addMember(self, uid):
		self.members.append(uid)

	def Message(self, username, message):
		shared.DPrint("Chat", 1, "["+str(self.CID)+"] "+str(username)+": "+message)
		self.chatlog.append((username, message))
		self.chatstring = self.chatstring + str(username) + ": "+str(message)+"\n"
		shared.gui['chat'].setChatLog(self.chatstring)