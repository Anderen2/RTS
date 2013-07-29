#Worldmodule - Pathfinding
#Module for finding the best path through the world towards a world point.

from engine import shared, debug
from math import floor

class AB():
	def __init__(self):
		debug.ACC("path_ab_getnext", self.GetNextCoord, args=2, info="Get next point in the path")
		debug.ACC("path_ab_trace", self.ConsoleFriendly, args=5, info="Get a trace of the path from a point to a point. \nUsage: path_trace srcX srcZ dstX dstY trig")

	def GetNextCoord(self, src, dst, speed):
		#Lazy ways ahoy!

		xRel = float(abs(float(dst[0])-float(src[0])))
		zRel = float(abs(float(dst[1])-float(src[1])))

		if xRel>zRel:
			xStep = 1*speed
			zStep = float(zRel/xRel)*speed

		elif xRel<zRel:
			xStep = float(xRel/zRel)*speed
			zStep = 1*speed

		else: 
			xStep = 1*speed
			zStep = 1*speed

		if dst[0]<src[0]:
			x=float(src[0])-xStep
		elif dst[0]>src[0]:
			x=float(src[0])+xStep
		else:
			x=dst[0]

		if dst[1]<src[1]:
			y=float(src[1])-zStep
		elif dst[1]>src[1]:
			y=float(src[1])+zStep
		else:
			y=dst[1]

		distance=abs((abs(src[0])+abs(src[1]))-(abs(dst[0])+abs(dst[1])))
		return (x,y,floor(distance))

	def GetNextCoord3D(self, src, dst, speed):
		#Lazy ways ahoy!

		xRel = float(abs(float(dst[0])-float(src[0])))
		yRel = float(abs(float(dst[1])-float(src[1])))
		zRel = float(abs(float(dst[2])-float(src[2])))

		if xRel>zRel:
			xStep = 1*speed
			zStep = float(zRel/xRel)*speed

		elif xRel<zRel:
			xStep = float(xRel/zRel)*speed
			zStep = 1*speed

		else: 
			xStep = 1*speed
			zStep = 1*speed

		if src[1]>dst[1]: #If target is lower
			if src[1]-dst[1]<2:
				y=dst[1]
			else:
				yStep = float(0.5)*speed
				y=src[1]-yStep
		else:
			if dst[1]-src[1]<2:
				y=dst[1]
			else:
				yStep = float(0.5)*speed
				y=src[1]+yStep

		if dst[0]<src[0]:
			x=float(src[0])-xStep
		elif dst[0]>src[0]:
			x=float(src[0])+xStep
		else:
			x=dst[0]

		if dst[2]<src[2]:
			z=float(src[2])-zStep
		elif dst[2]>src[2]:
			z=float(src[2])+zStep
		else:
			z=dst[2]

		distance=abs((abs(src[0])+abs(src[1])+abs(src[2]))-(abs(dst[0])+abs(dst[1])+abs(dst[2])))
		return (x,y,z,floor(distance))

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