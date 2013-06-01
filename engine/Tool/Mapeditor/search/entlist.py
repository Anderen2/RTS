#Entity List SearchEngine

from engine import shared, debug

class SearchEntlist():
	def __init__(self):
		pass

	def search(self, term):
		index=shared.EntityHandeler.EntDict
		hits=[]
		names=[]
		for key, value in index.iteritems():
			if str(term) in str(key):
				hits.append(key)
				names.append(value["name"])

			elif str(term) in str(value["name"]):
				hits.append(key)
				names.append(value["name"])

		if len(hits)==1:
			Confirmed=hits[0]
		else:
			Confirmed=None

		return (self.Prettify(hits, names), Confirmed)

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