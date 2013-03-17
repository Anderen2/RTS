#TwistedClient
import pickle
from traceback import print_exc
from string import split
from twisted.internet import reactor
from twisted.internet.defer import Deferred

# from engine import shared, debug
# import sh_netObject, sh_netMethod
# import cl_netPlayer, cl_netOPlayer

# shared.objectManager=sh_netObject.ObjectManager()

# #OBJECTS
# #0 = Self/Client/ThisPlayer/Me
# #1 = Service
# #2 = PlayerManager

# #1** = Other Players

# INTERFACE="client"

def Startup():
# 	shared.SelfPlayer=cl_netPlayer.Player()
# 	shared.Service=Service()
# 	shared.playerManager=PlayerManager()
# 	reactor.connectTCP("192.168.1.115", 1337, sh_netMethod.MethodFactory(), 15)
	pass

def Run():
	reactor.run()

def cleanUp():
	pass
	#reactor.disconnect()