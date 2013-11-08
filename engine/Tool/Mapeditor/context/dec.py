#Decorator Context Options

from engine import debug, shared
from ogre.gui.CEGUI import MouseCursor

class contextDec():
	def __init__(self):
		self.options=["Remove", "Duplicate", "Properties", "Script", "Entity Editor"]
		self.optfunc=[self.sRemove, self.sDupe, self.sProp, self.sScript, self.sEntEditor]

	def sRemove(self):
		for x in self.getUnits():
			shared.decHandeler.Remove(x.ID)

	def sDupe(self):
		Units=self.getUnits()
		Position=Units[len(Units)-1].entity.node.getPosition()
		PosTup=(Position.x, Position.y, Position.z)
		shared.decHandeler.Create(Units[len(Units)-1].entity.Type, pos=PosTup)

	def sProp(self):
		Units=self.getUnits()
		Position=Units[len(Units)-1].entity.node.getPosition()
		PosTup=(Position.x, Position.y, Position.z)
		print("Position: (%d, %d, %d)" % (PosTup[0], PosTup[1], PosTup[2]))

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
				Decorator=shared.decHandeler.Get(int(item.movable.getName()[4:]))
				return Decorator