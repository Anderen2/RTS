#TwistedServer
import pickle
from traceback import print_exc
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor, stdio

from engine import debug, shared
import TwCLI, sh_netObject, sh_netMethod
from sv_netPlayer import Player

shared.objectManager=sh_netObject.ObjectManager()

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
		shared.playerManager.DCONN(proto)
		self.connections.remove(proto)

	def PingAll(self):
		for x in self.connections:
			x.Ping()
			reactor.callLater(2, lambda: shared.DPrint("Service", 0, x.player.name+": "+str(x.ping)))
		reactor.callLater(5, self.PingAll)

class PlayerManager():
	def __init__(self):
		shared.objectManager.addEntry(0, 1, self)
		self.Players={}
		self.Playern=0

	#Network Responses
	def HI(self, name, Protocol=None):
		self.Playern+=1
		ply=Player(name, self.Playern)
		self.Players[self.Playern]=ply
		print("Shook hands with: "+name)
		shared.objectManager.addEntry(100, self.Playern, ply)
		Protocol.player=ply
		Protocol.sendMethod(2, "HI", [str(self.Playern)])

	def PL(self, Protocol=None):
		FooList=[]
		for x in self.Players:
			FooList.append(self.Players[x].PlayerInfo)
		Protocol.sendMethod(1, "PL", [pickle.dumps(FooList)])

	def DCONN(self, Protocol=None):
<<<<<<< HEAD
<<<<<<< HEAD
		shared.DPrint("PlayerManager", 1, "Player: "+str(Protocol.player.ID)+" disconnected")
=======
		shared.DPrint("PlayerManager", 1, "Player: "+Protocol.player.name+" disconnected")
>>>>>>> dd34fc3e589b68efcafaac9a17a710a19a2353cb
=======
		shared.DPrint("PlayerManager", 1, "Player: "+Protocol.player.name+" disconnected")
>>>>>>> parent of 6c61b62... Fixed various bugs
		del self.Players[Protocol.player.ID]


class Unit():
	pass

class UnitManager():
	pass

def Startup():
	shared.Server=Server()
	shared.Service=Service()
	cliFactory=TwCLI.CLIFactory()
	shared.playerManager=PlayerManager()
	unitManager=UnitManager()

	reactor.listenTCP(1337, sh_netMethod.MethodFactory())
	reactor.run()
