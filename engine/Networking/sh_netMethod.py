#MethodProtocol

import pickle, base64
from traceback import print_exc
from time import time
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.protocols import amp
from string import split
from engine import shared, debug

VERBOSE=True
PVERBOSE=True

class Method(amp.Command):
	arguments = [('obj', amp.Integer()),
				 ('func', amp.String()),
				 ('arg', amp.String())]
	response = [('retback', amp.String())]


class Ping(amp.Command):
	arguments = [('triptime', amp.Float())]
	response = [('triptime', amp.Float())]

class AMPMethod(amp.AMP):
	def __init__(self, factory):
		amp.AMP.__init__(self)
		self.factory=factory
		self.player=None

		self.OWPing = 0
		self.RAPing = 0
		self.AVGPing = 0

		self.maxretries = 3
		self.retries = 0

	#Recieve
	def method(self, obj, func, arg):
		print 'method'
		print (obj, func, arg)
		unpickledarg = pickle.loads(arg)
		shared.objectManager.runMethod(self, obj, func, unpickledarg)

		return {"retback": "Hello"}

	Method.responder(method)

	def ping(self, triptime):
		print("Got ping request")
		return {"triptime":time()}

	Ping.responder(ping)

	#Send
	def sendMethod(self, obj, func, arg):
		# print ("Sending:")
		# print (obj, func, arg)
		pickledarg = pickle.dumps(arg)
		d = self.callRemote(Method, obj=obj, func=func, arg=pickledarg)

		def errorMethod(reason):
			shared.DPrint("netMethod",2,"Error sending package: "+str(reason.getErrorMessage()))

		d.addErrback(errorMethod)

	def sendPing(self):
		d = self.callRemote(Ping, triptime=time())
		current_time = time()

		def returnPing(result):
			self.retries = 0
			self.OWPing = result["triptime"]-current_time
			self.RAPing = time() - current_time
			self.AVGPing = (self.AVGPing + self.RAPing) / 2

			print("One-Way Ping: %f" % (self.OWPing))
			print("Round-about Ping: %f" % (self.RAPing))
			print("Average Ping: %f" % (self.AVGPing))

		d.addCallback(returnPing)

		def errorPing(result):
			self.retries+=1
			self.AVGPing+=5

			if self.retries>self.maxretries:
				shared.Service.ConnectionLost(self, result)

		d.addErrback(errorPing)

	#Other
	def Frame(self):
		pass


class MethodFactory(Factory):
	protocol=AMPMethod

	def __init__(self):
		print "Factory Initialized"

	def startedConnecting(self, connector):
		print("Connecting...")

	def buildProtocol(self, addr):
		print("Connected.")
		protocol=AMPMethod(self)
		reactor.callLater(0, lambda: shared.Service.ConnectionMade(protocol))
		return protocol

	def clientConnectionLost(self, connector, reason):
		shared.DPrint("netMethod",2,"Lost connection: "+str(reason.getErrorMessage()))
		reactor.callLater(0, lambda: shared.Service.ConnectionLost(reason))

	def clientConnectionFailed(self, connector, reason):
		shared.DPrint("netMethod",2,"Failed connection: "+str(reason))
		reactor.callLater(0, lambda: shared.Service.ConnectionFailed(reason))

	def ConnectionLost(self, proto, reason):
		shared.DPrint("netMethod",2,"Lost connection: "+str(reason))
		reactor.callLater(0, lambda: shared.Service.ConnectionLost(proto, reason))