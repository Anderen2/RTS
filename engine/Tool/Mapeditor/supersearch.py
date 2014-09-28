#SuperSearch
#SSearch is an modular 'almost semantic' searchengine. Just create an sEngine in ./search/
#Implement it in self.sEngines and sEngName, and use ask(EngName, Callback) when you need to search

from engine import shared, debug
import ogre.gui.CEGUI as CEGUI

from engine.Tool.Mapeditor.search import entlist, unitlist

class SSearchGUI():
	def __init__(self):
		self.root = shared.renderGUI.windowManager.getWindow("Root")
		self.layout = shared.renderGUI.windowManager.loadWindowLayout("SSearch.layout")

		self.layout.setProperty("Text", "Search..")
		self.root.addChildWindow(self.layout)
		self.layout.setPosition(CEGUI.UVector2(CEGUI.UDim(0.35, 0), CEGUI.UDim(0.1, 0)))
		shared.globalGUI.registerLayout(self.layout)
		self.layout.hide()

		self.resultGUI=shared.renderGUI.windowManager.createWindow("Vanilla/MultiLineEditbox", "SSResults")
		self.resultGUI.setSize(CEGUI.UVector2(CEGUI.UDim(0.25, 0), CEGUI.UDim(0.2, 0)))
		self.resultGUI.setPosition(CEGUI.UVector2(CEGUI.UDim(0.35, 0), CEGUI.UDim(0.16, 0)))
		self.resultGUI.setReadOnly(True)
		self.root.addChildWindow(self.resultGUI)
		shared.globalGUI.registerLayout(self.resultGUI)
		self.resultGUI.hide()

		self.Searchbox=shared.renderGUI.windowManager.getWindow("Search/Text")
		self.OkBtn=shared.renderGUI.windowManager.getWindow("Search/OK")
		self.XBtn=shared.renderGUI.windowManager.getWindow("Search/X")
		self.OkBtn.subscribeEvent(self.OkBtn.EventMouseButtonDown, self, "b_OK")
		self.XBtn.subscribeEvent(self.XBtn.EventMouseButtonDown, self, "b_X")
		self.Searchbox.subscribeEvent(self.Searchbox.EventTextAccepted, self, "s_Enter")

		self.CurrentEngine=None
		self.CurrentEngName="None"
		self.Customer=None
		self.sEngines=[entlist.SearchEntlist(), unitlist.SearchUnitlist()]
		self.sEngName=["decorators", "units"]

		debug.ACC("sse", self.show, info="Show the SuperSearch", args=0)
		debug.ACC("sse_hide", self.hide, info="Hide the SuperSearch", args=0)
		debug.ACC("sse_eng", self.setEngine, info="Set the engine to use", args=1)

	def ask(self, engine, customer):
		if self.setEngine(engine):
			self.Customer=customer
			self.show()

	def show(self):
		self.Searchbox.setProperty("Text", "")
		self.resultGUI.setProperty("Text", "Type and press enter to search! \nCurrent searchengine is: "+self.CurrentEngName)
		self.layout.show()
		self.resultGUI.show()
		shared.console.hide()
		shared.renderioInput.CurrentKeyInterface=1
		shared.renderioInput.takeKeyFocus("ssearch")
		self.Searchbox.activate()

	def hide(self):
		self.layout.hide()
		self.resultGUI.hide()
		shared.renderioInput.looseKeyFocus("ssearch")

	def s_Enter(self, evt):
		self.b_OK(None)

	def b_OK(self, evt):
		result = self.performSearch(self.Searchbox.getProperty("Text"))

		print(result)

		if result!=None and self.Customer!=None:
			self.Customer(result)
			self.hide()

	def b_X(self, evt):
		self.hide()

	def setEngine(self, engine):
		if engine in self.sEngName:
			self.CurrentEngine=self.sEngines[self.sEngName.index(engine)]
			self.CurrentEngName=engine
			return True
		else:
			return False

	def showResults(self, result):
		self.resultGUI.setProperty("Text", result)

	def performSearch(self, term):
		resInfo, result = self.CurrentEngine.search(term)
		self.showResults(str(resInfo))
		if result!=None:
			return result