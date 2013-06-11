#OptionsGUI
#The OptionsGUI is a template for setting options
#It takes a dictionary and a caller as input, and calls the caller with the answers when the user clicks OK

from engine import shared, debug
from engine.Lib import textvalidator
from string import split
import ogre.gui.CEGUI as CEGUI

class GUI():
	def __init__(self):
		self.root = shared.renderGUI.windowManager.getWindow("Root")
		self.layout = shared.renderGUI.windowManager.loadWindowLayout("OptionsT.layout")

		self.layout.setProperty("Text", "Options")
		self.root.addChildWindow(self.layout)
		self.layout.setPosition(CEGUI.UVector2(CEGUI.UDim(0.30, 0), CEGUI.UDim(0.20, 0)))
		shared.globalGUI.registerLayout(self.layout)
		#self.layout.hide()

		self.Window=shared.renderGUI.windowManager.getWindow("Options")
		self.Sidebar=shared.renderGUI.windowManager.getWindow("Options/Sidebar")
		self.Desc=shared.renderGUI.windowManager.getWindow("Options/Desc")
		self.Opt=shared.renderGUI.windowManager.getWindow("Options/Opt")

		self.Apply=shared.renderGUI.windowManager.getWindow("Options/Sidebar/Apply")
		self.Cancel=shared.renderGUI.windowManager.getWindow("Options/Sidebar/Cancel")

		self.Apply.subscribeEvent(self.Apply.EventMouseButtonDown, self, "ApplyClick")
		self.Cancel.subscribeEvent(self.Cancel.EventMouseButtonDown, self, "CancelClick")

		self.SidebarItems=[]
		self.DescItems=[]
		self.OptItems=[]

		self.CurrentLayout={}
		

	def ask(self, title, callback, layout, config):
		self.layout.setProperty("Text", title)
		self.CurrentLayout=layout
		self.CurrentConfig=config
		self.Callback=callback
		self.SidebarItems=[]
		self.CurrentSection=None

		for name, content in layout.iteritems():
			print(name)
			item=shared.renderGUI.windowManager.createWindow("Vanilla/Button", "Options/Sidebar/"+name)
			item.setSize(CEGUI.UVector2(CEGUI.UDim(1, 0), CEGUI.UDim(0.10, 0)))
			item.setPosition(CEGUI.UVector2(CEGUI.UDim(0, 0), CEGUI.UDim(len(self.SidebarItems)*0.10, 0)))
			item.setText(name)

			item.subscribeEvent(item.EventMouseButtonDown, self, "sectionButtonClick")

			item.show()

			self.Sidebar.addChildWindow(item)
			shared.globalGUI.registerLayout(item)
			self.SidebarItems.append(item)

			if self.CurrentSection==None:
				self.CurrentSection=name
				self.CurrentContent=content

			print(content)

		self.updateContent()
		self.layout.show()

		shared.renderioInput.CurrentKeyInterface=1
		shared.renderioInput.takeKeyFocus("optionsgui")

	def updateContent(self):
		for item in self.DescItems:
			item.destroy()
		for item in self.OptItems:
			item.destroy()

		self.DescItems=[]
		self.OptItems=[]

		for Cname, option in self.CurrentContent.iteritems():
			print(Cname)
			text=shared.renderGUI.windowManager.createWindow("Vanilla/StaticText", "Options/Desc/"+str(Cname))
			text.setSize(CEGUI.UVector2(CEGUI.UDim(1, 0), CEGUI.UDim(0.10, 0)))
			text.setPosition(CEGUI.UVector2(CEGUI.UDim(0, 0), CEGUI.UDim(len(self.DescItems)*0.10, 0)))
			text.setText(str(Cname))
			text.show()

			self.Desc.addChildWindow(text)
			shared.globalGUI.registerLayout(text)
			self.DescItems.append(text)

			choice=shared.renderGUI.windowManager.createWindow("Vanilla/Editbox", "Options/Opt/"+str(Cname))
			choice.setSize(CEGUI.UVector2(CEGUI.UDim(1, 0), CEGUI.UDim(0.10, 0)))
			choice.setPosition(CEGUI.UVector2(CEGUI.UDim(0, 0), CEGUI.UDim(len(self.OptItems)*0.10, 0)))
			choice.setText(str(self.CurrentConfig[self.CurrentSection][Cname]))

			choice.subscribeEvent(choice.EventTextAccepted, self, "validateField")
			choice.subscribeEvent(choice.EventDeactivated, self, "validateField")


			choice.show()

			self.Opt.addChildWindow(choice)
			shared.globalGUI.registerLayout(choice)
			self.OptItems.append(choice)

	def validateField(self, evt):
		fieldname = split(str(evt.window.getName()),"/")[2]
		textinput = str(evt.window.getText())
		validator = self.CurrentLayout[self.CurrentSection][fieldname]

		Valid=textvalidator.Validate(textinput, validator)
		if Valid!=None:
			print("Validated: "+fieldname+"="+textinput)
			self.CurrentConfig[self.CurrentSection][fieldname]=textinput
		else:
			print("Field is not valid!")
			evt.window.activate()

	def sectionButtonClick(self, evt):
		self.CurrentSection=split(str(evt.window.getName()),"/")[2]
		self.CurrentContent=self.CurrentLayout[self.CurrentSection]
		self.updateContent()

	def ApplyClick(self, evt):
		self.Callback(self.CurrentConfig)
		self.hide()

	def CancelClick(self, evt):
		self.hide()

	def hide(self):
		self.layout.hide()
		shared.renderioInput.looseKeyFocus("optionsgui")
		for x in self.SidebarItems:
			x.destroy()

		self.SidebarItems=[]