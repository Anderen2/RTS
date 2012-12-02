#socketServ - Sockets based server

from engine import debug, shared
from engine.shared import DPrint
from engine.Server import socketClient as client
from threading import Thread
import socket

class Server(Thread):
	def __init__(self, ip, port):
		#PreInit
		Thread.__init__(self)
		self.IP=ip
		self.PORT=port
		self.setName(self.IP+":"+str(self.PORT)) #Set Thread name
		self.CList=[] #Client List
		self.Conn=0 #Total connections since startup

	def Init(self):
		#Initialization
		serverSock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
		serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		serverSock.bind ( ( self.IP, self.PORT ) )
		serverSock.settimeout(1)
		serverSock.listen(5)

		self.alive=True
		self.start() #Begin accepting/running

	def run(self):
		#Run!
		while self.alive:
			try:
				channel, details = serverSock.accept()
				DPrint("Server", 1, "Client Connected: "+str(details))
				self.Conn+=1
				CList[self.Conn]=(client.Client(channel, details, self.Conn))
				CList[self.Conn].state="Starting"
				CList[self.Conn].start()
				CList[self.Conn].setName(details)

			except socket.timeout:
				pass

	def rmClient(self, ID):
		DPrint("Server", 0, "Client removed: "+str(ID)+" "+str(CList[ID].DETAILS))
		CList[ID].pop()

	def Broadcast(self, msg):
		for client in CList:
			client.send("ASDGFASgF")