#TwistedClient
import pickle
from traceback import print_exc
from string import split
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor, stdio
from twisted.internet.defer import Deferred

from engine import shared, debug
import sh_netObject, sh_netMethod, TwCLI
import cl_netPlayer, cl_netOPlayer

shared.objectManager=sh_netObject.ObjectManager()

#OBJECTS
#0 = Self/Client/ThisPlayer/Me
#1 = Service
#2 = PlayerManager

#1** = Other Players

INTERFACE="client"

class Service():
	def __init__(self):
		shared.objectManager.addEntry(0, 1, self)
		debug.ACC("net_serverinfo", self.PrintNice, "Show server information", 0)

	def ConnectionMade(self, proto):
		#Handshake
		proto.sendMethod(1, "HI", [shared.SelfPlayer.name])
		shared.DPrint("client",0,"Shaking hands with server")
		reactor.callLater(0.1, lambda: proto.sendMethod(1, "PL", None))
		reactor.callLater(0.2, lambda: proto.sendMethod(0, "SI", None))

	def ConnectionFailed(self, proto):
		shared.DPrint("client",2,"Connection Failed")
		reactor.stop()

	def ConnectionLost(self, proto):
		shared.DPrint("client",2,"Connection Closed Unexpectly")
		reactor.stop()

	def PrintNice(self):
		return ("""\nConnected to server: %s \n%s\nServer Location: %s / %s \nPlayers Connected: %d""" % (self.ServerInfo["name"], self.ServerInfo["desc"], self.ServerInfo["region"], self.ServerInfo["country"], self.playercount))

	def PL(self, encoded, Protocol=None):
		playerlist=pickle.loads(encoded)
		shared.DPrint("client",1,"Got PlayerList")
		self.playercount=len(playerlist)
		shared.playerManager.ImportPlayers(playerlist)

	def SI(self, encoded, Protocol=None):
		self.ServerInfo=pickle.loads(encoded)
		shared.DPrint("client", 1, "Got ServerInfo")

class PlayerManager():
	def __init__(self):
		shared.objectManager.addEntry(0, 2, self)

		self.players={}

	def ImportPlayers(self, playerlist):
		for x in playerlist:
			ply=cl_netOPlayer.Player(x)
			self.players[x["ID"]]=ply

	def NEW(self, encoded, Protocol=None):
		decoded=pickle.loads(encoded)
		ply=cl_netOPlayer.Player(decoded)
		shared.Service.playercount+=1
		self.players[decoded["ID"]]=ply

def Startup():
	shared.SelfPlayer=cl_netPlayer.Player()
	shared.Service=Service()
	shared.playerManager=PlayerManager()
	# print(shared.objectManager.getVarible(shared.objectManager.getEntryByClass("UnitManager"), "test"))
	# print(shared.objectManager.setVarible(2, "test", "fuckoff"))
	# print(shared.objectManager.getVarible(shared.objectManager.getEntryByClass("UnitManager"), "test"))

	reactor.connectTCP("192.168.1.115", 1337, sh_netMethod.MethodFactory(), 15)

def Run():
	reactor.run()

def cleanUp():
	pass
	#reactor.disconnect()