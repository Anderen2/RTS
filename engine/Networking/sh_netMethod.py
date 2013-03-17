#MethodProtocol
from traceback import print_exc
from time import time
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from string import split
from engine import shared, debug

VERBOSE=True
PVERBOSE=False

class MethodProtocol(Protocol):
	def __init__(self, factory):
		DUMPDATA=False
		self.factory=factory
		self.player=None
		self.pingtime=0
		self.ping=0
		debug.ACC("net_senddata", self.sendData, "Send networked data", 1)
		debug.ACC("net_dumpdata", self.DataDump, "Dump networkdata to console\nTrue/False", 1)
		debug.ACC("net_sendmethod", self.sendMethodHuman, "Send networked method\nUsage: net_sendmethod object.function-arg1/arg2/arg3", 1)

	def DataDump(self, state):
		global VERBOSE
		if state=="True":
			VERBOSE=True
		else:
			VERBOSE=False

	def dataReceived(self, data):
		global VERBOSE
		#OBJECT.METHOD-ARG/ARG/ARG
		# chr 1^ chr 2^  chr 3^
		try:
			if data=="PONG":
				self.Pong()
				if PVERBOSE:
					print("Got Pong")
			elif data=="PING":
				self.Pingback()
				if PVERBOSE:
					print("Got Ping")
			else:
				Foo=split(data, chr(1))
				Bar=split(Foo[1], chr(2))
				
				obj=Foo[0]
				method=Bar[0]
				arg=split(Bar[1], chr(3))
				if VERBOSE:
					print("Object: " + obj + "\nMethod: " + method + "\nArguments: " + str(type(arg)))

				obj=int(obj)
				method=str(method)
				if arg!=[""]:
					arg=list(arg)
				else:
					arg=None

				shared.objectManager.runMethod(self, obj, method, arg)
		except:
			print_exc()

	def Ping(self):
		self.oldping=self.ping
		self.pingtime=time()
		self.sendData("PING")
		reactor.callLater(5, self.Timeout)

	def Pong(self):
		self.ping=time()-self.pingtime

	def Pingback(self):
		self.sendData("PONG")

	def Timeout(self):
		if self.ping==self.oldping:
			self.factory.ConnectionLost(self, "No Response")

	def sendData(self, data):
		self.transport.write(data)

	def sendMethodHuman(self, hummeth):
		Foo=split(hummeth, ".")
		obj=Foo[0]
		Bar=split(Foo[1], "-")
		func=Bar[0]
		
		try:
			args=split(Bar[1], "/")
			arg=chr(3).join(args)
		except:
			arg=""

		method=obj+chr(1)+func+chr(2)+arg
		if VERBOSE:
			print(method.replace(chr(1), ".").replace(chr(2), "-").replace(chr(3), "/"))
		self.transport.write(method)

	def sendMethod(self, obj, func, arg):
		try:
			if arg!=None:
				args=chr(3).join(arg)
			else:
				args=""

			method=str(obj)+chr(1)+str(func)+chr(2)+args
			if VERBOSE:
				print(split(method.replace(chr(1), ".").replace(chr(2), "-").replace(chr(3), "/"), "-")[0])
			self.transport.write(method)
		except:
			print_exc()
			return 1

class MethodFactory(Factory):
	protocol=MethodProtocol

	def __init__(self):
		print "Factory Initialized"

	def startedConnecting(self, connector):
		print("Connecting...")

	def buildProtocol(self, addr):
		print("Connected.")
		protocol=MethodProtocol(self)
		reactor.callLater(0.1, lambda: shared.Service.ConnectionMade(protocol))
		return protocol

	def clientConnectionLost(self, connector, reason):
		shared.DPrint("netMethod",2,"Lost connection: "+str(reason.getErrorMessage()))
		reactor.callLater(0.1, lambda: shared.Service.ConnectionLost(reason))

	def clientConnectionFailed(self, connector, reason):
		shared.DPrint("netMethod",2,"Failed connection: "+str(reason))
		reactor.callLater(0.1, lambda: shared.Service.ConnectionFailed(reason))

	def ConnectionLost(self, proto, reason):
		shared.DPrint("netMethod",2,"Lost connection: "+str(reason))
		reactor.callLater(0.1, lambda: shared.Service.ConnectionLost(proto, reason))