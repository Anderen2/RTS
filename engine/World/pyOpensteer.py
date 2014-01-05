"""          ----------------------------------------------------------------------------


     OpenSteer -- Steering Behaviors for Autonomous Characters

     Copyright (c) 2002-2003, Sony Computer Entertainment America
     Original author: Craig Reynolds <craig_reynolds@playstation.sony.com>

     Permission is hereby granted, free of charge, to any person obtaining a
     copy of this software and associated documentation files (the "Software"),
     to deal in the Software without restriction, including without limitation
     the rights to use, copy, modify, merge, publish, distribute, sublicense,
     and/or sell copies of the Software, and to permit persons to whom the
     Software is furnished to do so, subject to the following conditions:

     The above copyright notice and this permission notice shall be included in
     all copies or substantial portions of the Software.

     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
     THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
     FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
     DEALINGS IN THE SOFTWARE.

    Porting by Serge Besnard (serge [at] petiteappli [dot] com)
    Initally based on another port opensteerdotnet by handcircus, hosted by
    sourceforge

     ----------------------------------------------------------------------------
    """
from math import sqrt,pow
from random import random
import logging

class Vector3D:
    """ a stripped out class for 3D vectors"""
    
    __class__="Vector3D"
    
    def __mul__(self,s):
        """Returns a Vector3D result of multiplication by scalar s"""
        
        return Vector3D(tuple([x*s for x in self.V]))
    def __div__(self,s):
        """Returns a Vector3D result of multiplication by scalar s"""
        if not s==0 :
            return Vector3D([x/s for x in self.V])
        #ERROR DIVISION BY ZERO
        #Doesn't anyone has the time to write an exception throw ? I don't have the experience...
        return Vector3D.ZERO
    
    def __add__(self,A):
        return Vector3D(tuple([x1+x2 for (x1,x2) in zip(self.V,A)])) 
    
    def __sub__(self,A):
        return Vector3D(tuple([x1-x2 for (x1,x2) in zip(self.V,A)])) 
    
            
    def __init__(self, v=(0.,0.,0.)):
        self.V=tuple([v[i] for i in range(3)])


    
        
    def __cmp__(self,v):
        return cmp(self.V,v.asTuple())
    def __iter__(self):
        return self.V.__iter__()
    
    

    
    def __eq__(self,v):
        if (self.V==tuple(v)):
            return True
        return False
        
    def asTuple(self):
        return self.V

    def __getitem__(self,i):
        return self.V[i]
        
    def dotProduct(self, b):
        """simple dot product function"""
        return sum([x1*x2 for (x1,x2) in zip(self.V,b)])
        #return sum([self.V[i]*b[i] for i in range(3)])
    
    def length(self):
        return sqrt(sum([x*x for x in self.V]))
    
    def normalize(self):
        fLength =  self.length()
        if fLength > 1e-08 :
            fInvLength = 1.0 / fLength
            self.V=tuple([x*fInvLength for x in self.V])
            return fLength
        return 0
    
    def crossProduct(self,V):
        
        return Vector3D(tuple([self.V[1] * V[2] - self.V[2] * V[1],\
                        self.V[2] * V[0] - self.V[0] * V[2],\
                        self.V[0] * V[1] - self.V[1] * V[0]]))
    
    def __str__(self):
        return "Vector3D"+str(self.V)   

