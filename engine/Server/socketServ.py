#socketServ - Sockets based server

from engine import debug, shared
from engine.shared import DPrint
from engine.Server import socketClient as client
from engine.Networking import netResp, netCMD
from threading import Thread
from traceback import format_exc
from string import split
import socket

netResp.Init(1)
netCMD.Init(1)

EOC=chr(5) #EndOfCommand Seperator (ENQ Ascii) Used between Command and arguments
SOH=chr(1) #StartOfHeading Seperator (SOH Ascii) Used between arguments
STX=chr(2) #StartofTeXt Seperator (STX Ascii) Used to indicate that the rest of the package should be in Unicode
EOT=chr(4) #EndOfTransmission Seperator (EOT Ascii) Used to indicate that the transmission is complete
ETB=chr(23) #EndofTransmissionBlock Seperator (ETB Ascii) Used to indicate that the package is complete, but the transmission is not


class Server(Thread):
	def __init__(self, ip, port):
		#PreInit
		Thread.__init__(self)
		self.IP=ip
		self.PORT=port
		self.setName(self.IP+":"+str(self.PORT)) #Set Thread name
		self.CList={} #Client List
		self.Conn=0 #Total connections since startup

		debug.ACC("net_broadcast", self.svBroadcast, args=1, info="Broadcast data to all clients. Usage: \n net_broadcast message")
		debug.ACC("net_send", self.clSend, args=2, info="Send data to a client. Usage: \n net_send useruid message")
		debug.ACC("net_cs", self.clCS, args=-1, info="Send data to a client. Usage: \n net_cs uuid command message")

	def Init(self):
		#Initialization
		self.serverSock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM ) #Creating a TCP Socket. I know this is consuidered bad for many multiplayer games. But I'll concentrate about ingame optimalisations, instead of wrapping my head around building my own overhead for UDP
		self.serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.serverSock.bind ( ( self.IP, self.PORT ) )
		self.serverSock.settimeout(1)
		self.serverSock.listen(5)

		self.alive=True
		self.daemon=True
		self.start() #Begin accepting/running

	def run(self):
		#Run!
		while self.alive:
			try:
				channel, details = self.serverSock.accept()
				DPrint("Server", 1, "Client Connected: "+str(details))
				#self.CList.append(None)
				self.CList[self.Conn]=client.Client(channel, details, self.Conn)
				self.CList[self.Conn].daemon=True
				self.CList[self.Conn].state="Starting"
				self.CList[self.Conn].start()
				self.CList[self.Conn].setName(details)
				self.Conn+=1

			except socket.timeout:
				pass

	def rmClient(self, uid):
		DPrint("Server", 0, "Client removed: "+str(uid)+" "+str(self.CList[uid].DETAILS))
		del self.CList[uid]

	def svBroadcast(self, msg):
		for uidx in self.CList:
			self.CList[uidx].send(msg)

	def clSend(self, uid, msg):
		try:
			self.CList[int(uid)].send(msg)
		except:
			return format_exc()

	def clCS(self, uid, cmd, *args):
		# print(msg)
		# mesg="".join(msg)
		# args=split(mesg, " ")
		# print args
		self.CList[int(uid)].csend(cmd, args)

	def BroadcastSimple(self, msg):
		pass