
from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

class UnitOpt():
	def __init__(self):
		#Setup pointers
		self.windowManager = CEGUI.WindowManager.getSingleton()

		self.Window=self.windowManager.getWindow("Root/UnitOpt")
		self.Background=self.windowManager.getWindow("Root/UnitOpt/BG")
		self.Actions=self.windowManager.getWindow("Root/UnitOpt/BG/Actions")
		self.Upgrades=self.windowManager.getWindow("Root/UnitOpt/BG/Upgrades")

		#Create "ActionButtons"
		self.actionbuttons=range(14)
		space=0.01380952380952381
		borderv=0.028
		btnh=0.12904761904761903
		btnv=0.46333333333333333
		fv=borderv
		fh=space
		foo=0
		buttonid = 0
		#Top row
		while foo<7:
			fh=space+foo*(btnh+space)
			self.actionbuttons[buttonid] = self.windowManager.createWindow("TaharezLook/Button", "Root/UnitOpt/BG/Actions/"+str(foo))
			self.actionbuttons[buttonid].setText("Act "+str(foo))
			self.actionbuttons[buttonid].setPosition(CEGUI.UVector2(CEGUI.UDim(fh, 0), CEGUI.UDim(fv, 0)))
			self.actionbuttons[buttonid].setSize(CEGUI.UVector2(CEGUI.UDim(btnh, 0), CEGUI.UDim(btnv, 0)))
			self.actionbuttons[buttonid].subscribeEvent(self.actionbuttons[buttonid].EventMouseButtonDown, self, "Act_Mclick")
			self.actionbuttons[buttonid].hide()
			self.Actions.addChildWindow(self.actionbuttons[buttonid])
			foo+=1
			buttonid+=1

		fv=borderv+btnv+space
		fh=space
		foo=0
		#Bottom row
		while foo<7:
			fh=space+foo*(btnh+space)
			self.actionbuttons[buttonid] = self.windowManager.createWindow("TaharezLook/Button", "Root/UnitOpt/BG/Actions/"+str(foo+7))
			self.actionbuttons[buttonid].setText("Act "+str(foo+7))
			self.actionbuttons[buttonid].setPosition(CEGUI.UVector2(CEGUI.UDim(fh, 0), CEGUI.UDim(fv, 0)))
			self.actionbuttons[buttonid].setSize(CEGUI.UVector2(CEGUI.UDim(btnh, 0), CEGUI.UDim(btnv, 0)))
			self.actionbuttons[buttonid].subscribeEvent(self.actionbuttons[buttonid].EventMouseButtonDown, self, "Act_Mclick")
			self.actionbuttons[buttonid].hide()
			self.Actions.addChildWindow(self.actionbuttons[buttonid])
			foo+=1
			buttonid+=1

		#Create "UpgradeImages"
		self.upgradeimages=range(9)
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
				self.upgradeimages[foo] = self.windowManager.createWindow("TaharezLook/StaticImage", "Root/UnitOpt/BG/Upgrades/"+str(foobar))
				#self.upgradeimages[foo].setText("U"+str(foobar))
				self.upgradeimages[foo].setPosition(CEGUI.UVector2(CEGUI.UDim(fh, 0), CEGUI.UDim(fv, 0)))
				self.upgradeimages[foo].setSize(CEGUI.UVector2(CEGUI.UDim(btnh, 0), CEGUI.UDim(btnv, 0)))
				self.upgradeimages[foo].subscribeEvent(self.upgradeimages[foo].EventMouseButtonDown, self, "Upg_Mclick")
				self.Upgrades.addChildWindow(self.upgradeimages[foo])
				foo+=1
				foobar+=1
			fv=borderv+btnv+bar*(btnv)
			bar+=1

		shared.renderGUI.registerLayout(self.Window)

	def Act_Mclick(self, evt):
		if evt.button==CEGUI.LeftButton:
			if self.currentgroup!=None:
				#print(self.buttonindex)
				for buttonid, buttondata in self.buttonindex.iteritems():
					actionid, button = buttondata
					print "Buttans"
					print buttondata
					if evt.window.getText() == button.getText():
						print(buttonid)
						print(button.getID())
						print(evt.window.getID())
						self.currentgroup.guiAddAction(actionid)
					print(evt.window.getID(), button.getID())

	def updateActions(self, group, buttonlist):
		self.buttonindex={}
		self.buttonstaken=[]
		self.placelater=[]
		self.currentgroup = group
		if group!=None:
			for title, tooltip, position, actionid in buttonlist:
				if position==None:
					self.placelater.append((title, tooltip, position, actionid))

				elif position==False and type(position)!=int:
					pass

				elif position<14:
					if position not in self.buttonstaken:

						self.actionbuttons[position].setText(title)
						self.actionbuttons[position].setTooltipText(tooltip)
						self.actionbuttons[position].show()
						#print("\n\n\n\n\n\n")
						print(self.actionbuttons[position])
						self.buttonindex[position]=(actionid, self.actionbuttons[position])
						self.buttonstaken.append(position)
						
					else:
						shared.DPrint("UnitOpt", 2, "Button Position: "+str(position)+" requested by actionid: "+str(actionid)+" is already taken!")
						self.placelater.append((title, tooltip, position, actionid))

			for title, tooltip, position, actionid in self.placelater:
				for x in xrange(0, 15):
					if x not in self.buttonstaken:
						self.actionbuttons[x].setText(title)
						self.actionbuttons[x].setTooltipText(tooltip)
						self.actionbuttons[x].show()
						self.buttonindex[x]=(actionid, self.actionbuttons[x])
						self.buttonstaken.append(x)
						break
		else:
			for button in self.actionbuttons:
				button.hide()


	def Upg_Mclick(self, evt):
		pass