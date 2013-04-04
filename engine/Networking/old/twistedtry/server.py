#TwistedServer
import pickle
from traceback import print_exc
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor, stdio

from engine import debug, shared
import TwCLI, sh_netObject, sh_netMethod
from sv_netPlayer import Player

shared.objectManager=sh_netObject.ObjectManager()

#OBJECTS:
#0 = Server
#1 = Service
#1** = Players
#1**** = Units

INTERFACE="server"

class Server():
	def __init__(self):
		shared.objectManager.addEntry(0,0,self)
		self.ServerInfo={
		'name':"YARTS-Server",
		'desc':"Yet Another RTS Server",
		'region':'Europe',
		'country':'Norway'
		}

	def SI(self, Protocol=None):
		Protocol.sendMethod(1, "SI", [pickle.dumps(self.ServerInfo)])

class Service():
	def __init__(self):
		reactor.callLater(5, self.PingAll)
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

class PlayerManager():
	def __init__(self):
		shared.objectManager.addEntry(0, 1, self)
		self.Players={}
		self.Playern=0

	def sendMethodToAll(self, obj, func, arg):
		for x in self.Players:
			self.Players[x].protocol.sendMethod(obj, func, arg)

	#Network Responses
	def HI(self, name, Protocol=None):
		self.Playern+=1
		ply=Player(name, self.Playern, Protocol)
		self.sendMethodToAll(2, "NEW", [pickle.dumps(ply.getInfo())])
		#reactor.callLater(0.5, lambda: self.sendMethodToAll(1, "SI", [pickle.dumps(shared.Server.ServerInfo)])) Wtf were I even thinking here?
		self.Players[self.Playern]=ply
		print("Shook hands with: "+name)
		Protocol.player=ply
		Protocol.sendMethod(0, "HI", [str(self.Playern)])

	def PL(self, Protocol=None):
		FooList=[]
		for x in self.Players:
			FooList.append(self.Players[x].PlayerInfo)
		Protocol.sendMethod(1, "PL", [pickle.dumps(FooList)])

	def DCONN(self, Protocol=None):
		shared.DPrint("PlayerManager", 1, "Player: "+str(Protocol.player.ID)+" disconnected")
		del self.Players[Protocol.player.ID]

def Startup():
	shared.Server=Server()
	shared.Service=Service()
	cliFactory=TwCLI.CLIFactory()
	shared.playerManager=PlayerManager()

	reactor.listenTCP(1337, sh_netMethod.MethodFactory())
	reactor.run()
