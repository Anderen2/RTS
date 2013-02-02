#TwistedServer
import pickle
from traceback import print_exc
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor, stdio
import TwCLI, sh_netObject, sh_netMethod

from engine import debug, shared

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
	def ConnectionMade(self, proto):
		pass

	def ConnectionLost(self, proto):
		pass

class Player():
	def __init__(self, name, ID):
		self.PlayerInfo={
		'name':name,
		'ID':ID,
		'country':"Norway",
		'faction':0,
		'team':0
		}

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
		pass


class Unit():
	pass

class UnitManager():
	pass

def Startup():
	shared.Server=Server()
	shared.Service=Service()
	cliFactory=TwCLI.CLIFactory()
	playerManager=PlayerManager()
	unitManager=UnitManager()

	reactor.listenTCP(1337, sh_netMethod.MethodFactory())
	reactor.run()
