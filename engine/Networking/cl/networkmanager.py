#NetworkManager
from engine import debug, shared
from twisted.internet import reactor

class NetworkManager():
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