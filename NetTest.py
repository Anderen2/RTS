#NetworkingTester

from engine import shared, debug
from engine.Networking import client

NetClient=client.Client()

debug.RCC("net_connect localhost 13370")

while True:
	print(debug.RCC(raw_input("<<< ")))