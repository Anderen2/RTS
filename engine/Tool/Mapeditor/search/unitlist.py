#Entity List SearchEngine

from engine import shared, debug
from importlib import import_module
from os import listdir

class SearchUnitlist():
	def __init__(self):

		self.unitscripts={}
		#Find and import all availible UnitScripts HERE
		modpath = "engine.Object.unitscripts."
		filepath = "engine/Object/unitscripts/"

		for stuff in listdir(filepath):
			if not "." in stuff:
				self.unitscripts[stuff] = import_module(modpath+stuff+".cl_"+stuff).Unit

	def search(self, term):
		
		hits=[]
		hits2=[]
		names=[]
		for key, unit in self.unitscripts.iteritems():
			if str(term).lower() in str(key).lower():
				hits.append(unit)
				hits2.append(key)
				names.append(unit.Name)

			elif str(term).lower() in str(unit.Name).lower():
				hits.append(unit)
				hits2.append(key)
				names.append(unit.Name)

		if len(hits)==1:
			Confirmed=(hits[0].UnitID, hits[0].BuildEntity)
		else:
			Confirmed=None

		return (self.Prettify(hits2, names), Confirmed)

	def Prettify(self, result, names):
		pretty="did you mean: \n"

		if len(result)==0:
			return "No entitynames are matching the search term"

		i=0
		for x in result:
			pretty=pretty+str(x)+"\n"
			pretty=pretty+str(names[i])+"\n\n"
			i+=1
		return pretty