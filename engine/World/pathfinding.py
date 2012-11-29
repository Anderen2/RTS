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
	if dst[0]<src[0]:
		x=src[0]-1
	elif dst[0]>src[0]:
		x=src[0]+1
	else:
		x=dst[0]

	if dst[1]<src[1]:
		z=src[1]-1
	elif dst[1]>src[1]:
		z=src[1]+1
	else:
		z=dst[1]

	distance=abs((abs(src[0])+abs(src[1]))-(abs(dst[0])+abs(dst[1])))
	return (x,z,distance)

def ConsoleFriendly(x, z, x2, z2, trig):
	dist=999999
	src=(int(x), int(z))
	dst=(int(x2), int(z2))

	while dist>int(trig):
		xzd=GetNextCoord(src, dst)
		shared.DPrint("Pathfinding", 0, str(xzd))
		src=(xzd[0], xzd[1])
		dist=xzd[2]

debug.ACC("path_getnext", GetNextCoord, args=2, info="Get next point in the path")
debug.ACC("path_trace", ConsoleFriendly, args=5, info="Get a trace of the path from a point to a point. \nUsage: path_trace srcX srcZ dstX dstY trig")