class Utilities:
    
    def parallelComponent (self, source, unitBasis):
        projection = source.dotProduct(unitBasis)
        return unitBasis * projection
    
    def clip(self,  x,  min,  max):
        
            if (x < min) : return min
            if (x > max) : return max
            return x
    
    def perpendicularComponent (self, source, unitBasis):
        """return component of vector perpendicular to a unit basis vector
        (IMPORTANT NOTE: assumes "basis" has unit magnitude (length==1))"""
        return source - Utilities().parallelComponent(source,unitBasis)
    
    def interpolate(self, alpha, x0, x1):
        return x0 + ((x1 - x0) * alpha)
    
    def limitMaxDeviationAngle (self, source,cosineOfConeAngle,basis):
        
        return Utilities().vecLimitDeviationAngleUtility (True, source, cosineOfConeAngle,basis)
    
    def vecLimitDeviationAngleUtility(self,insideOrOutside,  source,  cosineOfConeAngle,basis):
        sourceLength = source.length()
        if sourceLength == 0 : return source
        
        # measure the angular diviation of "source" from "basis"
        direction = source *(1/ sourceLength)
        
        cosineOfSourceAngle = direction.dotProduct (basis)
        # Simply return "source" if it already meets the angle criteria.
        # (note: we hope this top "if" gets compiled out since the flag
        # is a constant when the function is inlined into its caller)
        if insideOrOutside:
            if cosineOfSourceAngle >= cosineOfConeAngle : return source
        else :
            # source vector is already outside the cone, just return it
            if cosineOfSourceAngle <= cosineOfConeAngle : return source
        
        #find the portion of "source" that is perpendicular to "basis"
        perp = Utilities().perpendicularComponent(source,basis)
        
        
        #normalize that perpendicular
        unitPerp = perp
        unitPerp.normalize()

        """# construct a new vector whose length equals the source vector,
            # and lies on the intersection of a plane (formed the source and
            # basis vectors) and a cone (whose axis is "basis" and whose
            # angle corresponds to cosineOfConeAngle)"""
        perpDist = sqrt (1 - (cosineOfConeAngle * cosineOfConeAngle))
        c0 = basis * cosineOfConeAngle
        c1 = unitPerp * perpDist
        return (c0 + c1) * sourceLength 

    def blendIntoAccumulator(self, smoothRate, newValue, smoothedAccumulator):
        return self.interpolate(Utilities().clip(smoothRate, 0., 1.),\
                    smoothedAccumulator,newValue)


        
