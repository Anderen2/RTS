#Vehicle-Abstract / Steeringfunctions
from math import sqrt, acos, cos, sin, atan2, pi
from engine import shared, debug
from engine.Lib.hook import Hook

Vector = shared.Vector3D

class VehicleManager():
	def __init__(self):
		self.vehicles = []
		self.obstacles = []

	def create(self, pos):
		vehicle = Vehicle(pos)
		self.vehicles.append(vehicle)
		return vehicle

	def createObstacle(self, pos):
		obstacle = Obstacle(pos)
		self.obstacles.append(obstacle)
		return obstacle

	def getClosestTo(self, vehicle):
		a = vehicle.position

		closestveh = None
		closest = (0,0,0)
		closestdist = 99999

		for x in self.vehicles:
			b = x.position
			dist = tuple([x1-x2 for (x1,x2) in zip(a,b)])
			dist2 = (abs(dist[0]) + abs(dist[1]) + abs(dist[2]))
			if dist2 < closestdist:
				closestdist = dist2
				closestveh = x
				closest = b

		for x in self.obstacles:
			b = x.position
			dist = tuple([x1-x2 for (x1,x2) in zip(a,b)])
			dist2 = (abs(dist[0]) + abs(dist[1]) + abs(dist[2]))
			if dist2 < closestdist:
				closestdist = dist2
				closestveh = x
				closest = b

		return closestveh

	def lineIntersectsCircle(self, ahead, ahead2, obstacle):
		#the property "center" of the obstacle is a Vector3D.
		distance = sqrt((obstacle.position[0] - ahead.position[0])**2 + (obstacle.position[1] - ahead.position[1])**2)
		return distance <= obstacle.radius

shared.VehicleManager = VehicleManager()

class Obstacle():
	def __init__(self, pos):
		self.steerable = False
		self.position = Vector(pos)
		self.size = 10

