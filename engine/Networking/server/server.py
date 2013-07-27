#TwistedServer v2
import pickle
from traceback import print_exc
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor, stdio
from engine import debug, shared
from engine.Networking import TwCLI, sh_netObject, sh_netMethod

from groupmanager import GroupManager
from playermanager import PlayerManager
from unitmanager import UnitManager
from chat import ChatManager

class Service():
	def __init__(self):
		shared.objectManager.addEntry(0, 0, self)
		self.RetBackQueue={}
		self.connections=[]

	def RetMeBack(self, function, method):
		self.RetBackQueue[method]=function

	def RetBack(self, *args):
		protocol=args[0]
		method=args[1]
		kwargs=args[1:]
		shared.DPrint("Service", 0, "Got a RetBack from method: "+method)
		if method in self.RetBackQueue:
			foo=self.RetBackQueue[method]
			del self.RetBackQueue[method]
			ret=foo(*kwargs)
			if ret!=None:
				return ret

	def ConnectionMade(self, proto):
		self.connections.append(proto)

	def ConnectionLost(self, proto, reason):
		shared.DPrint("Service", 1, "Connection to client lost: "+reason)
		try:
			shared.playerManager.DCONN(proto)
			self.connections.remove(proto)
		except KeyError:
			shared.DPrint("Service", 1, "Client does not exsist!")
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
		return ([self.ServerInfo])

def Startup():
	shared.Server=Server()

	ChatManager()
	UnitManager()
	GroupManager()

	reactor.listenTCP(1337, sh_netMethod.MethodFactory())
	reactor.run()