class LocalSpace:
    """          ----------------------------------------------------------------------------


     OpenSteer -- Steering Behaviors for Autonomous Characters

     Copyright (c) 2002-2003, Sony Computer Entertainment America
     Original author: Craig Reynolds <craig_reynolds@playstation.sony.com>

     Permission is hereby granted, free of charge, to any person obtaining a
     copy of this software and associated documentation files (the "Software"),
     to deal in the Software without restriction, including without limitation
     the rights to use, copy, modify, merge, publish, distribute, sublicense,
     and/or sell copies of the Software, and to permit persons to whom the
     Software is furnished to do so, subject to the following conditions:

     The above copyright notice and this permission notice shall be included in
     all copies or substantial portions of the Software.

     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
     THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
     FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
     DEALINGS IN THE SOFTWARE.


     ----------------------------------------------------------------------------


     LocalSpace: a local coordinate system for 3d space

     Provide functionality such as transforming from local space to global
     space and vice versa.  Also regenerates a valid space from a perturbed
     "forward vector" which is the basis of abnstract vehicle turning.

     These are comparable to a 4x4 homogeneous transformation matrix where the
     3x3 (R) portion is constrained to be a pure rotation (no shear or scale).
     The rows of the 3x3 R matrix are the basis vectors of the space.  They are
     all constrained to be mutually perpendicular and of unit length.  The top
     ("x") row is called "side", the middle ("y") row is called "up" and the
     bottom ("z") row is called forward.  The translation vector is called
     "position".  Finally the "homogeneous column" is always [0 0 0 1].
d
         [ R R R  0 ]      [ Sx Sy Sz  0 ]
         [ R R R  0 ]      [ Ux Uy Uz  0 ]
         [ R R R  0 ]  ->  [ Fx Fy Fz  0 ]
         [          ]      [             ]
         [ T T T  1 ]      [ Tx Ty Tz  1 ]

     This file defines three classes:
       AbstractLocalSpace:  pure virtual interface
       LocalSpaceMixin:     mixin to layer LocalSpace functionality on any base
       LocalSpace:          a concrete object (can be instantiated)

    """
    
    ZERO=Vector3D((0.,0.,0.))
    UNIT_X=Vector3D((1.,0.,0.))
    UNIT_Y=Vector3D((0.,1.,0.))
    UNIT_Z=Vector3D((0.,0.,1.))

    
    def __init__(self):

        print "LocalSpace init..."
        self.position=Vector3D((0.,0.,0.))
        self.up=Vector3D((0.,0.,0.))
        self.side=Vector3D((0.,0.,0.))
        self.forward=Vector3D((1.,0.,0.))
        print("LocalSpace init...2")
        self.resetLocalSpace()
        self._banking=False
        self.forcedNormal=Vector3D((0.0,1.0,0.0))
        print("LocalSpace init...OK")
        
        
    def setSide(self,s):

        self.side=Vector3D(tuple([s[i] for i in range(3)]))
        return  self.side
        
    def setUp(self,u):
        self.up=Vector3D(tuple([u[i] for i in range(3)]))
        return self.up
    
    def setForward(self, f):
        self.forward=Vector3D(tuple([f[i] for i in range(3)]))
        return self.forward
    
    
    def setPosition(self, p):
          
        self.position=Vector3D(p)
        return self.position
        
    def forceNormalUp(self):
        """ A trick to make sure that the object is always up following the _forcedNormal,
        which is normally the Y_Axis vector"""
        self.setUp(self.forcedNormal)
        self.setForward(Utilities().perpendicularComponent(self.forward, self.forcedNormal))
        self.setSide(self.localRotateForwardToSide(self.forward))

    
        
    def rightHanded(self):
        "use right-(or left-)handed coordinate space"
        return True
    
    def resetLocalSpace(self):
        """ ------------------------------------------------------------------------
         reset transform: set local space to its identity state, equivalent to a
         4x4 homogeneous transform like this:
        
             [ X 0 0 0 ]
             [ 0 1 0 0 ]
             [ 0 0 1 0 ]
             [ 0 0 0 1 ]
        
         where X is 1 for a left-handed system and -1 for a right-handed system."""
        self.forward=Vector3D((1.,0.,0.))
        self.up=Vector3D((0.,1.,0.))
        self.side=self.localRotateForwardToSide (self.forward)
        self.position=Vector3D((0., 0., 0.))
    
       
    
    
    def localizeDirection(self, globalDirection):
        """transform a direction in global space to its equivalent in local space"""
        if not (globalDirection is Vector3D) :
            globalDirection=Vector3D(globalDirection)
        
        return Vector3D((globalDirection.dotProduct(self.side),\
                globalDirection.dotProduct(self.up),\
                globalDirection.dotProduct(self.forward)))
     
    def globalizePosition(self, localPosition):
        """transform a point in local space to its equivalent in global space"""
        return self.position+globalizeDirection (localPosition)

    def globalizeDirection(self, localDirection):
        """transform a direction in local space to its equivalent in global space"""
        return self.side*localDirection[0]+ self.up*localDirection[1]+ self.forward*localDirection[2]
                                
    def setUnitSideFromForwardAndUp(self):
        """set "side" basis vector to normalized cross product of forward and up"""
        if self.rightHanded():
            #_side.cross (_forward, _up);
            self.side = self.forward.crossProduct(self.up)
        else:
            #_side.cross(_up, _forward);
            self.side = self.up.crossProduct(self.forward)

        self.side.normalize ()
    
    def regenerateOrthonormalBasisUF(self, newUnitForward):
        """ regenerate the orthonormal basis vectors given a new forward
           (which is expected to have unit length)"""
        
        if not (newUnitForward is Vector3D) : newUnitForward=Vector3D(newUnitForward)
                
        self.forward = newUnitForward

        # derive new side basis vector from NEW forward and OLD up
        self.setUnitSideFromForwardAndUp ()

        # derive new Up basis vector from new Side and new Forward
        # (should have unit length since Side and Forward are
        # perpendicular and unit length)
        if self.rightHanded():
            
            self.up=self.side.crossProduct( self.forward)
        else:
            #_up.cross (_forward, _side);
            self.up = self.forward.crossProduct(self.side)

    def regenerateOrthonormalBasis(self, newForward):
        """for when the new forward is NOT know to have unit length"""
        
        if not (newForward is Vector3D) :
            newForward=Vector3D(newForward)
        
        newForward.normalize()
        self.regenerateOrthonormalBasisUF (newForward)    

    
    def regenerateOrthonormalBasisWithUp(self, newForward,newUp):
        """ for supplying both a new forward and and new up"""
        
        if not (newForward is Vector3D) : newForward=Vector3D(newForward)
        if not (newUp is Vector3D) : newUp=Vector3D(newUp)
        
        self.up = newUp
        newForward.normalize()
        self.regenerateOrthonormalBasis(newForward)    
        
    def localRotateForwardToSide (self, v):
        """rotate, in the canonical direction, a vector pointing in the
        "forward" (+Z) direction to the "side" (+/-X) direction"""
        
        if not self.rightHanded() : v[2]=-v[2]
        return Vector3D((v[2],v[1],v[0]))
    

