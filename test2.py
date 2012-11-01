import os, sys
import ogre.renderer.OGRE as ogre
import ogre.renderer.ogreterrain as ogreterrain
import ogre.renderer.ogrepaging as ogrepaging
import ogre.io.OIS as OIS
import math


class GameCamera(object): # camera update
    def __init__(self, scene, camera, cameraNode, defNodeOrient):
        self.scene = scene
        self.viewPort = scene.ogreRoot.getAutoCreatedWindow().addViewport(camera)
        self.camera = camera
        self.cameraNode = cameraNode
        self.defNodeOrient = defNodeOrient

        self.camHeight = 40
        self.translateVector = ogre.Vector3(0.0, 0.0, 0.0)
        self.moveScale = 0
        self.moveSpeed = 400
        self.rotationScale = 0.1
        self.rotationSpeed = 0.5
        self.key = None

        self.ResetRotation()
        self.MoveCamera(500, self.camHeight, 500)
        self.RotateCamera(0, 0)

        listener = scene.gameRoot.GetEventListener()
        listener.BindMouseMoved(self._OnMouseMoved)
        listener.BindKeyPressed(self._OnKeyPressed)
        listener.BindKeyReleased(self._OnKeyReleased)
        listener.BindTick(self._OnTick)

    def _OnTick(self, frameEvent, lastMouseState, lastKeyState):
        if frameEvent.timeSinceLastFrame == 0:
            self.moveScale = 1
            self.rotationScale = 0.1

        else:
            self.moveScale = self.moveSpeed * frameEvent.timeSinceLastFrame
            self.rotationScale = self.rotationSpeed * frameEvent.timeSinceLastFrame

        if self.key == OIS.KC_A:
            self.translateVector.x = -self.moveScale

        if self.key == OIS.KC_D:
            self.translateVector.x = self.moveScale

        if self.key == OIS.KC_W:
            self.translateVector.z = -self.moveScale

        if self.key == OIS.KC_S:
            self.translateVector.z = self.moveScale

        if self.key == OIS.KC_PGUP:
            self.translateVector.y = self.moveScale

        if self.key == OIS.KC_PGDOWN:
            self.translateVector.y = -self.moveScale

        if self.key in [OIS.KC_A, OIS.KC_D, OIS.KC_W, OIS.KC_S, OIS.KC_PGDOWN, OIS.KC_PGUP]:
            self.TranslateCamera(self.translateVector)
    def _OnKeyReleased(self, evt):
        self.key = None
    def _OnKeyPressed(self, evt):
        self.key = evt.key

    def _OnMouseMoved(self, lastMouseState):
        self.RotateCamera(-lastMouseState.relX*self.rotationSpeed, -lastMouseState.relY*self.rotationSpeed)


    def MoveCamera(self, x, y, z):
        self.cameraNode.setPosition(x, y, z)

    def TranslateCamera(self, translateVector):
        try:
            self.camera.translate(translateVector) # for using OgreRefApp
        except AttributeError:
            self.camera.moveRelative(translateVector)

    def RotateCamera(self, yaw, pitch):
        self.camera.getParentSceneNode().yaw(ogre.Degree(yaw),
                ogre.Node.TS_WORLD)
        self.camera.getParentSceneNode().pitch(ogre.Degree(pitch))
        self.cameraNode._updateBounds()

    def ResetRotation(self):
        self.cameraNode.setOrientation(self.defNodeOrient)
        self.camera.lookAt(
            self.cameraNode._getDerivedPosition() + ogre.Vector3().NEGATIVE_UNIT_Z)

    def GetViewport(self):
        return self.viewPort

    def GetDefaultNodeOrient(self):
        return self.defNodeOrient
    def GetOgreCamera(self):
        return self.camera


class GameRoot(object): # Facade
    def __init__(self, ogreRoot, eventListener):
        self.ogreRoot = ogreRoot
        self.eventListener = eventListener
        self.scene = Scene(self)
        self.scene.OnGameRootInit()

    def GetOgreRoot(self):
        return self.ogreRoot
    def GetScene(self):
        return self.scene
    def GetEventListener(self):
        return self.eventListener

