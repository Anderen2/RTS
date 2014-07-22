#BaseGame - Serverside
#This is the class which all gamemodes derive and bases itself on

from engine import shared, debug
from engine.Lib.hook import Hook

class BaseGame():
	def __init__(self):
		print("BaseGame Init")
		shared.ChatManager.systemSay("The game is about to start!")

	def _playerJoin(self):
		pass

	def _playerReqUnit(self, ply, unit):
		unitcost = unit.COST
		return True

	def _unitDestroyed(self, unit):
		pass

	def _startGame(self):
		pass