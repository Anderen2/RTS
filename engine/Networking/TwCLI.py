#TwistedCLI
from traceback import print_exc
from twisted.internet import stdio
from twisted.protocols.basic import LineReceiver
from string import split
from engine import shared

class CLIIO(LineReceiver):
	from os import linesep as delimiter
	def __init__(self, factory):
		self.factory=factory
	def connectionMade(self):
		print("CLIIO Initialized")
	def lineReceived(self, line):
		try:
			Foo=split(line, ".")
			Bar=split(Foo[1], "-")
			
			obj=Foo[0]
			method=Bar[0]
			arg=split(Bar[1], "/")
			print("Object: " + obj + "\nMethod: " + method + "\nArguments: " + str(arg))

			obj=int(obj)
			method=str(method)
			arg=list(arg)

			shared.objectManager.runMethod(self, obj, method, arg)
		except:
			print("Invalid syntax")
			print_exc()

	def sendData(self, data):
		print(data)

	def sendMethod(self, obj, func, arg):
		try:
			args="/".join(arg)
			method=str(obj)+"."+str(func)+"-"+args
			self.transport.write(method)
		except:
			print_exc()
			return 1

class CLIFactory():
	def __init__(self):
		stdio.StandardIO(CLIIO(self))