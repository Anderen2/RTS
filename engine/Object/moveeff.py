#MoveEff
#Unit/Entity movement effects

from time import time
from engine import shared, debug
from twisted.internet import reactor
import ogre.renderer.OGRE as ogre

def globDiveDie(Entity, delta):
	#CurrentPos = Entity.GetPosition()
	Altitude = Entity.getAltitude()
	#print Altitude
	if Altitude!=None:
		if Altitude>5:
			speedinc = 1*delta
			altspeed = 10*delta
			rotspeed = (3000/Altitude)*delta
			MovementDirection = Entity.lastMovementDirection
			#print(MovementDirection)
			Entity.Translate(MovementDirection[0]+speedinc, MovementDirection[1]-altspeed, MovementDirection[2]+speedinc)
			Entity.node.pitch(ogre.Degree(rotspeed))
			return False
	return True