#Shared Gamemanager
from engine import shared, debug

if shared.side == "Server":
	from engine.Game.gamemodes import sv_basegame
elif shared.side == "Client":
	from engine.Game.gamemodes import cl_basegame

class cl_Gamemanager():
	def __init__(self):
		shared.objectManager.addEntry(0,7,self)
		debug.ACC("startgame", self.requestStart, info="Starts the gamemode", args=0)

		self.Gamemode = None

	def requestStart(self):
		shared.protocol.sendMethod(7, "reqStart", [])

	def net_startGame(self, gID, Protocol=None):
		print("Server requested game start. Gamemode = "+str(gID))

		self.Gamemode = cl_basegame.BaseGame()

class sv_Gamemanager():
	def __init__(self):
		shared.objectManager.addEntry(0,7,self)

		self.Gamemode = None

	def reqStart(self, Protocol=None):
		shared.PlayerManager.Broadcast(7, "net_startGame", ["basegame"])
		self.Gamemode = sv_basegame.BaseGame()

