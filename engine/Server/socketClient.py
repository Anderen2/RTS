#socketClient - Sockets based client

from engine import debug, shared
from engine.Networking import sh_netcmd, sv_netcmd
from threading import Thread
from traceback import format_exc
import socket

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