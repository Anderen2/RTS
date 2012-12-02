#Dedicated Server - Main
from engine import shared, debug
from engine.Server import socketServ

shared.SocketServer=socketServ.Server("localhost", 13370)

shared.SocketServer.Init()