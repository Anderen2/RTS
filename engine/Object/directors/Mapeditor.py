#Director - Mapeditor
#This "director" only feeds the Mapeditor selection data

from engine import shared, debug
from string import split

class Director():
	def __init__(self):
		pass

	def Init(self):
		pass

	def Action(self):
		self.Cast=[]
		self.CurrentSelection=[]

	def evt_selected(self, selections):
		shared.DPrint(0, "MapDir", "Selections Updated")
		self.selections=selections
		for x in self.CurrentSelection:
			x._deselected()

		self.CurrentSelection=[]

		for x in self.selections:
			decoID=int(split(x.getName(),"_")[1])
			Deco=shared.decHandeler.Get(decoID)
			Deco._selected()
			self.CurrentSelection.append(Deco)

	def evt_moveclick(self, pos):
		shared.mapBackend.SelectionRightClick()

	def evt_actionclick(self, data):
		shared.mapBackend.SelectionRightClick()

	def Frame(self):
		pass