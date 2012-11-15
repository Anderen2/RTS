#Worldmodule - Pathfinding
#Module for finding the best path through the world towards a world point.

from engine import shared, debug

# class Pathfinding():
# 	def __init__(self):
# 		#Load a pathfindingmap

# 	def GetNextCoord(self, src, dst):
# 		#Lazy ways ahoy!
# 		if dst[0]<0:
# 			x=src[0]-1
# 		else:
# 			x=src[0]+1

# 		if dst[1]<0:
# 			y=src[1]-1
# 		else:
# 			y=src[0]-1
# 		return (x,y)

def GetNextCoord(src, dst):
	#Lazy ways ahoy!
	if dst[0]<0:
		x=src[0]-1
	else:
		x=src[0]+1

	if dst[1]<0:
		y=src[1]-1
	else:
		y=src[0]-1

	distance=(abs(src[0])+abs(src[1]))-(abs(dst[0])+abs(dst[1]))
	return (x,y,distance)