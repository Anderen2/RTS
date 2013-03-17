#TwistedServer v2
import pickle

from engine import debug, shared
from engine.Networking import TwCLI, sh_netObject, sh_netMethod

class Server():
	def __init__(self):
		shared.objectManager.addEntry(0,0,self)
		self.ServerInfo={
		'name':"YARTS-Server",
		'desc':"Yet Another RTS Server",
		'region':'Europe',
		'country':'Norway'
		}

	#Connection/Factory spesific functions
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

	#Global client functions
	def PingAll(self):
		for x in self.connections:
			x.Ping()
			try:
				shared.DPrint("Service", 0, x.player.name+": "+str(x.ping))
			except:
				shared.DPrint("Service", 0, "UNINITIALIZED"+": "+str(x.ping))
		reactor.callLater(5, self.PingAll)


	#Network Responses
	def SI(self, Protocol=None):
		Protocol.sendMethod(1, "SI", [pickle.dumps(self.ServerInfo)])

	def firstPlayer(self):


def Startup():
	shared.Server=Server()
	cliFactory=TwCLI.CLIFactory()

	reactor.listenTCP(1337, sh_netMethod.MethodFactory())
	reactor.run()