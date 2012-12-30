#socketClient - Sockets based client

from engine import debug, shared
from engine.Networking import netResp, netCMD
from threading import Thread
from traceback import format_exc
import socket

netResp.Init(1)
netCMD.Init(1)

EOC=chr(5) #EndOfCommand Seperator (ENQ Ascii) Used between Command and arguments
SOH=chr(1) #StartOfHeading Seperator (SOH Ascii) Used between arguments
STX=chr(2) #StartofTeXt Seperator (STX Ascii) Used to indicate that the rest of the package should be in Unicode
EOT=chr(4) #EndOfTransmission Seperator (EOT Ascii) Used to indicate that the transmission is complete
ETB=chr(23) #EndofTransmissionBlock Seperator (ETB Ascii) Used to indicate that the package is complete, but the transmission is not

class Client(Thread):
	def __init__(self, channel, details, ID):
		#PreInit
		Thread.__init__(self)
		self.Sock=channel
		self.DETAILS=details
		self.ID=ID
		self.alive=True

	def send(self, msg):
		self.Sock.send(msg)

	def csend(self, cmd, args):
		foo=""
		for x in args:
			if args.index(x)!=len(args)-1:
				foo=foo+x+SOH
			else:
				foo=foo+x+EOT
		bar=cmd+EOC+foo
		self.Sock.send(bar)

	def run(self):
		while self.alive:
			try:
				recv=self.Sock.recv(1000)
				if not recv:
					shared.SocketServer.rmClient(self.ID)
					self.alive=False
				shared.DPrint("client", 0, recv)

			except socket.timeout:
				pass

			except:
				shared.DPrint("client", 2, format_exc())