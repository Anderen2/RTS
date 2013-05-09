#Mapfile creator (CLI)
import pickle

mapfilev=1.0
print("YARTS Mapfile Creator for v."+str(mapfilev))


#Mapproperties
mproperties={}
mproperties["name"]=raw_input("Name of map ")
mproperties["version"]=raw_input("Version of map ")
mproperties["mapfilev"]=mapfilev
mproperties["desc"]=raw_input("Description of map ")

#Terrain properies
tproperties={}
print("Do you have a terrain.cfg you want to rip? If so, type the path here, else leave it blank ")
terraincfg=raw_input()
if terraincfg!="":
	print("fapper ")
	exit()
else:
	print("No terraincfg defined, please enter the settings manually ")
	tproperties["tworldtexture"]=raw_input("Name of world texture ")
	tproperties["tdetailtexture"]=raw_input("Name of detail texture ")
	tproperties["tdetailtile="]=raw_input("number of times the detail texture will tile in a terrain tile ")
	tproperties["tpagesource"]=raw_input("Heightmap source ")
	tproperties["thighimage"]=raw_input("Name of Heightmap file ")
	tproperties["tpagesize"]=raw_input("How large is a page of tiles (in vertices)? Must be (2^n)+1 ")
	tproperties["ttilesize"]=raw_input("How large is each tile? Must be (2^n)+1 and be smaller than PageSize ")
	tproperties["tpageworldx"]=raw_input("The size of a terrain page, in world units (X) ")
	tproperties["tpageworldy"]=raw_input("The size of a terrain page, in world units (Y) ")
	tproperties["tmaxheight"]=raw_input("Maximum height of the terrain ")

	if "y" in raw_input("Change advanced settings for terrain? (if so, type yes) "):
		tproperties["trawsize"]=raw_input("RAW-specific setting - size (horizontal/vertical) ")
		tproperties["tbpp"]=raw_input("RAW-specific setting - bytes per pixel (1 = 8bit, 2=16bit) ")
		tproperties["tmaxpixelerror"]=raw_input("The maximum error allowed when determining which LOD to use ")
		tproperties["tvertexprogrammorph"]=raw_input("Use vertex program to morph LODs, if available? (yes/no) ")
	else:
		tproperties["trawsize"]=""
		tproperties["tbpp"]=""
		tproperties["tmaxpixelerror"]=3
		tproperties["tvertexprogrammorph"]="yes"

#Player properties
pproperties={}
print("\n")
print("Starting Player propertysetting")
pproperties["amount"]=int(raw_input("How many players will the map support? "))
for x in range(0, pproperties["amount"]):
	print("Player "+str(x)+" properties:  ")
	pproperties["player"+str(x)]={}
	pproperties["player"+str(x)]["cmdxyz"]=raw_input("XYZ coordinates of commandcenter (x,y,z):  ")
	pproperties["player"+str(x)]["cmdrotxyz"]=raw_input("XYZ rotation of commandcenter (rotx,roty,rotz):  ")
	pproperties["player"+str(x)]["cameraxyz"]=raw_input("Inital camera xyz coords (x,y,z):  ")
	pproperties["player"+str(x)]["camerarotxyz"]=raw_input("Inital camera xyz rotation (rotx,roty,rotz:  ")

#Decoration properties
dproperties={}
print("\n")
print("Starting Decoration placement, type end at any time to stop/move on ")
end=False
deco=0
while not end:
	foo=raw_input("Entity ("+str(deco)+") enginename:  ")
	if foo!="end":
		bar=raw_input("Decoration placement (x,y,z):  ")
		if bar!="end":
			foobar=raw_input("Decoration rotation (rotx,roty,rotz):  ")
			if foobar!="end":
				dproperties["deco"+str(deco)]={}
				dproperties["deco"+str(deco)]["name"]=foo
				dproperties["deco"+str(deco)]["xyz"]=bar
				dproperties["deco"+str(deco)]["rot"]=foobar
				deco+=1
			else:
				end=True
		else:
				end=True
	else:
				end=True

#Zones properties
zproperties={}
print("\n")
print("Starting Zone placement, type end at any time to stop/move on ")
end=False
zone=0
while not end:
	foo=raw_input("Zone ("+str(zone)+") name:  ")
	if foo!="end":
		bar=raw_input("Zone placement (x,y,z):  ")
		if bar!="end":
			foobar=raw_input("Zone rotation (rotx,roty,rotz):  ")
			if foobar!="end":
				zproperties["zone"+str(zone)]={}
				zproperties["zone"+str(zone)]["name"]=foo
				zproperties["zone"+str(zone)]["xyz"]=bar
				zproperties["zone"+str(zone)]["rot"]=foobar
				zone+=1
			else:
				end=True
		else:
				end=True
	else:
				end=True

#Unit properties
uproperties={}
print("\n")
print("Starting Unit placement, type end at any time to stop/move on ")
end=False
unit=0
while not end:
	foo=raw_input("Unit ("+str(unit)+") unitname:  ")
	if foo!="end":
		bar=raw_input("Unit placement (x,y,z):  ")
		if bar!="end":
			barfoo=raw_input("Unit team (0 for none): ")
			foobar=raw_input("Unit rotation (rotx,roty,rotz):  ")
			if foobar!="end":
				uproperties["unit"+str(unit)]={}
				uproperties["unit"+str(unit)]["name"]=foo
				uproperties["unit"+str(unit)]["xyz"]=bar
				uproperties["unit"+str(unit)]["rot"]=foobar
				uproperties["unit"+str(unit)]["team"]=barfoo
				unit+=1
			else:
				end=True
		else:
				end=True
	else:
				end=True

properties={}
properties["map"]=mproperties
properties["terrain"]=tproperties
properties["players"]=pproperties
properties["decos"]=dproperties
properties["zones"]=zproperties
properties["units"]=uproperties

print("Phew, that was a lot of data!")
raw_input("Press Enter")
print(properties)
raw_input("pickle [ENTER]")
#print(pickle.dumps(properties))
print("Where should I lay my dump? (Where is the toilet)?")
path=raw_input()
filee=open(path, "w")
pickle.dump(properties, filee)