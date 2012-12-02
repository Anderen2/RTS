#Grid Test #1
worldsize=1500
precision=500
XGrid=[]
for x in range(0,(worldsize+precision)/precision):
	XGrid.append(x*precision)

YGrid=[]
for y in range(0,(worldsize+precision)/precision):
	YGrid.append(y*precision)

print XGrid
print "___________________________________________"
print YGrid
print "___________________________________________"
Vertcount=len(XGrid)*len(YGrid)
print("Vertice Count: "+str(Vertcount))
Tricount=Vertcount/4
print("Triangle Count: "+str(Tricount))

What=(worldsize/precision)+1
print("Common: "+str(What))

raw_input()


#Create a list of all vertices
VertList=[]
for x in XGrid:
	for y in YGrid:
		VertList.append((x,y))

#Create a list of all triangles (1)
TriList1=[]
for x in VertList:
	TriList1.append((VertList.index(x), VertList.index(x)+1, VertList.index(x)+What))

#Remove bad triangles (1)
for x in range(1, What+1):
	TriList1.pop((What-1)*x)

#Remove offchart triangles (1)
for x in range(1,What):
	TriList1.pop(len(TriList1)-1)

#Reverse the verticles (2)
#VertList=VertList[::-1]

#Create a list of all triangles (2)
TriList2=[]
for x in VertList:
	TriList2.append((VertList.index(x)+What, VertList.index(x)+What+1, VertList.index(x)+1))

#Remove bad triangles (2)
for x in range(1, What+1):
	print x
	print TriList2.pop((What-1)*x)

#Remove offchart triangles (2)
for x in range(1,What):
	print x
	TriList2.pop(len(TriList2)-1)

print(TriList2)
print("__________________________")
print("L Triangle count: "+str(len(TriList1)))
print("R Triangle count: "+str(len(TriList2)))
print("Total Triangle count: "+str(len(TriList1)+len(TriList2)))

TriList=[]
for x in range(0,Tricount):
	Foo=x/4


raw_input()

Outline=[]
CurrVert=self.ConvXZtoVertex(pos)
Outline.append(CurrVert)
for x in range(0,radius):
	CurrVert=CurrVert+1
	Outline.append(CurrVert)
	print(CurrVert)
	CurrVert=CurrVert-self.OppVal
	Outline.append(CurrVert)
	print(CurrVert)
CurrVert=CurrVert+1
Outline.append(CurrVert)
print(CurrVert)
for x in range(0,radius):
	CurrVert=CurrVert+self.OppVal
	#Outline.append(CurrVert)
	print(CurrVert)
	CurrVert=CurrVert+1
	#Outline.append(CurrVert)
	print(CurrVert)
CurrVert=CurrVert+self.OppVal
Outline.append(CurrVert)
print(CurrVert)
for x in range(0, radius):
	CurrVert=CurrVert-1
	Outline.append(CurrVert)
	print(CurrVert)
	CurrVert=CurrVert+self.OppVal
	Outline.append(CurrVert)
	print(CurrVert)
CurrVert=CurrVert-1
Outline.append(CurrVert)
print(CurrVert)
for x in range(0, radius):
	CurrVert=CurrVert-self.OppVal
	#Outline.append(CurrVert)
	print(CurrVert)
	CurrVert=CurrVert-1
	#Outline.append(CurrVert)
	print(CurrVert)
CurrVert=CurrVert-self.OppVal
Outline.append(CurrVert)
print(CurrVert)

raw_input()