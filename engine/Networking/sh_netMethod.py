#MethodProtocol
from traceback import print_exc
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from string import split
from engine import shared

VERBOSE=False

class MethodProtocol(Protocol):
	def __init__(self, factory):
		self.factory=factory
		self.player=None

	def dataReceived(self, data):
		#OBJECT.METHOD-ARG/ARG/ARG
		# chr 1^ chr 2^  chr 3^
		try:
			Foo=split(data, chr(1))
			Bar=split(Foo[1], chr(2))
			
			obj=Foo[0]
			method=Bar[0]
			arg=split(Bar[1], chr(3))
			if VERBOSE:
				print("Object: " + obj + "\nMethod: " + method + "\nArguments: " + str(arg))

			obj=int(obj)
			method=str(method)
			if arg!=[""]:
				arg=list(arg)
			else:
				arg=None

			shared.objectManager.runMethod(self, obj, method, arg)
		except:
			print_exc()

	def sendData(self, data):
		self.transport.write(data)

	def sendMethod(self, obj, func, arg):
		try:
			if arg!=None:
				args=chr(3).join(arg)
			else:
				args=""

			method=str(obj)+chr(1)+str(func)+chr(2)+args
			if VERBOSE:
				print(method)
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
		print("Lost connection: ", reason)
		reactor.callLater(0.1, lambda: shared.Service.ConnectionLost(protocol))

	def clientConnectionFailed(self, connector, reason):
		print("Failed connection: ", reason)