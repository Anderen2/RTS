#TwistedClient
from traceback import print_exc
from string import split
from twisted.internet import reactor
from twisted.internet.defer import Deferred

from engine import shared, debug
from engine.Networking import sh_netObject, sh_netMethod
from engine.Networking.client import playermanager, unitmanager, groupmanager, chat

class Service():
	def __init__(self):
		shared.DPrint("Service", 0, "Initializing.")
		shared.Service=self
		sh_netObject.ObjectManager()
		shared.objectManager.addEntry(0,0,self)
		self.RetBackQueue={}
		self.Connected=False

	def Run(self):
		shared.DPrint("Service", 0, "Starting up reactor...")
		reactor.run()

	def cleanUp(self):
		shared.DPrint("Service", 0, "Cleaning up...")
		if self.Connected:
			shared.DPrint("Service", 0, "Disconnecting from reactor...")
			#reactor.disconnect()

	def Connect(self, ip, port):
		if not self.Connected:
			shared.DPrint("Service", 0, "Connecting to: "+str(ip)+":"+str(port))
			reactor.connectTCP(ip, port, sh_netMethod.MethodFactory(), 15)
			self.Connected=True
		else:
			shared.DPrint("Service", 0, "Tried to connect to: "+str(ip)+":"+str(port)+" but we are already connected to someone else!")

	def ConnectionMade(self, protocol):
		shared.DPrint("Service", 0, "A connection has been made")
		shared.protocol=protocol
		shared.Tjener=Tjener(protocol)

	def ConnectionLost(self, reason):
		shared.DPrint("Service", 2, "Connection was lost, Reason: "+str(reason))

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

class Tjener():
	def __init__(self, protocol):
		self.ServerInfo=None
		self.playercount=1
		shared.DPrint("Tjener", 0, "Pulling Serverinfo")

		debug.ACC("net_serverinfo", self.PrintNice, info="Prints serverinfo", args=0)

		protocol.sendMethod(1, "SI", [])
		shared.client.RetMeBack(self.GimmeServerInfo, "SI")

		shared.PlayerManager=playermanager.PlayerManager()
		shared.netUnitManager=unitmanager.UnitManager()
		groupmanager.GroupManager()
		shared.ChatManager=chat.ChatManager()

	def GimmeServerInfo(self, method, serverinfo):
		self.ServerInfo=serverinfo
		shared.DPrint("Tjener", 0, "Got serverinfo")

	def PrintNice(self):
		return ("""\nConnected to server: %s \n%s\nServer Location: %s / %s \nPlayers Connected: %d""" % (self.ServerInfo["name"], self.ServerInfo["desc"], self.ServerInfo["region"], self.ServerInfo["country"], self.playercount))

	
	