class AbstractVehicle(LocalSpace) :
    
        
    def  __init__(self):
        LocalSpace.__init__(self)
        self.mass=0.0
        self.speed=0.0
        self.radius=0.0
        
        
    def mass(self):
        """mass (defaults to unity so acceleration=force)"""
        return 0
    
    def setMass(self,mass):
        return 0

    # size of bounding sphere, for obstacle avoidance, etc.
    def radius(self):
        """size of bounding sphere, for obstacle avoidance, etc."""
        return 0
    
    def setRadius(self,radius):
        return 0

    # velocity of vehicle
    def velocity(self): return Vector3D.ZERO

    # speed of vehicle  (may be faster than taking magnitude of velocity)
    def speed(self) : return 0
    
    def setSpeed(self,speed) : self.speed=speed

    
    def predictFuturePosition(self, predictionTime) : 
        """ groups of (pointers to) abstract vehicles, and iterators over them
        #typedef std::vector<AbstractVehicle*> group;
        #typedef group::const_iterator iterator;    

        # predict position of this vehicle at some time in the future
        # (assumes velocity remains constant)"""
        return Vector3D.ZERO
    
    

    
    def maxForce(self):
        """the maximum steering force this vehicle can apply"""
        return 0
    
    def setMaxForce(self,max): return 0
    

    
    def maxSpeed(self):
        """the maximum speed this vehicle is allowed to move"""
        return 0
    
    def setMaxSpeed(self, max): return 0
    
class PathIntersection:
    
    def setIntersect(self,value):
        self.intersect=value
    def setDdistance(self,value):
        self.distance=value
    def setObstacle(self,value):
        self.obstacle=value
    
class Random():
    def nextFloat(self):
        return random()
    
