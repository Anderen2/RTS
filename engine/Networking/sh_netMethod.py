#MethodProtocol
import pickle, base64
from traceback import print_exc
from time import time
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from string import split
from engine import shared, debug

VERBOSE=True
PVERBOSE=True
RAWVERBOSE=False
RAWDECRYPT=False
QUEUEVERBOSE=False
HUMANOSE=False #Warning, this means that the server will read in Humanose form. It will break everything!
PHUMANOSE=False #Warning, this means that the server will transmit in Humanose form. It will break everything!

class MethodProtocol(Protocol):
	def __init__(self, factory):
		DUMPDATA=False
		self.factory=factory
		self.player=None
		self.pingtime=0
		self.ping=0
		self.queue=[]
		debug.ACC("net_senddata", self.sendData, "Send networked data", 1)
		debug.ACC("net_dumpdata", self.DataDump, "Dump networkdata to console\nTrue/False", 1)
		debug.ACC("net_sendmethod", self.sendMethodHuman, "Send networked method\nUsage: net_sendmethod object.function-arg1/arg2/arg3", 1)

		

		reactor.callLater(0, self.Frame)

	def DataDump(self, state):
		global VERBOSE
		if state=="True":
			VERBOSE=True
		else:
			VERBOSE=False

	def dataReceived(self, data):
		global VERBOSE
		global PVERBOSE
		global HUMANOSE
		global PHUMANOSE
		global RAWVERBOSE
		#OBJECT.METHOD-ARG/ARG/ARG
		# chr 1^ chr 2^  chr 3^
		if HUMANOSE:
			dot="."
			dash="-"
			slash="/"
		else:
			dot=chr(1)
			dash=chr(2)
			slash=chr(3)

		if PHUMANOSE:
			rdot="."
			rdash="-"
			rslash="/"
		else:
			rdot=chr(1)
			rdash=chr(2)
			rslash=chr(3)

		try:
			if HUMANOSE:
				data=split(data, "\n")[0]
			if data=="PONG":
				self.Pong()
				if PVERBOSE:
					print("Got Pong")
			elif data=="PING":
				self.Pingback()
				if PVERBOSE:
					print("Got Ping")
			else:
				Foo=split(data, dot)
				Bar=split(Foo[1], dash)
				
				obj=Foo[0]
				method=Bar[0]
				#print("Recived: "+Bar[1].replace(chr(3),"\n___\n"))
				#arg=split(Bar[1], slash)
				try:
					b64 = base64.b64decode(Bar[1])
					arg=pickle.loads(b64)
				except TypeError:
					print "\n\n\n\n\n\n\n"
					print("Got invalid package (Invalid Padding)\nTrying to reconstruct package.")
					print(Bar[1])
					print "\n\n\n\n\n\n\n"
					# if "==" in Bar[1]: #If padding exsists
					# 	if not "==" in Bar[1][len(Bar[1])-2:]: #But not at the end
					# 		try:
					# 			foo = Bar[1].split("==")

					# 			b64 = base64.b64decode(Bar[1])
					# 			arg=pickle.loads(b64)
					# 		except:
					# 			pass
					# 	if 

				if RAWVERBOSE:
					print("Recived: "+str(arg))
				if VERBOSE:
					print("\nRecieved:")
					print("Object: " + obj + "\nMethod: " + method + "\nArgument: " + str(type(arg)))
				if PVERBOSE:
					print("Arguments:\n"+str(arg))

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
		#Set TCP_NODELAY to keep TCP from hording our data
		self.transport.setTcpNoDelay(True)
		self.transport.write(data)

	def sendMethodHuman(self, hummeth):
		global VERBOSE, PHUMANOSE
		if PHUMANOSE:
			rdot="."
			rdash="-"
			rslash="/"
		else:
			rdot=chr(1)
			rdash=chr(2)
			rslash=chr(3)

		Foo=split(hummeth, ".")
		obj=Foo[0]
		Bar=split(Foo[1], "-")
		func=Bar[0]
		
		try:
			args=split(Bar[1], "/")
			arg=rslash.join(args)
		except:
			arg=""

		method=obj+rdot+func+rdash+arg
		if VERBOSE:
			print(method.replace(chr(1), ".").replace(chr(2), "-").replace(chr(3), "/"))
		self.transport.write(method)

	def txMeth(self, obj, func, arg):
		global VERBOSE, PHUMANOSE, RAWVERBOSE, RAWDECRYPT
		if PHUMANOSE:
			rdot="."
			rdash="-"
			rslash="/"
			rend="\n"
		else:
			rdot=chr(1)
			rdash=chr(2)
			rslash=chr(3)
			rend=""

		try:
			# args=""
			# if arg!=None:
			# 	if type(arg) is list:
			# 		for x in arg:
			# 			args=str(args)+str(x)+rslash
			# 		args=args[:len(args)-1]
			# 	else:
			# 		args=arg
			# else:
			# 	args=""

			prebaseargs = pickle.dumps(arg)
			args=base64.b64encode(prebaseargs)

			method=str(obj)+rdot+str(func)+rdash+args+rend
			if VERBOSE:
				print("\nTransmitting: ")
				print("Object: " + str(obj) + "\nMethod: " + str(func) + "\nArgument: " + str(type(arg)))
			if RAWVERBOSE:
				print(split(method.replace(chr(1), ".").replace(chr(2), "-").replace(chr(3), "/"), "-"))
				print method
			if RAWDECRYPT:
				print prebaseargs

			#Set TCP_NODELAY to keep TCP from hording our data
			self.transport.setTcpNoDelay(True)

			self.transport.write(method)
		except:
			print_exc()
			return 1

	def Frame(self):
		if len(self.queue)!=0:
			first=self.queue.pop(0)
			self.txMeth(first[0], first[1], first[2])
		reactor.callLater(0.05, self.Frame)

	def sendMethod(self, obj, func, arg):
		self.queue.append([obj, func, arg])

		if QUEUEVERBOSE:
			print("\nNetwork Queue:")
			for x in self.queue:
				print("\t"+str(x))
			print("\n")

class MethodFactory(Factory):
	protocol=MethodProtocol

	def __init__(self):
		print "Factory Initialized"

	def startedConnecting(self, connector):
		print("Connecting...")

	def buildProtocol(self, addr):
		print("Connected.")
		protocol=MethodProtocol(self)
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