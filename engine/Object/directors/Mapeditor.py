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

	def evt_selected(self, selections, shiftkeydown):
		shared.DPrint(0, "MapDir", "Selections Updated")
		self.selections=selections
		for x in self.CurrentSelection:
			x._deselected()

		self.CurrentSelection=[]

		for x in self.selections:
			decoID=split(x.getName(),"Node_")
			decoID=decoID[0]+decoID[1]
			print(x.getName())
			Deco=shared.decHandeler.GetAll(decoID)
			Deco._selected()
			self.CurrentSelection.append(Deco)

	def evt_moveclick(self, pos, shiftkeydown):
		print("RCLICK")
		shared.mapBackend.SelectionRightClick()

	def evt_actionclick(self, data, shiftkeydown):
		print("RCLICK - ACTION!")
		shared.mapBackend.SelectionRightClick()

	def Frame(self):
		pass