class MouseState(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.relX = 0
        self.relY = 0
        self.relZ = 0
        self.pressedButtons = {}

    def OnMouseMoved(self, x, y, w, h, relX, relY, relZ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.relX = relX
        self.relY = relY
        self.relZ = relZ
    def OnMousePressed(self, x, y, w, h, id):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.pressedButtons[id] = 0
    def OnMouseReleased(self, x, y, w, h, id):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        try:
            del self.pressedButtons[id]
        except:
            pass
    def UpdateWithMouseState(self, mouseState):
        self.x, self.y, self.w, self.h = mouseState.GetValues()
        self.relX, self.relY = self.GetRelativeMovements()
        for key in mouseState.GetPressedButtons().iterkeys():
            self.pressedButtons[key] = mouseState.GetPressedButtons()[key]
    def OnTick(self, time):
        for key in self.pressedButtons.iterkeys():
            self.pressedButtons[key] += time

    def GetValues(self):
        return self.x, self.y, self.w, self.h
    def GetRelativeMovements(self):
        return self.relX, self.relY
    def GetWheelMovement(self):
        return self.relZ
    def GetPressedButtons(self):
        return self.pressedButtons
    def _GetScreenVector(self, x, y, w, h):
        if w and h:
            mx = float(x) - float(w)/2.0
            my = float(y) - float(h)/2.0
            vectorX, vectorY = mx/(float(w)/2.0), -my/(float(h)/2.0)
            return vectorX, vectorY
        else:
            return 0, 0
    def GetScreenVector(self):
        return self._GetScreenVector(*self.GetValues())

    def GetScreenVectorDegree(self):
        vector = self.GetScreenVector()
        return Vector2ToAngle(*vector)

def Vector2ToAngle(x, y):
    vecOrg = ogre.Vector2(1.0, 0.0)
    vecPos = ogre.Vector2(x, y)
    vecPos.normalise()
    dotted = vecOrg.dotProduct(vecPos)
    if dotted == 0.0:
        dotted = 0.0001
    convert = 360.0/(2*math.pi)

    angle = math.acos(dotted)*convert
    if y < 0:
        angle = -angle
    angle %= 360
    return angle

class KeyState(object):
    def __init__(self):
        self.pressedKey = None
        self.pressedChar = None
        self.timePressedFor = None

    def OnKeyPressed(self, evt):
        self.pressedKey = evt.key
        self.pressedChar = evt.text
        self.timePressedFor = 0
    def OnTick(self, time):
        if self.timePressedFor:
            self.timePressedFor += time
    def OnKeyReleased(self):
        self.pressedKey = None
        self.pressedChar = None
        self.timePressedFor = None

    def GetPressedKey(self):
        return self.pressedKey
    def GetPressedTime(self):
        return self.timePressedFor

class OgreEventListener(ogre.FrameListener, ogre.WindowEventListener,
        OIS.MouseListener, OIS.KeyListener, OIS.JoyStickListener):
    mouse = None
    keyboard = None
    joy = None
 
    def __init__(self, app, renderWindow, bufferedMouse, bufferedKeys, bufferedJoy):
        ogre.FrameListener.__init__(self)
        ogre.WindowEventListener.__init__(self)
        OIS.MouseListener.__init__(self)
        OIS.KeyListener.__init__(self)
        OIS.JoyStickListener.__init__(self)

        self.app = app
        self.renderWindow = renderWindow

        # Init input system
        import platform
        int64 = False
        for bit in platform.architecture():
            if '64' in bit:
                int64 = True
        # Create the inputManager using the supplied renderWindow
        if int64:
            windowHnd = self.renderWindow.getCustomAttributeUnsignedLong("WINDOW")
        else:
            windowHnd = self.renderWindow.getCustomAttributeInt("WINDOW")
        t = self._inputSystemParameters()
        params = [("WINDOW",str(windowHnd))]
        params.extend(t)   
        self.inputManager = OIS.createPythonInputSystem(params)

        try:
            if bufferedMouse:
                self.mouse = self.inputManager.createInputObjectMouse(OIS.OISMouse, bufferedMouse)
                self.mouse.setEventCallback(self)

            if bufferedKeys:
                self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, bufferedKeys)
                self.keyboard.setEventCallback(self)

            if bufferedJoy:
                self.joy = self.inputManager.createInputObjectJoyStick(OIS.OISJoyStick, bufferedJoy)
                self.joy.setEventCallback(self)

        except Exception, e: # Unable to obtain mouse/keyboard/joy input
            raise e


        self.windowResized(self.renderWindow)

        # Listen for any events directed to the window manager's close button
        ogre.WindowEventUtilities.addWindowEventListener(self.renderWindow, self)

        self.quitApplication = False
        self.lastMouseState = MouseState()
        self.lastKeyState = KeyState()

        self.bindsMouseMoved = []
        self.bindsMousePressed = []
        self.bindsMouseReleased = []
        self.bindsKeyPressed = []
        self.bindsKeyReleased = []
        self.bindsOnTick = []
        self.bindsAppClosed = []

        self.bindsMouseMovedReturn = None
        self.bindsMousePressedReturn = None
        self.bindsMouseReleasedReturn = None



    def __del__ (self ):
        # Clean up OIS 
        self.delInputObjects()
 
        OIS.InputManager.destroyInputSystem(self.inputManager)
        self.inputManager = None
 
        ogre.WindowEventUtilities.removeWindowEventListener(self.renderWindow, self)
        self.windowClosed(self.renderWindow)
 
    def delInputObjects(self):
        # Clean up the initialized input objects
        if self.keyboard:
            self.inputManager.destroyInputObjectKeyboard(self.keyboard)
        if self.mouse:
            self.inputManager.destroyInputObjectMouse(self.mouse)
        if self.joy:
            self.inputManager.destroyInputObjectJoy(self.joy)
 
 
### Window Event Listener callbacks ###
 
    def windowResized(self, rw):
         dummyint = 0
         width, height, depth, left, top= rw.getMetrics(dummyint,dummyint,dummyint, dummyint, dummyint)
         # Note the wrapped function as default needs unsigned int's
         ms = self.mouse.getMouseState()
         ms.width = width
         ms.height = height
 
    def windowClosed(self, renderWindow):
        # Only close for window that created OIS
        for func in self.bindsAppClosed:
            func()
        if(renderWindow == self.renderWindow):
            del self

        import sys
        sys.exit()
 
### Mouse Listener callbacks ###
    def mouseMoved(self,arg):
        state = arg.get_state()
        self.lastMouseState.OnMouseMoved(state.X.abs, state.Y.abs, state.width, state.height, state.X.rel, state.Y.rel, state.Z.rel)
        for func in self.bindsMouseMoved:
            func(self.lastMouseState)

        return True

    def mousePressed(self, arg, id):
        state = arg.get_state()
        self.lastMouseState.OnMousePressed(state.X.abs, state.Y.abs, state.width, state.height, id)
        for func in self.bindsMousePressed:
            func(self.lastMouseState, id)

        return True
    
    def mouseReleased(self, arg, id):
        state = arg.get_state()
        self.lastMouseState.OnMouseReleased(state.X.abs, state.Y.abs, state.width, state.height, id)

        for func in self.bindsMouseReleased:
            func(self.lastMouseState, id)
        return True
 
### Key Listener callbacks ###
    def keyPressed(self, evt):
        self.lastKeyState.OnKeyPressed(evt)

        for func in self.bindsKeyPressed:
            func(evt)
        return True
 
    def keyReleased(self, evt):
        self.lastKeyState.OnKeyReleased()

        for func in self.bindsKeyReleased:
            func(evt)
        return True

### Joystick Listener callbacks ### 
    def buttonPressed(self, evt, id):
        return True
 
    def buttonReleased(self, evt, id):
        return True
 
    def axisMoved(self, evt, id):
        return True

### For mouse pointer ###
    def _inputSystemParameters (self ):
        if os.name == 'nt':
            return [("w32_mouse","DISCL_FOREGROUND"), ("w32_mouse", "DISCL_NONEXCLUSIVE")]
    
### Tick ###
    def frameStarted(self, frameEvent):              
        if self.keyboard:
            self.keyboard.capture()
        if self.mouse:
            self.mouse.capture()
        if self.joy:
            self.joy.capture()
            # joystick test
            axes_int = self.joy.getJoyStickState().mAxes
            axes = []
            for i in axes_int:
                axes.append(i.abs)            

        self.lastMouseState.OnTick(frameEvent.timeSinceLastFrame)
        self.lastKeyState.OnTick(frameEvent.timeSinceLastFrame)

        for func in self.bindsOnTick:
            func(frameEvent, self.lastMouseState, self.lastKeyState)

        stats = self.renderWindow.getStatistics()
        curFPS = str(int(stats.lastFPS))
        #print curFPS

        return True

    def BindMouseMoved(self, func):
        self.bindsMouseMoved += [func]
    def BindMousePressed(self, func):
        self.bindsMousePressed += [func]
    def BindMouseReleased(self, func):
        self.bindsMouseReleased += [func]

    def BindMouseMovedReturn(self, func):
        self.bindsMouseMovedReturn = func
    def BindMousePressedReturn(self, func):
        self.bindsMousePressedReturn = func
    def BindMouseReleasedReturn(self, func):
        self.bindsMouseReleasedReturn = func

    def BindKeyPressed(self, func):
        self.bindsKeyPressed += [func]
    def BindKeyReleased(self, func):
        self.bindsKeyReleased += [func]

    def BindTick(self, func):
        self.bindsOnTick += [func]

    def BindAppClosed(self, func):
        self.bindsAppClosed += [func]



class DummyPageProvider(ogrepaging.PageProvider):
    def prepareProceduralPage(self, page, section):
        return True
    def loadProceduralPage(self, page, section):
        return True
    def unloadProceduralPage(self, page, section):
        return True
    def unprepareProceduralPage(self, page, section):
        return True

class NewTerrain(object):
    MODE_NORMAL = 0
    MODE_EDIT_HEIGHT = 1
    MODE_EDIT_BLEND = 2

    SHADOWS_NONE = 0
    SHADOWS_COLOUR = 1
    SHADOWS_DEPTH = 2


    TERRAIN_PAGE_MIN_X = 0
    TERRAIN_PAGE_MIN_Y = 0
    TERRAIN_PAGE_MAX_X = 0
    TERRAIN_PAGE_MAX_Y = 0

    TERRAIN_FILE_PREFIX = "testTerrain"
    TERRAIN_FILE_SUFFIX = "dat"
    TERRAIN_WORLD_SIZE = 12000.0
    TERRAIN_SIZE = 513

    def __init__(self, sceneManager, scene):
        self.sceneMgr = sceneManager
        self.scene = scene
        self.camera = scene.GetCamera().camera
        self.root = scene.gameRoot.GetOgreRoot()
        self.ray = ogre.Ray()

        self.paging = True
        self.terrainGroup = None
        self.terrainPaging = None
        self.pageManager = None
        self.fly = False
        self.fallVelocity = 0
        self.dummyPageProvider = DummyPageProvider()
        self.mode = NewTerrain.MODE_NORMAL
        self.shadowMode = NewTerrain.SHADOWS_NONE
        self.layerEdit = 1
        self.brushSizeTerrainSpace = 0.02
        self.editNode = None
        self.editMarker = None
        self.updateCountDown = 0
        self.updateRate = 1.0 / 20.0
        self.terrainPos = ogre.Vector3(1000, 0, 5000)
        self.terrainsImported = False
        self.pssmSetup = None
        #XXX: I don't know what to do here. pssmSetup's supposed to be ShadowCameraSetupPtr
        self.houseList = []



        self.pressingKey = None
        listener = scene.gameRoot.GetEventListener()
        listener.BindMouseMoved(self._OnMouseMoved)
        listener.BindKeyPressed(self._OnKeyPressed)
        listener.BindKeyReleased(self._OnKeyReleased)
        listener.BindTick(self._OnTick)


        self.setupView()
        self.setupContent()

    def _OnTick(self, frameEvent, lastMouseState, lastKeyState):
        if self.mode != NewTerrain.MODE_NORMAL:
            ray = self.GetMouseRay(*lastMouseState.GetValues())
            rayResult = self.terrainGroup.rayIntersects(ray)
            if rayResult.hit:
                self.editMarker.setVisible(True)
                self.editNode.setPosition(rayResult.position)

                # figure out which terrains this affects
                brushSizeWorldSpace = NewTerrain.TERRAIN_WORLD_SIZE * self.brushSizeTerrainSpace
                sphere = ogre.Sphere(rayResult.position, brushSizeWorldSpace)
                terrainList = self.terrainGroup.sphereIntersects(sphere)

                for ti in terrainList:
                    doTerrainModify(ti, rayResult.position, frameEvent.timeSinzeLastFrame)
            else:
                self.editMarker.setVisible(False)

        # no need to do this
        """
        if (!mFly)
        {
            // clamp to terrain
            Vector3 camPos = mCamera->getPosition();
            Ray ray;
            ray.setOrigin(Vector3(camPos.x, 10000, camPos.z));
            ray.setDirection(Vector3::NEGATIVE_UNIT_Y);

            TerrainGroup::RayResult rayResult = mTerrainGroup->rayIntersects(ray);
            Real distanceAboveTerrain = 50;
            Real fallSpeed = 300;
            Real newy = camPos.y;
            if (rayResult.hit)
            {
                if (camPos.y > rayResult.position.y + distanceAboveTerrain)
                {
                    mFallVelocity += evt.timeSinceLastFrame * 20;
                    mFallVelocity = std::min(mFallVelocity, fallSpeed);
                    newy = camPos.y - mFallVelocity * evt.timeSinceLastFrame;

                }
                newy = std::max(rayResult.position.y + distanceAboveTerrain, newy);
                mCamera->setPosition(camPos.x, newy, camPos.z);
                
            }

        }
        """

        
        if self.updateCountDown > 0:
            self.updateCountDown -= frameEvent.timeSinceLastFrame
            if self.updateCountDown <= 0:
                self.terrainGroup.update()
                self.updateCountDown = 0
        
        if terrainGroup.isDerivedDataUpdateInProgress():
            if self.terrainsImported:
                print "Building terrain, please wait..."
            else:
                print "Updating textures, patience..."
        else:
            if self.terrainsImported:
                self.saveTerrains(True)
                self.terrainsImported = False

    def _OnKeyReleased(self, evt):
        self.pressingKey = None
    def _OnKeyPressed(self, evt):
        if evt.key == OIS.KC_S:
            if self.pressingKey == OIS.KC_LCONTROL or self.pressingKey == OIS.KC_RCONTROL:
                self.saveTerrains(True)


        if evt.key == OIS.KC_F10:
            ti = self.terrainGroup.getTerrainIterator()
            while ti.hasMoreElements():
                tkey = ti.peekNextKey()
                ts = ti.getNext()
                if ts.instance and ts.instance.isLoaded():
                    ts.instance._dumpTextures("terrain_" + str(tkey), ".png")

        if evt.key == OIS.KC_1:
            self.mode = NewTerrain.MODE_NORMAL
        if evt.key == OIS.KC_2:
            self.mode = NewTerrain.MODE_EDIT_HEIGHT
        if evt.key == OIS.KC_3:
            self.mode = NewTerrain.MODE_EDIT_BLEND
        if evt.key == OIS.KC_4:
            self.shadowMode = NewTerrain.SHADOWS_NONE
            self.changeShadows()
        if evt.key == OIS.KC_5:
            self.shadowMode = NewTerrain.SHADOWS_COLOUR
            self.changeShadows()
        if evt.key == OIS.KC_6:
            self.shadowMode = NewTerrain.SHADOWS_DEPTH
            self.changeShadows()


        self.pressingKey = evt.key
    def _OnMouseMoved(self, lastMouseState):
        self.RotateCamera(-lastMouseState.relX*self.rotationSpeed, -lastMouseState.relY*self.rotationSpeed)




    def GetMouseRay(self, x, y, w, h):
        pos_w = float(x) / float(w)
        pos_h = float(y) / float(h)
        mouseRay = self.scene.GetCameraToViewportRay(pos_w, pos_h)
        return mouseRay


    def doTerrainModify(self, terrain, centrepos, timeElepsed):
        tsPos = terrain.getTerrainPosition(centrepos)

        if self.pressingKey == OIS.KC_EQUALS or self.pressingKey == OIS.KC_MINUS:
            if self.mode == NewTerrain.MODE_EDIT_HEIGHT:
                terrainSize = terrain.getSize() - 1
                startx = (tsPos.x - self.brushSizeTerrainSpace) * terrainSize
                starty = (tsPos.y - self.brushSizeTerrainSpace) * terrainSize
                endx = (tsPos.x + self.brushSizeTerrainSpace) * terrainSize
                endy = (tsPos.y + self.brushSizeTerrainSpace) * terrainSize
                startx = max(startx, 0)
                starty = max(starty, 0)
                endx = min(endx, terrainSize)
                endy = min(endy, terrainSize)

                x = startx
                y = starty
                while y <= endy:
                    while x <= endx:
                        tsXdist = (x / terrainSize) - tsPos.x
                        tsYdist = (y / terrainSize) - tsPos.y
                        weight = min(1.0, math.sqrt(tsYdist ** 2 + tsXdist ** 2) / (0.5* self.brushSizeTerrainSpace))
                        weight = 1.0 - weight**2

                        addedHeight = weight * 250.0 * timeElepsed
                        if self.pressingKey == OIS.KC_EQUALS:
                            newheight = terrain.getHeightAtPoins(x, y) + addedHeight
                        else:
                            newheight = terrain.getHeightAtPoins(x, y) - addedHeight
                        terrain.setHeightAtPoint(x, y, newheight)
                        if self.updateCountDown == 0:
                            self.updateCountDown = self.updateRate

                        x += 1
                    y += 1

            elif self.mode == NewTerrain.MODE_EDIT_BLEND:
                layer = terrain.getLayerBlendMap(self.layerEdit)
                # we need image coords
                imgSize = terrain.getLayerBlendMapSize()
                startx = (tsPos.x - self.brushSizeTerrainSpace) * imgSize
                starty = (tsPos.y - self.brushSizeTerrainSpace) * imgSize
                endx = (tsPos.x + self.brushSizeTerrainSpace) * imgSize
                endy = (tsPos.y + self.brushSizeTerrainSpace) * imgSize
                startx = max(startx, 0)
                starty = max(starty, 0)
                endx = min(endx, imgSize)
                endy = min(endy, imgSize)
                x = startx
                y = starty
                while y <= endy:
                    while x <= endx:
                        tsXdist = (x / imgSize) - tsPos.x
                        tsYdist = (y / imgSize) - tsPos.y
                        weight = min(1.0, math.sqrt(tsYdist ** 2 + tsXdist ** 2) / (0.5 * self.brushSizeTerrainSpace))
                        weight = 1.0 - weight**2

                        paint = weight * timeElapsed
                        imgY = imgSize - y
                        if self.pressingKey == OIS.KC_EQUALS:
                            val = layer.getBlendValue(x, imgY) + paint
                        else:
                            val = layer.getBlendValue(x, imgY) - paint

                        val = ogre.Math.Clamp(val, 0.0, 1.0)
                        layer.setBlendValue(x, imgY, val)
                        layer.update()


                        x += 1
                    y += 1

    def saveTerrains(self, onlyIfModified):
        self.terrainGroup.saveAllTerrains(onlyIfModified)

    def defineTerrain(self, x, y, flat = False):
        """
        // if a file is available, use it
        // if not, generate file from import

        // Usually in a real project you'll know whether the compact terrain data is
        // available or not; I'm doing it this way to save distribution size
        """
        if flat:
            self.terrainGroup.defineTerrain(x, y, 0.0)
        else:
            filename = self.terrainGroup.generateFilename(x, y)
            if ogre.ResourceGroupManager.getSingleton().resourceExists(self.terrainGroup.getResourceGroup(), filename):
                self.terrainGroup.defineTerrain(x, y)
            else:
                img = self.getTerrainImage((x % 2) != 0, (y%2) != 0)
                self.terrainGroup.defineTerrain(x, y, img)
                self.terrainsImported = True

    def getTerrainImage(self, flipX, flipY):
        img = ogre.Image()
        img.load("terrain.png", ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME)
        if flipX:
            img.flipAroundY()
        if flipY:
            img.flipAroundX()
        
        return img

    def initBlendMaps(self, terrain):
        # XXX: I don't know how it is gonna be done so I'll leave it be
        blendMap0 = terrain.getLayerBlendMap(1)
        blendMap1 = terrain.getLayerBlendMap(2)
        minHeight0 = 70
        fadeDist0 = 40
        minHeight1 = 70
        fadeDist1 = 15
        # float* pBlend0 = blendMap0.getBlendPointer()
        # float* pBlend1 = blendMap1.getBlendPointer()

        # for (Ogre::uint16 y = 0; y < terrain->getLayerBlendMapSize(); ++y)
        # {
        #     for (Ogre::uint16 x = 0; x < terrain->getLayerBlendMapSize(); ++x)
        #     {
        #         Real tx, ty;

        #         blendMap0->convertImageToTerrainSpace(x, y, &tx, &ty);
        #         Real height = terrain->getHeightAtTerrainPosition(tx, ty);
        #         Real val = (height - minHeight0) / fadeDist0;
        #         val = Math::Clamp(val, (Real)0, (Real)1);
        #         //*pBlend0++ = val;

        #         val = (height - minHeight1) / fadeDist1;
        #         val = Math::Clamp(val, (Real)0, (Real)1);
        #         *pBlend1++ = val;
        #     }
        # }
        # blendMap0.dirty()
        # blendMap1.dirty()
        # #//blendMap0->loadImage("blendmap1.png", ResourceGroupManager::DEFAULT_RESOURCE_GROUP_NAME);
        # blendMap0.update()
        # blendMap1.update()

        # """
        # // set up a colour map
        # /*
        # if (!terrain->getGlobalColourMapEnabled())
        # {
        #     terrain->setGlobalColourMapEnabled(true);
        #     Image colourMap;
        #     colourMap.load("testcolourmap.jpg", ResourceGroupManager::DEFAULT_RESOURCE_GROUP_NAME);
        #     terrain->getGlobalColourMap()->loadImage(colourMap);
        # }
        # */
        # """


    def configureTerrainDefaults(self, l):
        #// Configure global
        ogreterrain.TerrainGlobalOptions.setMaxPixelError(8)
        #// testing composite map
        ogreterrain.TerrainGlobalOptions.setCompositeMapDistance(3000)
        #//TerrainGlobalOptions::setUseRayBoxDistanceCalculation(true);
        #//TerrainGlobalOptions::getDefaultMaterialGenerator()->setDebugLevel(1);
        #//TerrainGlobalOptions::setLightMapSize(256);
        # XXX: castAsSM2Profile?
        """
        TerrainMaterialGeneratorA::SM2Profile* matProfile = 
            static_cast<TerrainMaterialGeneratorA::SM2Profile*>(TerrainGlobalOptions::getDefaultMaterialGenerator()->getActiveProfile());
        """
        matProfile = ogreterrain.getDefaultMaterialGenerator().getActiveProfile()

        #//matProfile->setLightmapEnabled(false);
        #// Important to set these so that the terrain knows what to use for derived (non-realtime) data
        ogreterrain.TerrainGlobalOptions.setLightMapDirection(l.getDerivedDirection())
        ogreterrain.TerrainGlobalOptions.setCompositeMapAmbient(self.sceneMgr.getAmbientLight())
        #//TerrainGlobalOptions::setCompositeMapAmbient(ColourValue::Red);
        ogreterrain.TerrainGlobalOptions.setCompositeMapDiffuse(l.getDiffuseColour())

        #// Configure default import settings for if we use imported image
        defaultimp = self.terrainGroup.getDefaultImportSettings()
        defaultimp.terrainSize = NewTerrain.TERRAIN_SIZE
        defaultimp.worldSize = NewTerrain.TERRAIN_WORLD_SIZE
        defaultimp.inputScale = 600
        defaultimp.minBatchSize = 33
        defaultimp.maxBatchSize = 65
        #// textures
        defaultimp.layerList.resize(3)
        defaultimp.layerList[0].worldSize = 100
        defaultimp.layerList[0].textureNames.push_back("dirt_grayrocky_diffusespecular.dds");
        defaultimp.layerList[0].textureNames.push_back("dirt_grayrocky_normalheight.dds");
        defaultimp.layerList[1].worldSize = 30
        defaultimp.layerList[1].textureNames.push_back("grass_green-01_diffusespecular.dds");
        defaultimp.layerList[1].textureNames.push_back("grass_green-01_normalheight.dds");
        defaultimp.layerList[2].worldSize = 200
        defaultimp.layerList[2].textureNames.push_back("growth_weirdfungus-03_diffusespecular.dds");
        defaultimp.layerList[2].textureNames.push_back("growth_weirdfungus-03_normalheight.dds");


    """
    void addTextureDebugOverlay(TrayLocation loc, TexturePtr tex, size_t i)
    {
        addTextureDebugOverlay(loc, tex->getName(), i);
    }
    void addTextureDebugOverlay(TrayLocation loc, const String& texname, size_t i)
    {
        // Create material
        String matName = "Ogre/DebugTexture" + StringConverter::toString(i);
        MaterialPtr debugMat = MaterialManager::getSingleton().getByName(matName);
        if (debugMat.isNull())
        {
            debugMat = MaterialManager::getSingleton().create(matName,
                ResourceGroupManager::DEFAULT_RESOURCE_GROUP_NAME);
        }
        Pass* p = debugMat->getTechnique(0)->getPass(0);
        p->removeAllTextureUnitStates();
        p->setLightingEnabled(false);
        TextureUnitState *t = p->createTextureUnitState(texname);
        t->setTextureAddressingMode(TextureUnitState::TAM_CLAMP);

        // create template
        if (!OverlayManager::getSingleton().hasOverlayElement("Ogre/DebugTexOverlay", true))
        {
            OverlayElement* e = OverlayManager::getSingleton().createOverlayElement("Panel", "Ogre/DebugTexOverlay", true);
            e->setMetricsMode(GMM_PIXELS);
            e->setWidth(128);
            e->setHeight(128);
        }

        // add widget
        String widgetName = "DebugTex"+ StringConverter::toString(i);
        Widget* w = mTrayMgr->getWidget(widgetName);
        if (!w)
        {
            w = mTrayMgr->createDecorWidget(
                loc, widgetName, "Panel", "Ogre/DebugTexOverlay");
        }
        w->getOverlayElement()->setMaterialName(matName);

    }

    void addTextureShadowDebugOverlay(TrayLocation loc, size_t num)
    {
        for (size_t i = 0; i < num; ++i)
        {
            TexturePtr shadowTex = mSceneMgr->getShadowTexture(i);
            addTextureDebugOverlay(loc, shadowTex, i);

        }

    }
    """
        
    def buildDepthShadowMaterial(self, textureName):
        matName = "DepthShadows/" + textureName

        ret = ogre.MaterialManager.getSingleton().getByName(matName)
        if ret.isNull():
            baseMat = ogre.MaterialManager.getSingleton().getByName("Ogre/shadow/depth/integrated/pssm")
            ret = baseMat.clone(matName)
            p = ret.getTechnique(0).getPass(0)
            p.getTextureUnitState("diffuse").setTextureName(textureName)

            splitPoints = ogre.Vector4()
            # XXX: castAsPSSMShadowCameraSetup?
            #const PSSMShadowCameraSetup::SplitPointList& splitPointList = 
            #    static_cast<PSSMShadowCameraSetup*>(mPSSMSetup.get())->getSplitPoints();
            splitPointList = mPSSMSetup.get().getSplitPoints()
            for i in range(3):
                splitPoints[i] = splitPointList[i]
            p.getFragmentProgramParameters().setNamedConstant("pssmSplitPoints", splitPoints)

        return ret;

    def changeShadows(self):
        self.configureShadows(self.shadowMode != NewTerrain.SHADOWS_NONE, self.shadowMode == NewTerrain.SHADOWS_DEPTH)

    def configureShadows(self, enabled, depthShadows):
        # XXX: castAsSM2Profile?
        """
        TerrainMaterialGeneratorA::SM2Profile* matProfile = 
            static_cast<TerrainMaterialGeneratorA::SM2Profile*>(TerrainGlobalOptions::getDefaultMaterialGenerator()->getActiveProfile());
        """
        matProfile = ogreterrain.TerrainGlobalOptions.getDefaultMaterialGenerator().getActiveProfile()
        matProfile.setReceiveDynamicShadowsEnabled(enabled);
        SHADOWS_IN_LOW_LOD_MATERIAL = True
        if SHADOWS_IN_LOW_LOD_MATERIAL:
            matProfile.setReceiveDynamicShadowsLowLod(True)
        else:
            matProfile.setReceiveDynamicShadowsLowLod(False)

        for i in self.houseList:
            i.setMaterialName("Examples/TudorHouse")

        if enabled:
            #// General scene setup
            self.sceneMgr.setShadowTechnique(ogre.SHADOWTYPE_TEXTURE_ADDITIVE_INTEGRATED)
            self.sceneMgr.setShadowFarDistance(3000)

            #// 3 textures per directional light (PSSM)
            self.sceneMgr.setShadowTextureCountPerLightType(ogre.Light.LT_DIRECTIONAL, 3)

            if self.pssmSetup.isNull():
                #// shadow camera setup
                pssmSetup = ogre.PSSMShadowCameraSetup()
                pssmSetup.setSplitPadding(self.camera.getNearClipDistance())
                pssmSetup.calculateSplitPoints(3, self.camera.getNearClipDistance(), self.sceneMgr.getShadowFarDistance())
                pssmSetup.setOptimalAdjustFactor(0, 2)
                pssmSetup.setOptimalAdjustFactor(1, 1)
                pssmSetup.setOptimalAdjustFactor(2, 0.5)
                self.pssmSetup.bind(pssmSetup);

            self.sceneMgr.setShadowCameraSetup(self.pssmSetup)

            if depthShadows:
                self.sceneMgr.setShadowTextureCount(3)
                self.sceneMgr.setShadowTextureConfig(0, 2048, 2048, ogre.PF_FLOAT32_R)
                self.sceneMgr.setShadowTextureConfig(1, 1024, 1024, ogre.PF_FLOAT32_R)
                self.sceneMgr.setShadowTextureConfig(2, 1024, 1024, ogre.PF_FLOAT32_R)
                self.sceneMgr.setShadowTextureSelfShadow(True)
                self.sceneMgr.setShadowCasterRenderBackFaces(True)
                self.sceneMgr.setShadowTextureCasterMaterial("PSSM/shadow_caster")

                houseMat = buildDepthShadowMaterial("fw12b.jpg")
                for i in self.houseList:
                    i.setMaterial(houseMat)

            else:
                self.sceneMgr.setShadowTextureCount(3)
                self.sceneMgr.setShadowTextureConfig(0, 2048, 2048, PF_X8B8G8R8)
                self.sceneMgr.setShadowTextureConfig(1, 1024, 1024, PF_X8B8G8R8)
                self.sceneMgr.setShadowTextureConfig(2, 1024, 1024, PF_X8B8G8R8)
                self.sceneMgr.setShadowTextureSelfShadow(False)
                self.sceneMgr.setShadowCasterRenderBackFaces(False)
                self.sceneMgr.setShadowTextureCasterMaterial("") # XXX: I'm not sure if it's done right. it was StringUtil::BLANK originally.

            matProfile.setReceiveDynamicShadowsDepth(depthShadows)
            #matProfile.setReceiveDynamicShadowsPSSM(static_cast<PSSMShadowCameraSetup*>(mPSSMSetup.get()))
            matProfile.setReceiveDynamicShadowsPSSM(self.pssmSetup.get())

            #//addTextureShadowDebugOverlay(TL_RIGHT, 3);

        else:
            self.sceneMgr.setShadowTechnique(ogre.SHADOWTYPE_NONE)


    """
    /*-----------------------------------------------------------------------------
    | Extends setupView to change some initial camera settings for this sample.
    -----------------------------------------------------------------------------*/
    """
    def setupView(self):
        self.camera.setPosition(self.terrainPos + ogre.Vector3(1683, 50, 2116))
        self.camera.lookAt(ogre.Vector3(1963, 50, 1660))
        self.camera.setNearClipDistance(0.1)
        self.camera.setFarClipDistance(50000)

        if self.root.getRenderSystem().getCapabilities().hasCapability(ogre.RSC_INFINITE_FAR_PLANE):
            self.camera.setFarClipDistance(0)#   // enable infinite far clip distance if we can

    def setupContent(self):
        blankTerrain = False
        #//blankTerrain = true;

        self.editMarker = self.sceneMgr.createEntity("editMarker", "sphere.mesh")
        self.editNode = self.sceneMgr.getRootSceneNode().createChildSceneNode()
        self.editNode.attachObject(self.editMarker)
        self.editNode.setScale(0.05, 0.05, 0.05)

        ogre.MaterialManager.getSingleton().setDefaultTextureFiltering(ogre.TFO_ANISOTROPIC)
        ogre.MaterialManager.getSingleton().setDefaultAnisotropy(7)

        self.sceneMgr.setFog(ogre.FOG_LINEAR, ogre.ColourValue(0.7, 0.7, 0.8), 0, 10000, 25000)

        lightdir = ogre.Vector3(0.55, -0.3, 0.75)
        lightdir.normalise()


        l = self.sceneMgr.createLight("tstLight")
        l.setType(ogre.Light.LT_DIRECTIONAL)
        l.setDirection(lightdir)
        l.setDiffuseColour(ogre.ColourValue(1.0, 1.0, 1.0))
        l.setSpecularColour(ogre.ColourValue(0.4, 0.4, 0.4))

        self.sceneMgr.setAmbientLight(ogre.ColourValue(0.2, 0.2, 0.2))


        self.terrainGroup = ogreterrain.TerrainGroup(self.sceneMgr, ogreterrain.Terrain.ALIGN_X_Z, NewTerrain.TERRAIN_SIZE, NewTerrain.TERRAIN_WORLD_SIZE)
        self.terrainGroup.setFilenameConvention(NewTerrain.TERRAIN_FILE_PREFIX, NewTerrain.TERRAIN_FILE_SUFFIX)
        self.terrainGroup.setOrigin(self.terrainPos)

        self.configureTerrainDefaults(l)
        if self.paging:
            #// Paging setup
            self.pageManager = ogrepaging.PageManager()
            #// Since we're not loading any pages from .page files, we need a way just 
            #// to say we've loaded them without them actually being loaded
            self.pageManager.setPageProvider(self.dummyPageProvider)
            self.pageManager.addCamera(self.camera)
            self.terrainPaging = ogrepaging.TerrainPaging(self.pageManager)
            world = self.pageManager.createWorld()
            self.terrainPaging.createWorldSection(world, self.terrainGroup, 2000, 3000, 
                NewTerrain.TERRAIN_PAGE_MIN_X, NewTerrain.TERRAIN_PAGE_MIN_Y, 
                NewTerrain.TERRAIN_PAGE_MAX_X, NewTerrain.TERRAIN_PAGE_MAX_Y)
        else:
            x = NewTerrain.TERRAIN_PAGE_MIN_X
            while x <= NewTerrain.TERRAIN_PAGE_MAX_X:
                while y <= NewTerrain.TERRAIN_PAGE_MAX_Y:
                    self.defineTerrain(x, y, blankTerrain)
                    y += 1
                x += 1
            #// sync load since we want everything in place when we start
            self.terrainGroup.loadAllTerrains(True)

        if self.terrainsImported:
            ti = self.terrainGroup.getTerrainIterator()
            while ti.hasMoreElements():
                t = ti.getNext().instance
                self.initBlendMaps(t)

        self.terrainGroup.freeTemporaryResources()



        #// create a few entities on the terrain
        e = self.sceneMgr.createEntity("tudorhouse.mesh")
        entPos = ogre.Vector3(self.terrainPos.x + 2043, 0, self.terrainPos.z + 1715)
        rot = ogre.Quaternion()
        entPos.y = self.terrainGroup.getHeightAtWorldPosition(entPos) + 65.5
        rot.FromAngleAxis(ogre.Degree(random.randrange(-180.0, 180.0, int=float)), ogre.Vector3().UNIT_Y)
        sn = self.sceneMgr.getRootSceneNode().createChildSceneNode(entPos, rot)
        sn.setScale(Vector3(0.12, 0.12, 0.12))
        sn.attachObject(e)
        self.houseList += [e]

        e = self.sceneMgr.createEntity("tudorhouse.mesh")
        entPos = ogre.Vector3(self.terrainPos.x + 1850, 0, self.terrainPos.z + 1478)
        rot = ogre.Quaternion()
        entPos.y = self.terrainGroup.getHeightAtWorldPosition(entPos) + 65.5
        rot.FromAngleAxis(ogre.Degree(random.randrange(-180.0, 180.0, int=float)), ogre.Vector3().UNIT_Y)
        sn = self.sceneMgr.getRootSceneNode().createChildSceneNode(entPos, rot)
        sn.setScale(Vector3(0.12, 0.12, 0.12))
        sn.attachObject(e)
        self.houseList += [e]

        e = self.sceneMgr.createEntity("tudorhouse.mesh")
        entPos = ogre.Vector3(self.terrainPos.x + 1970, 0, self.terrainPos.z + 2180)
        rot = ogre.Quaternion()
        entPos.y = self.terrainGroup.getHeightAtWorldPosition(entPos) + 65.5
        rot.FromAngleAxis(ogre.Degree(random.randrange(-180.0, 180.0, int=float)), ogre.Vector3().UNIT_Y)
        sn = self.sceneMgr.getRootSceneNode().createChildSceneNode(entPos, rot)
        sn.setScale(Vector3(0.12, 0.12, 0.12))
        sn.attachObject(e)
        self.houseList += [e]

        self.sceneMgr.setSkyBox(True, "Examples/CloudyNoonSkyBox")


class Scene(object):
    def __init__(self, gameRoot):
        self.gameRoot = gameRoot

    def GetOgreSceneManager(self):
        return self.sceneManager
    def OnGameRootInit(self):
        self.ogreRoot = self.gameRoot.GetOgreRoot()
        self.sceneManager = self.ogreRoot.createSceneManager(ogre.ST_GENERIC)
        #self.sceneManager = self.ogreRoot.createSceneManager(ogre.ST_EXTERIOR_CLOSE)

        def CreateCamera():
            camera = self.sceneManager.createCamera("PlayerCam")
            cameraNode = self.sceneManager.getRootSceneNode().createChildSceneNode("PlayerCamNode")
            cameraNode.attachObject(camera)
            cameraNode.setFixedYawAxis(True)
            camera.setNearClipDistance(2)
            camera.setFarClipDistance(1000)

            defNodeOrient = cameraNode.getOrientation()
            return camera, cameraNode, defNodeOrient

        
        self.gameCamera = GameCamera(self, *CreateCamera())

        self.rn = self.sceneManager.getRootSceneNode()

        # Set ambient light
        self.sceneManager.setAmbientLight(ogre.ColourValue(0.8, 0.8, 0.8))

        # Fog
        # NB it's VERY important to set this before calling setWorldGeometry 
        # because the vertex program picked will be different
        fadeColour = ogre.ColourValue(0.101, 0.125, 0.1836)
        #self.sceneManager.setFog(ogre.FOG_LINEAR, fadeColour, 0.001, 500, 1000)
        renderWindow = self.ogreRoot.getAutoCreatedWindow()
        renderWindow.getViewport(0).setBackgroundColour(fadeColour)

        #terrain_cfg = "terrain.cfg"
        #self.sceneManager.setWorldGeometry(terrain_cfg)

        self.terrain = NewTerrain(self.sceneManager, self)



    def GetTerrain(self):
        return self.terrain
    def GetCamera(self):
        return self.gameCamera
    def GetGameRoot(self):
        return self.gameRoot
    def GetCameraToViewportRay(self, pos_w, pos_h):
        return self.gameCamera.camera.getCameraToViewportRay(pos_w, pos_h)
    def GetOgreSceneManager(self):
        return self.sceneManager


class OgreApplication(object):
    app_title = "New Terrain"
    def Init(self):
        def _InitOgre():
            # create root
            self.ogreRoot = ogre.Root()

            # Read the resources.cfg file and add all resource locations in it
            cf = ogre.ConfigFile()
            cf.load("resources.cfg")
            seci = cf.getSectionIterator()
            while seci.hasMoreElements():
                secName = seci.peekNextKey()
                settings = seci.getNext()

                for item in settings:
                    typeName = item.key
                    archName = item.value
                    ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName)

            # Show the config dialog if we don't yet have an ogre.cfg file
            if not self.ogreRoot.restoreConfig() and not self.ogreRoot.showConfigDialog():
                raise Exception("User canceled config dialog! (setupRenderSystem)")

            # createRenderWindow
            self.ogreRoot.initialise(True, self.app_title)

            # initializeResourceGroups
            ogre.TextureManager.getSingleton().setDefaultNumMipmaps(3)
            ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()

            # initialise event listener
            self.eventListener = OgreEventListener(self, self.ogreRoot.getAutoCreatedWindow(), True, True, False)
            self.ogreRoot.addFrameListener(self.eventListener)

        _InitOgre()
        self.gameRoot = GameRoot(self.ogreRoot, self.eventListener)

    def Launch(self):
        self.Init()
        self.ogreRoot.startRendering()

    def GetGameRoot(self):
        return self.gameRoot

def main():
    try:
        app = OgreApplication()
        app.Launch()
    except ogre.OgreException, e:
        print e

if __name__ == '__main__':
    main()



