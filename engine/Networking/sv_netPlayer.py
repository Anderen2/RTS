#sv_netPlayer
from engine import shared, debug
class Player():
	def __init__(self, name, ID):
		self.name=name
		self.ID=ID
		self.PlayerInfo={
		'name':name,
		'ID':ID,
		'country':"Norway",
		'faction':0,
		'team':0
		}