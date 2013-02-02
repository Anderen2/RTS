#TwistedClient
import pickle
from traceback import print_exc
from random import randrange
from string import split
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor, stdio
from twisted.internet.defer import Deferred

from engine import shared, debug
import sh_netObject, sh_netMethod, TwCLI
import cl_netPlayer, cl_netOPlayer

shared.objectManager=sh_netObject.ObjectManager()

INTERFACE="client"

class Service():
	def __init__(self):
		shared.objectManager.addEntry(0, 1, self)
		debug.ACC("net_serverinfo", self.PrintNice, "Show server information", 0)

	def ConnectionMade(self, proto):
		#Handshake
		proto.sendMethod(1, "HI", ["Anderen2"+str(randrange(0,100,1))])
		shared.DPrint("client",0,"Shaking hands with server")
		reactor.callLater(0.1, lambda: proto.sendMethod(1, "PL", None))
		reactor.callLater(0.2, lambda: proto.sendMethod(0, "SI", None))

	def ConnectionFailed(self, proto):
		shared.DPrint("client",2,"Connection Failed")
		reactor.stop()

	def PrintNice(self):
		return ("""\nConnected to server: %s \n%s\nServer Location: %s / %s \nPlayers Connected: %d""" % (self.ServerInfo["name"], self.ServerInfo["desc"], self.ServerInfo["region"], self.ServerInfo["country"], len(self.playerlist)))

	def PL(self, encoded, Protocol=None):
		self.playerlist=pickle.loads(encoded+".")
		shared.DPrint("client",1,"Got PlayerList")

	def SI(self, encoded, Protocol=None):
		self.ServerInfo=pickle.loads(encoded+".")
		shared.DPrint("client", 1, "Got ServerInfo")
		#shared.DPrint("client",1,self.ServerInfo)

class Unit():
	def __init__(self, ID, team, utype):
		print("I am alive!")
		self.ID=ID
		self.TEAM=team
		self.TYPE=utype

		self.pos=(10,0,30)
		self.rot=(30,10,0)
		self.NWP=None #Next Waypoint
		self.FM=None #Current Firemode
		self.HP=100

	def WP(self, x, y, z, Protocol=None):
		self.NWP=(x, y, z)
		print(str(self.ID)+" > ", self.NWP)

	def FG(self, x, y, z, Protocol=None):
		self.FM=(x, y, z)
		print("Firing gun at pos: ", self.FM)

	def FU(self, ID, Protocol=None):
		self.FM=ID
		print("Firing gun at ID: ", self.FM)

	def DMG(self, dmg, Protocol=None):
		self.HP=self.HP-int(dmg)
		print("HP LEFT: "+ str(self.HP))

	def TEST(self, string, Protocol=None):
		print(string)

class UnitManager():
	def __init__(self):
		self.clist=[]
		self.test="Hey!"
		shared.objectManager.addEntry(0, 3, self)

	def CU(self, team, type, Protocol=None):
		meth.sendData("ACK.UnitCreated")
		self.clist.append(Unit(len(self.clist), 1, 2))
		shared.objectManager.addEntry(1000, len(self.clist), self.clist[len(self.clist)-1])	

def Startup():
	shared.SelfPlayer=cl_netPlayer.Player()
	shared.Service=Service()
	#cliFactory=TwCLI.CLIFactory()
	unitManager=UnitManager()

	# print(shared.objectManager.getVarible(shared.objectManager.getEntryByClass("UnitManager"), "test"))
	# print(shared.objectManager.setVarible(2, "test", "fuckoff"))
	# print(shared.objectManager.getVarible(shared.objectManager.getEntryByClass("UnitManager"), "test"))

	reactor.connectTCP("localhost", 1337, sh_netMethod.MethodFactory(), 5)

def Run():
	reactor.run()

def cleanUp():
	pass
	#reactor.disconnect()