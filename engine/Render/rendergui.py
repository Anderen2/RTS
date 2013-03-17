#Rendermodule - rendergui
#Classes for rendering 2D GUI upon the 3D renderer

from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class GUI():
	def __init__(self):
		self.root=shared.renderRoot
		self.scene=shared.render3dScene
		self.UnitHandeler=shared.unitHandeler
		UDim=CEGUI.UDim

	def Setup(self):
		shared.DPrint("RenderGUI",1,"Setting up CEGUI")
		#Setup varibles
		self.MoveInterface=None
		self.hackhz, self.hackvz = shared.render3dCamera.getDimensions()
		self.globalpha=0.9
		self.upperalpha=0.5

		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton
		#self.sceneManager = self.scene.sceneManager
		#self.renderWindow = self.root.getAutoCreatedWindow()
		#self.ceguiSystem=CEGUI.System.getSingleton()
		#self.resourceProvider = CEGUI.DefaultResourceProvider()

		# CEGUI setup
		if CEGUI.Version__.startswith("0.6"):
			self.renderer = CEGUI.OgreCEGUIRenderer(renderWindow, ogre.RENDER_QUEUE_OVERLAY, False, 3000, self.sceneManager)
			self.system = CEGUI.System(self.renderer)
			CEGUI.SchemeManager.getSingleton().loadScheme("TaharezLookSkin.scheme")
			CEGUI.SchemeManager.getSingleton().loadScheme("VanillaSkin.scheme")
		else:
			self.renderer = CEGUI.OgreRenderer.bootstrapSystem()
			self.system = CEGUI.System.getSingleton()
			CEGUI.SchemeManager.getSingleton().create("TaharezLookSkin.scheme")
			CEGUI.SchemeManager.getSingleton().create("VanillaSkin.scheme")

		#Loading Layouts
		self.sheet = CEGUI.WindowManager.getSingleton().loadWindowLayout("RTS.layout")
		self.NoSel = CEGUI.WindowManager.getSingleton().loadWindowLayout("NoSel.layout")
		self.UnitQueue = CEGUI.WindowManager.getSingleton().loadWindowLayout("UnitQueue.layout")

		self.system.setGUISheet(self.sheet)
		self.windowManager().getWindow("Root/UnitInfo").addChildWindow(self.UnitQueue)
		self.windowManager().getWindow("Root/UnitInfo").addChildWindow(self.NoSel)

		#Setup Defaults
		self.system.setDefaultMouseCursor("TaharezLook", "MouseArrow")
		self.system.setDefaultFont("BlueHighway-12")
		CEGUI.MouseCursor.getSingleton().setImage("TaharezLook", "MouseArrow")

		#Load minimap
		Ist=CEGUI.ImagesetManager.getSingleton().createFromImageFile("minimapset", "./minimap.png")
		Ist.defineImage("minimap", CEGUI.Vector2(0,0), CEGUI.Size(290,290),CEGUI.Vector2(0,0))

		#Create the rest of the gui elements
		self.CreateGuiElements()

		#Setup the gui elements
		self.SetupGuiElements()

	def CreateGuiElements(self):
		shared.DPrint("RenderGUI",1,"Creating GUI elements")
		windowManager = CEGUI.WindowManager.getSingleton()
		#Create "ActionButtons"
		self.actionbuttons=range(14)
		foowindow=windowManager.getWindow("Root/UnitOpt/BG/Actions")
		space=0.01380952380952381
		borderv=0.028
		btnh=0.12904761904761903
		btnv=0.46333333333333333
		fv=borderv
		fh=space
		foo=0
		while foo<7:
			fh=space+foo*(btnh+space)
			self.actionbuttons[foo] = windowManager.createWindow("TaharezLook/Button", "Root/UnitOpt/BG/Actions/"+str(foo))
			self.actionbuttons[foo].setText("Act "+str(foo))
			self.actionbuttons[foo].setPosition(CEGUI.UVector2(CEGUI.UDim(fh, 0), CEGUI.UDim(fv, 0)))
			self.actionbuttons[foo].setSize(CEGUI.UVector2(CEGUI.UDim(btnh, 0), CEGUI.UDim(btnv, 0)))
			self.actionbuttons[foo].subscribeEvent(self.actionbuttons[foo].EventMouseButtonDown, self, "Act_Mclick")
			foowindow.addChildWindow(self.actionbuttons[foo])
			foo+=1

		fv=borderv+btnv+space
		fh=space
		foo=0
		while foo<7:
			fh=space+foo*(btnh+space)
			self.actionbuttons[foo] = windowManager.createWindow("TaharezLook/Button", "Root/UnitOpt/BG/Actions/"+str(foo+7))
			self.actionbuttons[foo].setText("Act "+str(foo+7))
			self.actionbuttons[foo].setPosition(CEGUI.UVector2(CEGUI.UDim(fh, 0), CEGUI.UDim(fv, 0)))
			self.actionbuttons[foo].setSize(CEGUI.UVector2(CEGUI.UDim(btnh, 0), CEGUI.UDim(btnv, 0)))
			self.actionbuttons[foo].subscribeEvent(self.actionbuttons[foo].EventMouseButtonDown, self, "Act_Mclick")
			foowindow.addChildWindow(self.actionbuttons[foo])
			foo+=1

		#Create "UpgradeImages"
		self.upgradeimages=range(9)
		foowindow=windowManager.getWindow("Root/UnitOpt/BG/Upgrades")
		borderh=0.036923076923076925
		borderv=0.028
		btnh=0.3076923076923077
		btnv=0.31
		fv=borderv
		fh=borderh
		bar=0
		foobar=0
		while bar<3:
			foo=0
			while foo<3:
				fh=borderh+foo*(btnh)
				self.upgradeimages[foo] = windowManager.createWindow("TaharezLook/StaticImage", "Root/UnitOpt/BG/Upgrades/"+str(foobar))
				#self.upgradeimages[foo].setText("U"+str(foobar))
				self.upgradeimages[foo].setPosition(CEGUI.UVector2(CEGUI.UDim(fh, 0), CEGUI.UDim(fv, 0)))
				self.upgradeimages[foo].setSize(CEGUI.UVector2(CEGUI.UDim(btnh, 0), CEGUI.UDim(btnv, 0)))
				self.upgradeimages[foo].subscribeEvent(self.upgradeimages[foo].EventMouseButtonDown, self, "Upg_Mclick")
				foowindow.addChildWindow(self.upgradeimages[foo])
				foo+=1
				foobar+=1
			fv=borderv+btnv+bar*(btnv)
			bar+=1

	def SetupGuiElements(self):
		shared.DPrint("RenderGUI",1,"Setting up Gui Elements")
		windowManager = CEGUI.WindowManager.getSingleton()
		self.windowManager = CEGUI.WindowManager.getSingleton()
		#Loop through all the windows to apply movement, and hover feedback functionality
		windowlist=["Root/Map", "Root/Options", "Root/Tactical", "Root/UnitInfo", "Root/Chat", "Root/GameInfo", "Root/UnitOpt", "Root/Power", "Root/Money"]
		for x in windowlist:
			foo=windowManager.getWindow(x)
			foo.subscribeEvent(foo.EventMouseEnters, self, "W_Menter")
			foo.subscribeEvent(foo.EventMouseLeaves, self, "W_Mleave")
			foo.subscribeEvent(foo.EventMouseButtonDown, self, "W_Mclick")
			foo.subscribeEvent(foo.EventMouseButtonUp, self, "W_Mrelease")
			foo.subscribeEvent(foo.EventMouseMove, self, "MouseMoving")
			foo.setAlpha(self.globalpha)
			foobar=windowManager.getWindow(x+"/BG")
			foobar.setProperty("Image","set:guibgset image:guibgs")
			bar=0
			while bar<foo.getChildCount():
				foo2=foo.getChildAtIdx(bar)
				#shared.DPrint(3,0,"Setting up: "+foo2.getName())
				foo2.subscribeEvent(foo2.EventMouseEnters, self, "W_Menter")
				foo2.subscribeEvent(foo2.EventMouseLeaves, self, "W_Mleave")
				foo2.subscribeEvent(foo2.EventMouseButtonDown, self, "W_Mclick")
				foo2.subscribeEvent(foo2.EventMouseButtonUp, self, "W_Mrelease")
				foo2.subscribeEvent(foo2.EventMouseMove, self, "MouseMoving")
				bar=bar+1
				bar2=0
				while bar2<foo2.getChildCount():
					foo3=foo2.getChildAtIdx(bar2)
					#shared.DPrint(3,0,"Setting up: "+foo3.getName())
					foo3.subscribeEvent(foo3.EventMouseEnters, self, "W_Menter")
					foo3.subscribeEvent(foo3.EventMouseLeaves, self, "W_Mleave")
					foo3.subscribeEvent(foo3.EventMouseButtonDown, self, "W_Mclick")
					foo3.subscribeEvent(foo3.EventMouseButtonUp, self, "W_Mrelease")
					foo3.subscribeEvent(foo3.EventMouseMove, self, "MouseMoving")
					bar2=bar2+1
					bar3=0
					while bar3<foo3.getChildCount():
						foo4=foo3.getChildAtIdx(bar3)
						#shared.DPrint(3,0,"Setting up: "+foo4.getName())
						foo4.subscribeEvent(foo4.EventMouseEnters, self, "W_Menter")
						foo4.subscribeEvent(foo4.EventMouseLeaves, self, "W_Mleave")
						foo4.subscribeEvent(foo4.EventMouseButtonDown, self, "W_Mclick")
						foo4.subscribeEvent(foo4.EventMouseButtonUp, self, "W_Mrelease")
						foo4.subscribeEvent(foo4.EventMouseMove, self, "MouseMoving")
						foo4.setAlpha(1)
						bar3=bar3+1

		foo=windowManager.getWindow("Root")
		foo.subscribeEvent(foo.EventMouseMove, self, "MouseMoving")

		#Remove the UnitQueue sheet, as we are done looping through it
		self.windowManager.getWindow("Root/UnitInfo").removeChildWindow("Root/UnitInfo/BG/UnitQueue")

		#Set some stuff manually:

		#Optionsbuttons:
		foo=windowManager.getWindow("Root/Options/BG/0")
		foo.setProperty("NormalImage", "set:GuiSet image:arrowup")
		foo.setProperty("PushedImage", "set:GuiSet image:arrowup")
		foo.subscribeEvent(foo.EventMouseButtonDown, self, "Opt0_Mclick")
		foo=windowManager.getWindow("Root/Options/BG/1")
		foo.setProperty("NormalImage", "set:GuiSet image:bagdeinfo")
		foo.setProperty("PushedImage", "set:GuiSet image:bagdeinfo")
		foo.subscribeEvent(foo.EventMouseButtonDown, self, "Opt1_Mclick")
		foo=windowManager.getWindow("Root/Options/BG/2")
		foo.setProperty("NormalImage", "set:GuiSet image:build")
		foo.setProperty("PushedImage", "set:GuiSet image:build")
		foo.subscribeEvent(foo.EventMouseButtonDown, self, "Opt2_Mclick")
		foo=windowManager.getWindow("Root/Options/BG/3")
		foo.setProperty("NormalImage", "set:GuiSet image:user")
		foo.setProperty("PushedImage", "set:GuiSet image:user")
		foo.subscribeEvent(foo.EventMouseButtonDown, self, "Opt3_Mclick")
		foo=windowManager.getWindow("Root/Options/BG/4")
		foo.setProperty("NormalImage", "set:GuiSet image:arrowdown")
		foo.setProperty("PushedImage", "set:GuiSet image:arrowdown")
		foo.subscribeEvent(foo.EventMouseButtonDown, self, "Opt4_Mclick")

		#Tacticalbuttons
		foo=["0","1","2","3","4"]
		for x in foo:
			bar=windowManager.getWindow("Root/Tactical/BG/"+x)
			bar.subscribeEvent(bar.EventMouseButtonDown, self, "Tact"+x+"_Mclick")

		#Minimap
		foo=windowManager.getWindow( "Root/Map/BG/Image")
		foo.setProperty("Image","set:minimapset image:minimap")
		foo.subscribeEvent(foo.EventMouseEnters, self, "Map_Menter")
		foo.subscribeEvent(foo.EventMouseLeaves, self, "Map_Mleave")
		foo.subscribeEvent(foo.EventMouseButtonDown, self, "Map_Mclick")
		foo.subscribeEvent(foo.EventMouseButtonUp, self, "Map_Mrelease")

		#Powerbar
		foo=windowManager.getWindow("Root/Power/BG/Bar")
		foo.setProperty("CurrentProgress", "0.5")
		foo.subscribeEvent(foo.EventMouseButtonDown, self, "Pwr_Mclick")

		#Money
		foo=windowManager.getWindow("Root/Money/BG/Text")
		foo.setProperty("Text", "$ 9001")
		foo.subscribeEvent(foo.EventMouseButtonDown, self, "Cash_Mclick")

		#Chat
		foo=windowManager.getWindow("Root/Chat/BG/Title")
		foo.subscribeEvent(foo.EventMouseEnters, self, "Chat_Menter")
		foo.subscribeEvent(foo.EventMouseLeaves, self, "Chat_Mleave")
		foo.subscribeEvent(foo.EventMouseButtonDown, self, "Chat_TitleClick")
		foo=windowManager.getWindow("Root/Chat/BG/Type")
		foo.subscribeEvent(foo.EventMouseEnters, self, "Chat_Menter")
		foo.subscribeEvent(foo.EventMouseLeaves, self, "Chat_Mleave")
		foo=windowManager.getWindow("Root/Chat/BG/History__auto_vscrollbar__")
		foo.subscribeEvent(foo.EventMouseEnters, self, "Chat_Menter")
		foo.subscribeEvent(foo.EventMouseLeaves, self, "Chat_Mleave")
		foo=windowManager.getWindow("Root/Chat/BG/History")
		foo.subscribeEvent(foo.EventMouseEnters, self, "Chat_Menter")
		foo.subscribeEvent(foo.EventMouseLeaves, self, "Chat_Mleave")
		foo.setReadOnly(True)

		#Gameinfo
		foo=windowManager.getWindow("Root/GameInfo/BG/Title")
		foo.subscribeEvent(foo.EventMouseEnters, self, "GameInfo_Menter")
		foo.subscribeEvent(foo.EventMouseLeaves, self, "GameInfo_Mleave")
		foo.subscribeEvent(foo.EventMouseButtonDown, self, "GameInfo_TitleClick")
		foo=windowManager.getWindow("Root/GameInfo/BG/History")
		foo.subscribeEvent(foo.EventMouseEnters, self, "GameInfo_Menter")
		foo.subscribeEvent(foo.EventMouseLeaves, self, "GameInfo_Mleave")

		#Set defaultalpha for the transparent windows
		foo=windowManager.getWindow("Root/Chat")
		foo.setAlpha(0.2)
		foo=windowManager.getWindow("Root/GameInfo")
		foo.setAlpha(0.2)

		self.SetupDebugStuff()

	def SetupDebugStuff(self):
		windowManager = CEGUI.WindowManager.getSingleton()
		foowindow=windowManager.getWindow("Root")
		self.FPScounter = windowManager.createWindow("TaharezLook/StaticText", "FPScounter")
		self.FPScounter.setText("999")
		self.FPScounter.setPosition(CEGUI.UVector2(CEGUI.UDim(0.5, 0), CEGUI.UDim(0, 0)))
		self.FPScounter.setSize(CEGUI.UVector2(CEGUI.UDim(0.11, 0), CEGUI.UDim(0.05, 0)))
		foowindow.addChildWindow(self.FPScounter)

		self.DIVcounter = windowManager.createWindow("TaharezLook/StaticText", "DIVcounter")
		self.DIVcounter.setText("999")
		self.DIVcounter.setPosition(CEGUI.UVector2(CEGUI.UDim(0.3, 0), CEGUI.UDim(0, 0)))
		self.DIVcounter.setSize(CEGUI.UVector2(CEGUI.UDim(0.11, 0), CEGUI.UDim(0.05, 0)))
		foowindow.addChildWindow(self.DIVcounter)
		#self.Console()
		self.GuiStats(debug.GUISTATS)

	def Console(self):
		windowManager = CEGUI.WindowManager.getSingleton()
		foowindow=windowManager.getWindow("Root")
		if windowManager.getWindow("Root").isChild("Con"):
			windowManager.getWindow("Root/UnitInfo").removeChildWindow("Root/UnitInfo/BG/UnitQueue")
		else:
			self.conwin = CEGUI.WindowManager.getSingleton().loadWindowLayout("console.layout")
			self.windowManager().getWindow("Root").addChildWindow(self.conwin)
			self.conwin.setPosition(CEGUI.UVector2(CEGUI.UDim(0, 0), CEGUI.UDim(0, 0)))
			self.conwin.setSize(CEGUI.UVector2(CEGUI.UDim(1, 0), CEGUI.UDim(0.25, 0)))
			self.windowManager().getWindow("Con/BG/Log").setReadOnly(True)

	def MouseMoving(self, evt):
		UDim=CEGUI.UDim
		if self.MoveInterface!=None:
			mousePos = CEGUI.MouseCursor.getSingleton().getPosition()
			self.MoveInterfaceMCVec=(mousePos.d_x, mousePos.d_y)
			self.MoveInterfaceMRVec=(mousePos.d_x/self.hackhz, mousePos.d_y/self.hackvz)
			self.MoveInterfacePRVec=(evt.window.getXPosition(),evt.window.getYPosition())
			self.MoveInterfaceSZVec=(evt.window.getWidth(),evt.window.getHeight())
			self.MoveInterfaceLoVec=(self.MoveInterfaceMRVec[0]-UDim(self.MoveInterfaceSZVec[0]).d_scale,self.MoveInterfaceMRVec[1]-UDim(self.MoveInterfaceSZVec[1]).d_scale)
			self.MoveInterface.setPosition( CEGUI.UVector2( CEGUI.UDim(0,mousePos.d_x), CEGUI.UDim(0,mousePos.d_y) ))

	def W_Mclick(self, evt):
		UDim=CEGUI.UDim
		#print(evt.button)
		#print(evt.window)
		#self.MoveInterface=True
		if evt.button==CEGUI.MiddleButton:
			CEGUI.System.getSingleton().setDefaultMouseCursor("TaharezLook", "MouseMoveCursor")
			shared.DPrint("RenderGUI",0,"Clicked: "+str(evt.window.getName()))
			if evt.window.getParent().getParent().getParent().getName()!="Root":
				self.MoveInterface=evt.window.getParent().getParent().getParent()
			else:
				self.MoveInterface=evt.window.getParent().getParent()
			mousePos = CEGUI.MouseCursor.getSingleton().getPosition()
			self.MoveInterfaceMCVec=(mousePos.d_x, mousePos.d_y)
			self.MoveInterfaceMRVec=(mousePos.d_x/self.hackhz, mousePos.d_y/self.hackvz)
			self.MoveInterfacePRVec=(evt.window.getXPosition(),evt.window.getYPosition())
			self.MoveInterfaceSZVec=(evt.window.getWidth(),evt.window.getHeight())
			self.MoveInterfaceLoVec=(self.MoveInterfaceMRVec[0]-UDim(self.MoveInterfaceSZVec[0]).d_scale,self.MoveInterfaceMRVec[1]-UDim(self.MoveInterfaceSZVec[1]).d_scale)
			#print self.MoveInterfaceLoVec
			if self.MoveInterface!=None:
				self.MoveInterface.setAlpha(0.20)
			#evt.window.pickUp()
			#evt.window.setPosition(UVec(UDim(0.5,0),UDim(0.5,0)))

	def W_Mrelease(self,evt):
		if evt.button==CEGUI.MiddleButton:
			if self.MoveInterface!=None:
				self.MoveInterface.setAlpha(self.globalpha)
			CEGUI.System.getSingleton().setDefaultMouseCursor("TaharezLook", "MouseArrow")
			self.MoveInterface=None

	def W_Menter(self, evt):
		self.IgnoreMe=["Root/UnitOpt/BG/Actions","Root/UnitOpt/BG/Upgrades"]
		self.IgnoreMyParent=["Root/Chat/BG", "Root/Chat", "Root/GameInfo/BG", "Root/GameInfo"]
		shared.DPrint("RenderGUI",0,"Entered: "+str(evt.window.getName()))
		#if evt.window.getName()!="Root/UnitOpt/BG/Actions" and evt.window.getName()!="Root/UnitOpt/BG/Upgrades" and evt.window.getParent().getName()!="Root/Chat/BG" and evt.window.getParent().getName()!="Root/Chat" and evt.window.getParent().getName()!="Root/GameInfo/BG" and evt.window.getParent().getName()!="Root/GameInfo":
		if not evt.window.getName() in self.IgnoreMe:
			if not evt.window.getParent().getName() in self.IgnoreMyParent:
				evt.window.setAlpha(0.50)
		self.ActiveWindow=evt.window
 
 	def W_Mleave(self, evt):
 		#if evt.window.getName()!="Root/UnitOpt/BG/Actions" and evt.window.getName()!="Root/UnitOpt/BG/Upgrades" and evt.window.getParent().getName()!="Root/Chat/BG" and evt.window.getParent().getName()!="Root/Chat" and evt.window.getParent().getName()!="Root/GameInfo/BG" and evt.window.getParent().getName()!="Root/GameInfo":
 		if not evt.window.getName() in self.IgnoreMe:
			if not evt.window.getParent().getName() in self.IgnoreMyParent:
 				evt.window.setAlpha(1)
 		self.ActiveWindow=None

 	def Map_Menter(self, evt):
 		pass

 	def Map_Mleave(self, evt):
 		pass

 	def Map_Mclick(self, evt):
 		pass

 	def Map_Mrelease(self, evt):
 		pass

 	def Opt0_Mclick(self, evt):
 		pass

 	def Opt1_Mclick(self, evt):
 		#Map/Aliances
 		if evt.button==CEGUI.LeftButton:
 			shared.unitHandeler.CreateMov(3,1,1,"robot")

 	def Opt2_Mclick(self, evt):
 		#Nearest free worker
 		if evt.button==CEGUI.LeftButton:
 			if self.windowManager.getWindow("Root/UnitInfo").isChild("Root/UnitInfo/BG/NoSel"):
 				self.windowManager.getWindow("Root/UnitInfo").removeChildWindow("Root/UnitInfo/BG/NoSel")
 				self.windowManager.getWindow("Root/UnitInfo").addChildWindow(self.UnitQueue)
 			else:
 				self.windowManager.getWindow("Root/UnitInfo").removeChildWindow("Root/UnitInfo/BG/UnitQueue")
 				self.windowManager.getWindow("Root/UnitInfo").addChildWindow(self.NoSel)

 	def Opt3_Mclick(self, evt):
 		#Pausemenu
 		if evt.button==CEGUI.LeftButton:
 			for x in range(1,10):
 				shared.unitHandeler.CreateMov(3,1,1,"robot")

 	def Opt4_Mclick(self, evt):
 		#Hide Gui
 		pass

 	def Tact0_Mclick(self, evt):
 		pass

 	def Tact1_Mclick(self, evt):
 		pass

 	def Tact2_Mclick(self, evt):
 		pass

 	def Tact3_Mclick(self, evt):
 		pass

 	def Tact4_Mclick(self, evt):
 		pass

 	def Pwr_Mclick(self, evt):
 		if evt.button==CEGUI.LeftButton:
 			print("Overclock engaged!")

 	def Cash_Mclick(self, evt):
 		if evt.button==CEGUI.LeftButton:
 			print("Its over ninethousaaaaaaaaaaaannnddd!")

 	def Act_Mclick(self, evt):
 		if evt.button==CEGUI.LeftButton:
	 		action=str(evt.window.getName())
	 		baction=action[24:]
	 		print baction

	def Upg_Mclick(self, evt):
		pass

	def Chat_TitleClick(self, evt):
		if evt.button==CEGUI.LeftButton:
			evt.window.setText("Chat: Team")
		elif evt.button==CEGUI.RightButton:
			if self.windowManager.getWindow("Root/Chat/BG").getAlpha()!=0:
				self.windowManager.getWindow("Root/Chat/BG/Type").hide()
				self.windowManager.getWindow("Root/Chat/BG/History").hide()
				self.windowManager.getWindow("Root/Chat/BG/Title").setInheritsAlpha(False)
				self.windowManager.getWindow("Root/Chat/BG").setAlpha(0)
			else:
				self.windowManager.getWindow("Root/Chat/BG/Type").show()
				self.windowManager.getWindow("Root/Chat/BG/History").show()
				self.windowManager.getWindow("Root/Chat/BG/Title").setInheritsAlpha(True)
				self.windowManager.getWindow("Root/Chat/BG").setAlpha(1)

	def Chat_Menter(self, evt):
		if self.windowManager.getWindow("Root/Chat/BG").getAlpha()!=0:
			self.windowManager.getWindow("Root/Chat").setAlpha(1)

	def Chat_Mleave(self, evt):
		if self.windowManager.getWindow("Root/Chat/BG").getAlpha()!=0:
			self.windowManager.getWindow("Root/Chat").setAlpha(0.2)

	def GameInfo_Menter(self, evt):
		if self.windowManager.getWindow("Root/GameInfo/BG").getAlpha()!=0:
			self.windowManager.getWindow("Root/GameInfo").setAlpha(1)

	def GameInfo_Mleave(self, evt):
		if self.windowManager.getWindow("Root/GameInfo/BG").getAlpha()!=0:
			self.windowManager.getWindow("Root/GameInfo").setAlpha(0.2)

	def GameInfo_TitleClick(self, evt):
		if evt.button==CEGUI.LeftButton:
			print("This is a beta..")
			shared.DPrint("RenderGUI",0,"Beta: Wth?")
		elif evt.button==CEGUI.RightButton:
			if self.windowManager.getWindow("Root/GameInfo/BG").getAlpha()!=0:
				self.windowManager.getWindow("Root/GameInfo/BG/History").hide()
				self.windowManager.getWindow("Root/GameInfo/BG/Title").setInheritsAlpha(False)
				self.windowManager.getWindow("Root/GameInfo/BG").setAlpha(0)
			else:
				self.windowManager.getWindow("Root/GameInfo/BG/History").show()
				self.windowManager.getWindow("Root/GameInfo/BG/Title").setInheritsAlpha(True)
				self.windowManager.getWindow("Root/GameInfo/BG").setAlpha(1)

	def quitevent(self, evt):
		exit()

	def addevent(self, evt):
		shared.DPrint("RenderGUI",0,"Adding Unit")
		self.UnitHandeler.CreateMov("robot")

	def omgevent(self, evt):
		print("Omging!")

	def HideAll(self):
		self.windowManager.getWindow("Root").hide()

	def ShowAll(self):
		self.windowManager.getWindow("Root").show()

	def GuiStats(self, foo):
		if foo:
			self.windowManager.getWindow("FPScounter").show()
			self.windowManager.getWindow("DIVcounter").show()
		else:
			self.windowManager.getWindow("FPScounter").hide()
			self.windowManager.getWindow("DIVcounter").hide()