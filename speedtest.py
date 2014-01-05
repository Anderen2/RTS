#Table lookup speed test

from random import randrange
from time import time

class Sample():
	def __init__(self):
		self.position=(randrange(0, 100),randrange(0, 100),randrange(0, 100))

Lookup = []
print("Creating lookuptable")
for x in xrange(10000):
	sc = Sample()
	Lookup.append(sc)

getclose = Sample()
a = getclose.position

print(getclose)
print(a)

closestveh = None
closest = (0,0,0)
closestdist = 9999

start = time()

for x in Lookup:
	b = x.position
	dist = tuple([x1-x2 for (x1,x2) in zip(a,b)])
	dist2 = (abs(dist[0]) + abs(dist[1]) + abs(dist[2]))
	if dist2 < closestdist:
		closestdist = dist2
		closestveh = x
		closest = b

print("Time taken: %s" % (time()-start))

print(closest)
print(closestdist)
print(closestveh)