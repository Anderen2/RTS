#Networking - Client
import socket
from threading import Thread
from engine.Networking import netent, netResp, netCMD
from engine import shared, debug
from engine.shared import DPrint
from string import split

netResp.Init(2)
netCMD.Init(2)

EOC=chr(5) #EndOfCommand Seperator (ENQ Ascii) Used between Command and arguments
SOH=chr(1) #StartOfHeading Seperator (SOH Ascii) Used between arguments
STX=chr(2) #StartofTeXt Seperator (STX Ascii) Used to indicate that the rest of the package should be in Unicode
EOT=chr(4) #EndOfTransmission Seperator (EOT Ascii) Used to indicate that the transmission is complete
ETB=chr(23) #EndofTransmissionBlock Seperator (ETB Ascii) Used to indicate that the package is complete, but the transmission is not


class Client(Thread):
	def __init__(self):
		#Pre Init
		Thread.__init__(self)
		self.Sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
		self.Sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		debug.ACC("net_connect", self.Init, args=2, info="Connect to an server, Usage: \n net_connect IP PORT")
		debug.ACC("net_disconnect", self.Disconnect, args=0, info="Disconnect from the currently connected server")
		debug.ACC("net_say", self.chatSay, args=1, info="Say something!")
		debug.ACC("net_send", self.netSend, args=1, info="Send data to the server")
		debug.ACC("net_ping", self.netPing, info="Get network latency")
	
	def Init(self, IP, PORT):
		try:
			self.Sock.connect((str(IP),int(PORT)))
		except socket.error, e:
			DPrint("NET", 3, e)
			return str(e)

		#Start Running!
		self.alive=True
		self.daemon=True
		self.start()
		return "Success"

	def Disconnect(self):
		self.alive=False
		self.Sock.close()

	def netSend(self, msg):
		DPrint("NET", 0, "Sending: "+str(msg))
		self.Sock.send(msg)

	def netPing(self):
		pass

	def chatSay(self, msg):
		DPrint("NET", 0, "Saying: "+str(msg))

	def run(self):
		DPrint("NET", 0, "RUNNING")
		while self.alive:
			recv=self.Sock.recv(1000)

			if self.alive:
				if not recv:
					DPrint("NET", 2, "Server unexpectedly closed connection!")

				else:
					if recv[len(recv)-1]==EOT:
						recv=recv[0:len(recv)-1]
						#got the whole transmission
						ComPAR=split(recv, EOC)
						print ComPAR
						CMD=ComPAR[0]
						PAR=split(ComPAR[1], SOH)
						DPrint("rNET", 0, "Got Data!")
						DPrint("rNET", 0, recv)
						DPrint("rNET", 0, CMD)
						DPrint("rNET", 0, PAR)
						
					else:
						DPrint("rNET", 0, "transmission not complete, waiting..")
						DPrint("rNET", 0, recv)
					# else:
					# 	DPrint("NET", 2, "Undefined response: "+recv)