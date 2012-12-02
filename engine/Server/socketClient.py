#socketClient - Sockets based client

from engine import debug, shared
from threading import Thread
from traceback import traceback.format_exc
import socket

class Client(Thread):
	def __init__(self, channel, details, ID):
		#PreInit
		Thread.__init__(self)
		self.clientSock=channel
		self.DETAILS=details
		self.ID=ID
		self.alive=True

	def Run(self):
		while self.alive:
			try:
				recv=self.clientSock.recv(1000)
				if not recv:
					shared.SocketServer.rmClient(self.ID)

			except socket.timeout:
				pass

			except:
				print traceback.format_exc()