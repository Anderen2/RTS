#Worldmodule - Pathfinding
#Module for finding the best path through the world towards a world point.

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
		print(str(xzd))
		src=(xzd[0], xzd[1])
		dist=xzd[2]

ConsoleFriendly(0, 0, 20, 30, 1)