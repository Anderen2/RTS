#MoveEff
#Unit/Entity movement effects

from time import time
from engine import shared, debug
from twisted.internet import reactor
import ogre.renderer.OGRE as ogre

def globDiveDie(Entity, delta):
	#CurrentPos = Entity.GetPosition()
	Altitude = Entity.getAltitude()
	print(Altitude)
	#print Altitude
	if Altitude!=None:
		if Altitude>5:
			speedinc = 1*delta
			altspeed = 3*delta
			rotspeed = (3000/Altitude)*delta
			MovementDirection = Entity.lastMovementDirection
			#print(MovementDirection)
			Entity.Translate(MovementDirection[0]+speedinc, MovementDirection[1]-altspeed, MovementDirection[2]+speedinc)
			Entity.node.pitch(ogre.Degree(rotspeed))
			return False
	return True

# def globPlaneCircle(Entity, delta):
	# speed = 150 #Forward momentumvelocity
	# time = 1 #Turnrate/Time/ 
	# testrad = 100

	# MovementDirection = Entity.lastMovementDirection
	# Position = Entity.GetPosition()

	# try:
	# 	if not Entity.__globPlaneCircleDir:
	# 		Entity.__globPlaneCircleDir = Position

	# 	else:
	# 		if (shared.Vector3D(Position) - shared.Vector3D(__globPlaneCircleDir)).length() > testrad:


	# except:
	# 	Entity.__globPlaneCircleDir = Position



	# self.GetEntity().node.rotate((0,1,0), ogre.Radian(float(time)/float(testrad)))
	# self.GetEntity().node.translate(self.GetEntity().node.getOrientation() * (0,1,speed) * delta)