class SteerLibrary (AbstractVehicle) :
    """ """
    
    def  __init__(self) :
        AbstractVehicle.__init__(self)
        self.gaudyPursuitAnnotation = False
        self.randomGenerator=Random()
        self.resetSteering()
    
    def resetSteering (self):
        self.WanderSide = 0
        self.WanderUp = 0

        #default to non-gaudyPursuitAnnotation
        self.gaudyPursuitAnnotation = False
        

        
    def isAhead ( self, target, cosThreshold) :
    
        targetDirection = (target - self.position)
        targetDirection.normalise ()
        return (self.forward().dotProduct(targetDirection) > cosThreshold)
    
    def isAside ( self, target, cosThreshold) :
        targetDirection = (target - self.position)
        targetDirection.normalise ()
        dp = self.forward().dotProduct(targetDirection)
        return (dp < cosThreshold) and (dp > -cosThreshold)
    def frandom01 (self):
        return (self.randomGenerator.nextFloat())
        
    def scalarRandomWalk (self, initial, walkspeed,  min,  max):
        
        next = initial + (((self.frandom01() * 2) - 1) * walkspeed)
        if (next < min) : return min
        if (next > max) : return max
        return next
    
    def isBehind (self, target, cosThreshold) :
    
        targetDirection = (target - self.position)
        targetDirection.normalise ()
        return self.forward().DotProduct(targetDirection) < cosThreshold
    
        
    def steerForWander (self, dt):
        """random walk WanderSide and WanderUp between -1 and +1"""
        speed = 12 * dt
        self.WanderSide = self.scalarRandomWalk (self.WanderSide, speed, -1, 1)
        self.WanderUp   = self.scalarRandomWalk (self.WanderUp,   speed, -1, 1)

        # return a pure lateral steering vector: (+/-Side) + (+/-Up)
        return (self.side() * self.WanderSide) + (self.up() * self.WanderUp)
    
    def steerForSeek(self, target):
        """"""
        #logging.debug("Steer for seek")
        target=Vector3D(target)
        #logging.debug("target : "+str(target))
        
        desiredVelocity = target - self.position
        return desiredVelocity - self.velocity() 
    
    def truncateLength(self, tVector, maxLength):

        tLength = tVector.length()
        returnVector = tVector
        if tLength > maxLength:
            returnVector.normalize() # = tVector - tVector*(tLength - maxLength)
            returnVector = returnVector*maxLength
        return returnVector    
    
