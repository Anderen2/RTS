#TwistedServer v2
import pickle

from engine import debug, shared
from engine.Networking import TwCLI, sh_netObject, sh_netMethod
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor, stdio
from traceback import print_exc

class Service():
	def __init__(self):
		#reactor.callLater(5, self.PingAll)
		self.connections=[]

	def ConnectionMade(self, proto):
		self.connections.append(proto)

	def ConnectionLost(self, proto, reason):
		shared.DPrint("Service", 1, "Connection to client lost: "+reason)
		try:
			shared.playerManager.DCONN(proto)
			self.connections.remove(proto)
		except KeyError:
			shared.DPrint("Service", 1, "Client not exsisting!")
		#proto.loseConnection()

	def PingAll(self):
		for x in self.connections:
			x.Ping()
			try:
				shared.DPrint("Service", 0, x.player.name+": "+str(x.ping))
			except:
				shared.DPrint("Service", 0, "UNINITIALIZED"+": "+str(x.ping))
		reactor.callLater(5, self.PingAll)

	def Broadcast(self, obj, method, args):
		for x in self.connections:
			x.sendMethod(obj, method, args)

class Server():
	def __init__(self):
		shared.objectManager.addEntry(0,1,self)
		self.ServerInfo={
		'name':"YARTS-Server",
		'desc':"Yet Another RTS Server",
		'region':'Europe',
		'country':'Norway'
		}

	def SI(self, Protocol):
		return (pickle.dumps(self.ServerInfo))

class PlayerManager():
	def __init__(self):
		shared.PlayerManager=self
		shared.objectManager.addEntry(0,2, self)
		self.PlayerCount=0
		self.PDict={}

	def HI(self, Username, PickledExtras, Protocol=None):
		if not self.getFromProto(Protocol):
			self.PlayerCount+=1
			self.Broadcast(2, "HI", [Username, str(self.PlayerCount), PickledExtras])
			self.PDict[self.PlayerCount]=Player(self.PlayerCount, Username, Protocol, PickledExtras)
			Protocol.sendMethod(2, "HI", [str(self.PlayerCount)])
		else:
			Protocol.sendMethod(3, "SA", ["-1", "0", "You are already in the game."])

	def LP(self, Protocol=None):
		foolist=[]
		for x in self.PDict:
			foolist.append({"uid":self.PDict[x].UID, "username":self.PDict[x].username, "info":self.PDict[x].PlayerInfo})

		Protocol.sendMethod(2, "LP", pickle.dumps(foolist))

	def Broadcast(self, obj, method, args):
		for x in self.PDict:
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

class Player():
	def __init__(self, UID, Username, Protocol, PickledExtras):
		#self.PlayerInfo=pickle.loads(PickledExtras)
		self.PlayerInfo={"Land":"Of the dead"}
		self.UID=UID
		self.username=Username
		self.Protocol=Protocol
		shared.ChatManager.addMember(self.UID, 1)

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


def Startup():
	shared.Server=Server()
	cliFactory=TwCLI.CLIFactory()

	ChatManager()

	reactor.listenTCP(1337, sh_netMethod.MethodFactory())
	reactor.run()