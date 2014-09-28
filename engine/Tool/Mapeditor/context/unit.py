#Decorator Context Options

from engine import debug, shared
from ogre.gui.CEGUI import MouseCursor
from string import split

class context():
	def __init__(self):
		self.options=["Remove", "Duplicate", "Properties", "Script", "Entity Editor"]
		self.optfunc=[self.sRemove, self.sDupe, self.sProp, self.sScript, self.sEntEditor]

	def sRemove(self):
		print("____________________________________")
		print("____________________________________")
		print("____________________________________")
		for x in self.getUnits():
			print x
			shared.decHandeler.Remove(x.ID, prefix="unit")

	def sDupe(self):
		Units=self.getUnits()
		Position=Units[len(Units)-1].entity.node.getPosition()
		PosTup=(Position.x, Position.y, Position.z)
		shared.decHandeler.CreateCustomPrefix(Units[len(Units)-1].entity.Type, pos=PosTup, prefix="unit")

	def sProp(self):
		self.units = self.getUnits()
		print(self.units)
		if len(self.units)!=0:
			self.unit = self.units[0]
			print(self.unit)
			print(self.unit.name)
			print(self.unit.entity)
			try:
				print(self.unit._mapeditorValues)
				layout={"General": {"Owner":"int"}, "EAttributes":{"Inital": "str"}}

				config={"General": {"Owner":self.unit._mapeditorValues["pidowner"]}, "EAttributes": {"Inital": self.unit._mapeditorValues["attribs"]}}
				shared.globalGUI.OptionsGUI.ask("Unit Properties", self.callbackProp, layout, config)
			except:
				pass

	def callbackProp(self, config):
		for section, keys in config.iteritems():
			print("["+section+"]")

			for key, value in keys.iteritems():
				print(key+"="+str(value))
				if key == "Owner":
					for x in self.units:
						x._mapeditorValues["pidowner"] = value

				if key == "Inital":
					for x in self.units:
						x._mapeditorValues["attribs"] = value
						# for y in value:
						# 	akey, avalue = split(y,"=")
						# 	x.

		#shared.Mapfile.MapConfig=textvalidator.convertConfig(config)

	def sScript(self):
		pass

	def sEntEditor(self):
		pass

	def getUnits(self):
		if not shared.DirectorManager.Mapeditor.CurrentSelection==None:
			if not len(shared.DirectorManager.Mapeditor.CurrentSelection)==0:
				return shared.DirectorManager.Mapeditor.CurrentSelection
		
		shared.render3dSelectStuff.clearSelection()
		shared.render3dSelectStuff.startSelection(shared.globalGUI.ContextMenu.rightclickpos)
		shared.render3dSelectStuff.endSelection()
		return shared.DirectorManager.Mapeditor.CurrentSelection

	def getUnitByRay(self):
		self.dimh, self.dimv = shared.render3dCamera.getDimensions()
		print("Raybeens")
		mousePos = MouseCursor.getSingleton().getPosition()
		mouseRay = shared.render3dCamera.camera.getCameraToViewportRay(mousePos.d_x / float(self.dimh),
													  mousePos.d_y / float(self.dimv))
		self.raySceneQuery.setRay(mouseRay)
		self.raySceneQuery.setSortByDistance(True)
		result = self.raySceneQuery.execute()
		if len(result)>0:
			for item in result:
				print "____________________________________"
				print item.movable.getName()
				print item.movable.getParentSceneNode().getName()
				Decorator=shared.decHandeler.GetAll(item.movable.getName())
				return Decorator