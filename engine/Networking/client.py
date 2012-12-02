#Networking - Client
import socket
from threading import Thread
from engine.Networking import netent, sh_netcmd, cl_netcmd
from engine import shared, debug
from engine.shared import DPrint

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
			DPrint("NET", 1, str(self.Sock.connect((str(IP),int(PORT)))))
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

	def chatSay(self, msg):
		DPrint("NET", 0, "Saying: "+str(msg))

	def run(self):
		DPrint("NET", 0, "RUNNING")
		while self.alive:
			DPrint("NET", 0, "TICK!")
			recv=self.Sock.recv(1000)
			DPrint("NET", 0, "TOCK!")

			if self.alive:
				if not recv:
					DPrint("NET", 2, "Server unexpectedly closed connection!")

				else:
					if recv=="PING":
						DPrint("NET", 0, "Ping recived, responding...")
						self.Sock.send("PING")

					else:
						DPrint("NET", 2, "Undefined response: "+recv)