class SimpleVehicule(SteerLibrary):
    """    
    // ----------------------------------------------------------------------------
    // <<from original file>> (SB)
    //
    // SimpleVehicle
    //
    // A steerable point mass with a velocity-aligned local coordinate system.
    // SimpleVehicle is useful for developing prototype vehicles in OpenSteerDemo,
    // it is the base class for vehicles in the PlugIns supplied with OpenSteer.
    // Note that SimpleVehicle is provided only as sample code.  Your application
    // can use the OpenSteer library without using SimpleVehicle, as long as you
    // implement the AbstractVehicle protocol.
    //
    // SimpleVehicle makes use of the "mixin" concept from OOP.  To quote
    // "Mixin-Based Programming in C++" a clear and helpful paper by Yannis
    // Smaragdakis and Don Batory (http://citeseer.nj.nec.com/503808.html):
    //
    //     ...The idea is simple: we would like to specify an extension without
    //     predetermining what exactly it can extend. This is equivalent to
    //     specifying a subclass while leaving its superclass as a parameter to be
    //     determined later. The benefit is that a single class can be used to
    //     express an incremental extension, valid for a variety of classes...
    // 
    // In OpenSteer, vehicles are defined by an interface: an abstract base class
    // called AbstractVehicle.  Implementations of that interface, and related
    // functionality (like steering behaviors and vehicle physics) are provided as
    // template-based mixin classes.  The intent of this design is to allow you to
    // reuse OpenSteer code with your application's own base class.
    //
    // 10-04-04 bk:  put everything into the OpenSteer namespace
    // 01-29-03 cwr: created
    //
    //
    // ----------------------------------------------------------------------------
    """    
    
    
    serialNumberCounter=0
    
    
    
    def  __init__(self):
        #print "SteerLibrary initit..."
        SteerLibrary.__init__(self)
        #set inital state
        #print "SteerLibrary initiated"
        self.reset()
        self.banking = False
        self.maxSpeed=10.0
        self.mass=1.0
 
        
        #maintain unique serial numbers
        SimpleVehicule.serialNumberCounter = SimpleVehicule.serialNumberCounter+1
        self.serialNumber=SimpleVehicule.serialNumberCounter

    def velocity(self):
        return self.forward * self.speed

    def reset(self):
        self.resetLocalSpace()
        self.maxForce=0.8
        self.smoothedAcceleration=Vector3D((0,0,0))
        self._lastPosition=Vector3D((0,0,0))
        self._lastForward=self.forward
        self._curvature= self._smoothedCurvature=0
        self.smoothedPosition=self.position
        
    def adjustRawSteeringForce(self,force):
        """// adjust the steering force passed to applySteeringForce.
        //
        // allows a specific vehicle class to redefine this adjustment.
        // default is to disallow backward-facing steering at low speed.
        //
        """
        maxAdjustedSpeed = 0.2 * self.maxSpeed

        if ((self.speed > maxAdjustedSpeed) or (force == Vector3D((0,0,0)))):
            return force
        else :
            range = self.speed / maxAdjustedSpeed
            u=Utilities()
            cosine = u.interpolate(pow(range, 20), 1.0, -1.0)
            tmp= u.limitMaxDeviationAngle(force, cosine, self.forward)
            
            return tmp
        
    def interpolate(self, alpha,  x0,  x1):
        
            return x0 + ((x1 - x0) * alpha)
        
    def regenerateLocalSpace(self,newVelocity):
        """// ----------------------------------------------------------------------------
        // the default version: keep FORWARD parallel to velocity, change UP as
        // little as possible.
        //
        // parameter names commented out to prevent compiler warning from "-W"
        """
        # adjust orthonormal basis vectors to be aligned with new velocity
        if self.speed > 0:
            #print self.speed
            self.regenerateOrthonormalBasisUF (newVelocity / self.speed)
        

    def regenerateLocalSpaceForBanking(self,newVelocity,elapsedTime):
        """// ----------------------------------------------------------------------------
        // alternate version: keep FORWARD parallel to velocity, adjust UP according
        // to a no-basis-in-reality "banking" behavior, something like what birds and
        // airplanes do
        """

        # the length of this global-upward-pointing vector controls the vehicle's
        # tendency to right itself as it is rolled over from turning acceleration
        globalUp =Vector3D(0, 0.2, 0)

        # acceleration points toward the center of local path curvature, the
        # length determines how much the vehicle will roll while turning
        accelUp = self._smoothedAcceleration * 0.05

        # combined banking, sum of UP due to turning and global UP
        bankUp = accelUp + globalUp

        # blend bankUp into vehicle's UP basis vector
        smoothRate = elapsedTime * 3
        TempUp = Vector3D(self.up)
        tempUp=Utilities.blendIntoAccumulator(smoothRate, bankUp, tempUp)
        tempUp.normalize()
        self.setUp (tempUp)

        # adjust orthonormal basis vectors to be aligned with new velocity
        self.regenerateLocalSpace(newVelocity)
    
    
    def measurePathCurvature(self,elapsedTime):
        """// ----------------------------------------------------------------------------
        // measure path curvature (1/turning-radius), maintain smoothed version
        """

        if elapsedTime > 0:
            
            dP = self._lastPosition - self.position;
            dF = (self._lastForward - self.forward ) / dP.length()
            #SI - BIT OF A WEIRD FIX HERE . NOT SURE IF ITS CORRECT
            #Vector3 lateral = dF.perpendicularComponent (forward ());
            lateral = Utilities().perpendicularComponent( dF,self.forward)

            if lateral.dotProduct(self.side) < 0 :
                sign=1.0
            else :
                sign=-1.0
            self._curvature = lateral.length() * sign
            #OpenSteerUtility.blendIntoAccumulator(elapsedTime * 4.0f, _curvature,_smoothedCurvature);
            self._smoothedCurvature= \
                Utilities().blendIntoAccumulator(elapsedTime * 4.0, \
                self._curvature, self._smoothedCurvature)

            self._lastForward = self.forward 
            self._lastPosition = self.position

    
    def applySteeringForce(self, force, elapsedTime):
    

        adjustedForce = self.adjustRawSteeringForce (force)

        """ enforce limit on magnitude of steering force
        #Vector3 clippedForce = adjustedForce.truncateLength (maxForce ());
        #Vector3 clippedForce = adjustedForce.truncateLength(maxForce());"""

           
        clippedForce = self.truncateLength(adjustedForce, self.maxForce)
        #print "clippedforce : "+str(clippedForce)
        # compute acceleration and velocity
        newAcceleration = clippedForce * (1/ self.mass)
        newVelocity = self.velocity()

        # damp out abrupt changes and oscillations in steering acceleration
        # (rate is proportional to time step, then clipped into useful range)
        if elapsedTime > 0:
            smoothRate =Utilities().clip(9 * elapsedTime, 0.15, 0.4)
            self.smoothedAcceleration=Utilities().blendIntoAccumulator(\
                                smoothRate,\
                                  newAcceleration, self.smoothedAcceleration)
        
        #print "smotthed acceleration : "+str(self.smoothedAcceleration)
        
        # Euler integrate (per frame) acceleration into velocity
        newVelocity = newVelocity+self.smoothedAcceleration * elapsedTime

        # enforce speed limit
        
        #newVelocity = newVelocity.truncateLength (maxSpeed ());
        newVelocity = self.truncateLength(newVelocity,self.maxSpeed)
        #print "new Velocity : "+ str(newVelocity)

        # update Speed
        self.setSpeed (newVelocity.length())
        #logging.debug(str(newVelocity))
        
        # Euler integrate (per frame) velocity into position
        self.setPosition (self.position+ (newVelocity * elapsedTime))
        #logging.debug(str(self.position))
        
        # regenerate local space (by default: align vehicle's forward axis with
        # new velocity, but this behavior may be overridden by derived classes.)
        if not self._banking:
            self.regenerateLocalSpace(newVelocity)
        else:
            self.regenerateLocalSpaceForBanking(newVelocity, elapsedTime)

        # maintain path curvature information
        self.measurePathCurvature (elapsedTime)

        # running average of recent positions
        self.smoothedPosition=Utilities().blendIntoAccumulator(elapsedTime * 0.06,\
                              self.position , self.smoothedPosition)

        return newVelocity
  