class Vehicle():
	def __init__(self, pos):
		self.steerable = True
		self.position = Vector(pos)
		self.size = 10
		self.velocity = Vector()
		self.oldvelocity = Vector()
		self.max_velocity = 5 #Maximum acceleration
		self.max_force = 1 #Maximum steering force
		self.max_speed = 5 #Maximum speed
		self.mass = 100 #Vehicle mass (Affects steering abillity)
		self.breaking_force = 0.8
		self.arrive_breaking_radius = 100
		self.max_see_ahead = 50
		self.max_avoid_force = 10
		self.path_node_radius = 50

		self.path = []
		self._circlestate = None
		self._previous_path_node_radius = None

		#Hooks:
		self.Hook = Hook(self)
		self.Hook.new("OnPathStart", 1)
		self.Hook.new("OnPathAdded", 1)
		self.Hook.new("OnPathNext", 1)
		self.Hook.new("OnPathEnd", 1)

		self.Hook.new("OnStep", 1)
		self.Hook.new("OnBreaking", 1)
		self.Hook.new("OnStop", 1)


	def Stop(self):
		self.Hook.call("OnStop", self.velocity)
		self.velocity = Vector()
		print("Stopping!")

	def Break(self):
		self.Hook.call("OnBreaking", self.velocity)
		self.velocity = self.velocity * self.breaking_force
		if self.velocity.length()<0.1:
			self.Stop()
			return True

		# print("Breaking!")

	def towardsPos(self, target):
		# print("TowardsPos!")
		if type(target) != Vector:
			target = Vector(target)

		self.velocity = target - self.position
		self.velocity.normalize()
		self.velocity = self.velocity * self.max_velocity

	def seekPos(self, target):
		# print("seekPos!")
		if type(target) != Vector:
			target = Vector(target)

		self.desired_velocity = target - self.position
		self.desired_velocity.normalize()
		self.desired_velocity = self.desired_velocity * self.max_velocity
		#print("Desired : %s" % self.desired_velocity)

		self.steering = self.desired_velocity - self.velocity
		self.steering.truncate(self.max_force)
		#print("Steer1  : %s" % self.steering)
		self.steering = self.steering / self.mass
		#print("Steering: %s" % self.steering)

		self.velocity = self.velocity + self.steering
		
	def fleePos(self, target):
		# print("fleePos!")
		if type(target) != Vector:
			target = Vector(target)

		self.desired_velocity = self.position - target
		self.desired_velocity.normalize()
		self.desired_velocity = self.desired_velocity * self.max_velocity

		self.steering = self.desired_velocity - self.velocity
		self.steering.truncate(self.max_force)
		self.steering = self.steering / self.mass

		self.velocity = self.velocity + self.steering

	def arrivePos(self, target):
		# print("arrivePos!")
		if type(target) != Vector:
			target = Vector(target)

		self.desired_velocity = target - self.position
		#self.desired_velocity.normalize()

		distance = self.desired_velocity.length()
		print("Distance: %s" % distance)

		if distance < self.arrive_breaking_radius:
			self.desired_velocity.normalize()
			self.desired_velocity = self.desired_velocity * self.max_velocity * (float(distance) / self.arrive_breaking_radius)
			#self.desired_velocity = Vector()
			print("BreakVel: %s" % self.desired_velocity)

		else:
			self.desired_velocity.normalize()
			self.desired_velocity = self.desired_velocity * self.max_velocity

		self.steering = self.desired_velocity - self.velocity
		self.steering.truncate(self.max_force)
		self.steering = self.steering / self.mass

		self.velocity = self.velocity + self.steering

	def pursueVehicle(self, target):
		# print("pursueVehicle!")
		if type(target) != Vector:
			target = Vector(target)

		distance = (target.position - self.position).length()
		ticks = distance / self.max_velocity
		prediction = self.position + target.position * ticks

		self.arrivePos(prediction)

	def evadeVehicle(self, target):
		# print("evadeVehicle!")
		if type(target) != Vector:
			target = Vector(target)

		distance = (target.position - self.position).length()
		ticks = distance / self.max_velocity
		prediction = self.position + target.position * ticks

		self.fleePos(prediction)

	def avoidCollision(self):
		# print("avoidCollision!")
		## UNCOMPLETE!
		ahead = self.position + Vector(self.velocity.asTuple()).normalize() * self.max_see_ahead
		ahead2 = self.position + Vector(self.velocity.asTuple()).normalize() * (self.max_see_ahead * 0.5)

		closestObstacle = shared.VehicleManager.getClosestTo(self)
		avoidance_force = ahead - closestObstacle.position
		avoidance_force.normalize()
		avoidance_force = avoidance_force * self.max_avoid_force

	def seekToNode(self, target, towards=False):
		# print("seekToNode!")
		"""This is similar to seek, but its more natural looking than seek when operating with path-nodes"""
		"""This also returns True when the nodes radius is reached, promting the seeker to seek for the next node"""

		if type(target) != Vector:
			target = Vector(target)

		distance = (target - self.position).length()
		if distance < self.path_node_radius:
			return True

		# self.desired_velocity = target - self.position
		# self.desired_velocity.normalize()
		# self.desired_velocity = self.desired_velocity * self.max_velocity

		# self.steering = self.desired_velocity - self.velocity
		# self.steering.truncate(self.max_force)
		# self.steering = self.steering / self.mass

		# self.velocity = self.velocity + self.steering

		if not towards:
			self.seekPos(target)
		else: 
			self.towardsPos(target)

	def followPath(self, delta, towards=False):
		# print("followPath!")
		# towards = False
		# print "followPath"
		# print self.path
		if len(self.path)!=0:
			if self.seekToNode(self.path[0], towards):
				self.path.pop(0)
				print("Next: %f" % delta)

				try:
					self.Hook.call("OnPathNext", self.path[0])
				except:
					pass

		else:
			print("I am the one who knocks.")
			self.Hook.call("OnPathEnd", None)
			if not towards:
				self.Break()

		

	def followCircleAroundPoint(self, pos, radius, precicion=50):
		# print("followCircleAroundPoint!")
		# print(pos)
		centerpoint = Vector(pos)
		circleradius = radius

		if not self._circlestate:
			print (centerpoint - self.position).length()

		if (centerpoint - self.position).length() >= radius and not self._circlestate:
			print "We've reached the end of the circle, lets start moving around it"
			#We've reached the end of the circle, lets start moving around it
			difference = (centerpoint - self.position).asTuple()
			print difference
			circleRadian = atan2(difference[0], difference[2])
			print circleRadian
			x = centerpoint[0] + radius * cos(circleRadian)
			y = centerpoint[2] + radius * sin(circleRadian)
			self._circlestart = (x, self.position[1], y)
			print self._circlestart
			self._circlenext = self._circlestart
			self._circleradian = circleRadian
			self._circlestate = True
			self._previous_path_node_radius = self.path_node_radius
			self.path_node_radius = self.path_node_radius + precicion
			self.seekToNode(self._circlestart)

			print "="*10

		elif self._circlestate:
			if self.seekToNode(self._circlenext):
				dg = ((self._circleradian * 180) / pi) + precicion
				print "%d*" % dg
				if dg > 360:
					self._circleradian = (0 * (pi/180))

				else:
					self._circleradian = (dg * (pi/180))

				x = centerpoint[0] + radius * cos(self._circleradian)
				y = centerpoint[2] + radius * sin(self._circleradian)

				self._circlenext = (x, self.position[1], y)

				print self._circlenext

			
		else:
			#We have not reached the end of the circle yet. Keep current velocity. 
			self._circlestate = False

	def addPosToPath(self, pos):
		print("Target added! -------------------------------")
		print(pos)
		self.path.append(pos)
		print self.path
		self.Hook.call("OnPathAdded", pos)

	def clearPath(self):
		self.path = []

		print("clearPath!")

	def step(self, delta):
		self.Hook.call("OnStep", delta)
		
		self.velocity.truncate(self.max_speed)

		# if self.oldvelocity != Vector():
		# 	print acos( ( self.velocity.dotProduct(self.oldvelocity) ) / ( self.velocity.length()*self.oldvelocity.length() ) )

		self.oldvelocity = self.velocity
		self.position = self.position + (self.velocity*(delta*60))
		#print("Velocity: %s" % self.velocity)
		#print("Position: %s" % self.position)
		return self.position.asTuple()