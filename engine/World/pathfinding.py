#Worldmodule - Pathfinding
#Module for finding the best path through the world towards a world point.

from engine import shared, debug
from math import floor

class AB():
	def __init__(self):
		debug.ACC("path_ab_getnext", self.GetNextCoord, args=2, info="Get next point in the path")
		debug.ACC("path_ab_trace", self.ConsoleFriendly, args=5, info="Get a trace of the path from a point to a point. \nUsage: path_trace srcX srcZ dstX dstY trig")

	def GetNextCoord(self, src, dst):
		#Lazy ways ahoy!

		xRel = float(abs(float(dst[0])-float(src[0])))
		yRel = float(abs(float(dst[1])-float(src[1])))

		if xRel>yRel:
			xStep = 1
			#yStep = float((yRel/(xRel/yRel))/10)
			yStep = float(yRel/xRel)

		elif xRel<yRel:
			#xStep = float((xRel/(yRel/xRel))/10)
			xStep = float(xRel/yRel)
			yStep = 1

		else: 
			xStep = 1
			yStep = 1

		#print(xStep)
		#print(yStep)

		if dst[0]<src[0]:
			x=float(src[0])-xStep
		elif dst[0]>src[0]:
			x=float(src[0])+xStep
		else:
			x=dst[0]

		if dst[1]<src[1]:
			z=float(src[1])-yStep
		elif dst[1]>src[1]:
			z=float(src[1])+yStep
		else:
			z=dst[1]

		distance=abs((abs(src[0])+abs(src[1]))-(abs(dst[0])+abs(dst[1])))
		return (x,z,floor(distance))

	def ConsoleFriendly(self, x, z, x2, z2, trig):
		dist=999999
		src=(int(x), int(z))
		dst=(int(x2), int(z2))

		while dist>int(trig):
			xzd=self.GetNextCoord(src, dst)
			shared.DPrint("Pathfinding", 0, str(xzd))
			src=(xzd[0], xzd[1])
			dist=xzd[2]

	

class aStar():
	def __init__(self):
		pass

ABPath=AB()
aStarPath=aStar()