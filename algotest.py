from time import sleep
from engine import shared
from engine.shared import Vector
from engine.World import posalgo, pathfinding, movetypes

def run():
	shared.Pathfinder = pathfinding
	target = (672.6337432861328, 150.00076295109483, 189.78003407655163)
	newpos = (82.22440251298826, 205.77553978789962, 160.34340858459473)
	dist = 20

	while True:
		#target = Vector(target)+Vector(0, 10, 1)
		sleep(0.001)
		print("\ttarget: "+str(target))
		print(newpos)
		simdist, newpos = movetypes.Move(newpos, target, 1, 0)
		print(str(simdist)+"<"+str(dist))
		if (simdist)<dist:
			break