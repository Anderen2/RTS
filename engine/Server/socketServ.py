#socketServ - Sockets based server

from engine import debug, shared
from engine.shared import DPrint
from engine.Server import socketClient as client
from threading import Thread
from traceback import format_exc
import socket

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
		debug.ACC("net_send", self.clSend, args=2, info="Send data to client. Usage: \n net_send userid message")

	def Init(self):
		#Initialization
		self.serverSock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM ) #Creating a TCP Socket. I know this is considered bad for many multiplayer games. But I'll concentrate about ingame optimalisations, instead of wrapping my head around building my own overhead for UDP
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

	def rmClient(self, ID):
		DPrint("Server", 0, "Client removed: "+str(ID)+" "+str(self.CList[ID].DETAILS))
		del self.CList[ID]

	def svBroadcast(self, msg):
		for idx, client in self.CList:
			client.send(msg)

	def clSend(self, ID, msg):
		try:
			self.CList[int(ID)].send(msg)
		except:
			return format_exc()

	def BroadcastSimple(self, msg):
		pass