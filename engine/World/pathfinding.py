#Worldmodule - Pathfinding
#Module for finding the best path through the world towards a world point.

from engine import shared, debug
from math import floor, sqrt
import astar_grid, movetypes

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

		#distance=abs((abs(src[0])+abs(src[1]))-(abs(dst[0])+abs(dst[1]))) What the actual fuck were I thinking here..
		distance = sqrt((dst[0] - src[0])**2 + (dst[1] - src[1])**2)
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

		#distance=abs((abs(src[0])+abs(src[1])+abs(src[2]))-(abs(dst[0])+abs(dst[1])+abs(dst[2])))
		distance = sqrt((dst[0] - src[0])**2 + (dst[1] - src[1])**2 + (dst[2] - src[2])**2)
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
aStarPath=astar_grid.AStarGraph()
aStarPath.generateGraph(1500, 32)
aStarPath.generateSearchGrid()

def testDecoMove(decid, startx, starty, endx, endy):
	global deco
	global path

	deco = shared.decHandeler.Get(int(decid))
	start = (int(startx), int(starty))
	end = (int(endx), int(endy))

	print("Searching")
	path = aStarPath.Search2(start, end)
	print("Found Path.. Starting A>B Movement")
	shared.render.Hook.Add("OnRenderFrame", testDecoMove_Step)

def testDecoMove2(decid, endx, endy):
	global deco
	global path

	deco = shared.decHandeler.Get(int(decid))
	decostart = deco.entity.GetPosition()
	start = (decostart[0], decostart[2])
	end = (int(endx), int(endy))

	print("Searching")
	path = aStarPath.Search2(start, end)
	print("Found Path.. Starting A>B Movement")
	shared.render.Hook.Add("OnRenderFrame", testDecoMove_Step)

debug.ACC("a*_test", testDecoMove, args=5, info="Move decorator w/ a*\nUsage: decid startx starty endx endy")
debug.ACC("a*_test2", testDecoMove2, args=3, info="Move decorator relative to current pos w/ a*\nUsage: decid endx endy")

mtmove = False
dist = 0

def testDecoMove_Step(delta):
	global mtmove
	global deco
	global path
	global pathpos
	global newpos
	global dist

	if mtmove == False:
		if len(path)>0:
			try:
				pathpos = path.pop(0)
				print "pathpos %s | dist %d" % (str(pathpos), dist)
				mtmove = True
			except:
				shared.render.Hook.RM("OnRenderFrame", testDecoMove_Step)
				mtmove = False

				print("pathpos: Exception Caught")

		else:
			shared.render.Hook.RM("OnRenderFrame", testDecoMove_Step)
			mtmove = False

	dist, newpos = movetypes.Move(deco.entity.GetPosition(), pathpos, 1, 1)
	print "dist: %d - newpos: %s" % (dist, str(newpos))
	deco._setPos(newpos[0], newpos[1], newpos[2])
	if dist < 1:
		if len(pathpos)==0:
			shared.render.Hook.RM("OnRenderFrame", testDecoMove_Step)
			mtmove = False

		mtmove = False