class PolylinePathway:
    
    
    def __init__(self,_pointCount, points,_radius,_cyclic):
        """// construct a PolylinePathway given the number of points (vertices),
        // an array of points, and a path radius.
        
        arguments : integer,Vector3D[], float,boolean
        
        
        """
        self.initialize(_pointCount, _points, _radius, _cyclic)

    def initialize(self,_pointCount,_points,_radius,_cyclic):
        """// utility for constructors
        arguments : integer,Vector3D[], float,boolean
        """
        # set data members, allocate arrays
        self.radius = _radius;
        self.cyclic = _cyclic;
        self.pointCount = _pointCount;
        self.totalPathLength = 0;
        if cyclic : 
            pointCount+=1
        self.lengths = []
        self.points  = []
        self.normals = []
        
        for i in range(_pointCount):
            closeCycle = _cyclic & (i == self.pointCount-1)
            if closeCycle : j=0
            else : j=i
            
            self.points.extend( _points[j])
            if i > 0 :
                # compute the segment length
                self.normals.extend( self.points[i] - self.points[i-1])
                self.lengths.extend( self.normals[i].length ())

                # find the normalized vector parallel to the segment
                self.normals[i] *= 1 / self.lengths[i]

                # keep running total of segment lengths
                self.totalPathLength += self.lengths[i]
        
    def mapPointToPath (self, point,tangent, outside):
        """
        Given an arbitrary point ("A"), returns in a tuple the nearest point ("P") on
        this path, the path tangent at P and a measure of how far A
        is outside the Pathway's "tube".
        Note that a negative distance indicates A is inside the Pathway.
        """
    
        minDistance = 10000
        
        ### TO BE CONTINUED 

if __name__ == '__main__':
    print ("Start test")
    ls=SimpleVehicule()

    print ls.position
    
    for i in range(20):
        ls.applySteeringForce(ls.steerForSeek((01,00,01)),0.1)
        print ls.position
        
        
    
    