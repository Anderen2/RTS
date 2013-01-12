import traceback
from string import split
import shared

#DEBUG OPTIONS:
AABB=True
GUISTATS=True

#COMMAND OPTIONS:
CDict={}

def ParseCommand(Txt):
	global AABB, GUISTATS
	CmdPar=split(Txt," ")
	CMD=CmdPar[0].lower()
	PAR=CmdPar[1:]
	try:
		#GLOBAL COMMANDS:
		if CMD=="helloworld":
			return "Hey"+str(PAR)
		elif CMD=="exit":
			exit()

		#CONSOLE COMMANDS
		elif CMD=="showconsole":
			shared.console.show()
		elif CMD=="hideconsole":
			shared.console.hide()

		#DEBUG COMMANDS
		elif CMD=="dbg_aabb":
			AABB = not AABB
			return str(AABB)
		elif CMD=="dbg_guistats":
			GUISTATS = not GUISTATS
			shared.renderguiGUI.GuiStats(GUISTATS)
			return str(GUISTATS)

		#GUI COMMANDS
		elif CMD=="gui_hideall":
			shared.renderguiGUI.HideAll()
		elif CMD=="gui_showall":
			shared.renderguiGUI.ShowAll()

		#UNIT HANDLER COMMANDS
		elif CMD=="u_create":
			shared.unitHandeler.CreateMov(3,1,1,"robot")
			#Type, Faction, Team, SubType
		elif CMD=="u_cs":
			shared.unitHandeler.CreateMov(int(PAR[0]),int(PAR[1]),int(PAR[2]),PAR[3])
		elif CMD=="u_cmul":
			for x in range(0,int(PAR[0])):
				shared.unitHandeler.CreateMov(3,1,1,"robot")
		elif CMD=="u_csmul":
			for x in range(0,int(PAR[0])):
				shared.unitHandeler.CreateMov(int(PAR[1]),int(PAR[2]),int(PAR[3]),PAR[4])
		elif CMD=="u_count":
			return str(shared.unitHandeler.Count())
		elif CMD=="u_pop":
			shared.unitHandeler.Destroy(len(shared.unitHandeler.units)-1)
		elif CMD=="u_destroy":
			shared.unitHandeler.Destroy(int(PAR[0]))
		elif CMD=="u_kill":
			shared.unitHandeler.Get(int(PAR[0]))._dead()
		elif CMD=="u_damage":
			shared.unitHandeler.Get(int(PAR[0]))._damage(int(PAR[1]))
		elif CMD=="u_amount" or CMD=="u_total":
			ARG=split(PAR[0],"-")
			return str(shared.unitHandeler.Amount(SubType=ARG[0],Team=ARG[1], Faction=ARG[2], Type=ARG[3]))

		#UNIT COMMANDS
		elif CMD=="u_move":
			shared.unitHandeler.Get(int(PAR[0])).entity.Move()
		elif CMD=="u_setpos":
			return str(shared.unitHandeler.Get(int(PAR[0])).entity.SetPosition(int(PAR[1]), int(PAR[2]), int(PAR[3])))
		elif CMD=="u_translate":
			return str(shared.unitHandeler.Get(int(PAR[0])).entity.Translate(int(PAR[1]), int(PAR[2]), int(PAR[3])))

		elif CMD=="u_rotate":
			return str(shared.unitHandeler.Get(int(PAR[0])).entity.Rotate(float(PAR[1]), float(PAR[2]), float(PAR[3])))

		#DECORATOR COMMANDS
		elif CMD=="d_create":
			shared.decHandeler.Create(1,"barrel")
			#Type, Faction, Team, SubType
		elif CMD=="d_cs":
			shared.decHandeler.Create(PAR[0])
		elif CMD=="d_cmul":
			for x in range(0,int(PAR[0])):
				shared.decHandeler.Create(1,"barrel")
		elif CMD=="d_csmul":
			for x in range(0,int(PAR[0])):
				shared.decHandeler.Create(int(PAR[0]),int(PAR[1]),int(PAR[2]),PAR[3])
		elif CMD=="d_count":
			return str(shared.decHandeler.Count())
		elif CMD=="d_pop":
			shared.decHandeler.Destroy(len(shared.decHandeler.units)-1)
		elif CMD=="d_destroy":
			shared.decHandeler.Destroy(int(PAR[0]))
		elif CMD=="d_kill":
			shared.decHandeler.Get(int(PAR[0]))._dead()
		elif CMD=="d_damage":
			shared.decHandeler.Get(int(PAR[0]))._damage(int(PAR[1]))
		elif CMD=="d_amount" or CMD=="u_total":
			ARG=split(PAR[0],"-")
			return str(shared.decHandeler.Amount(SubType=ARG[0], Type=ARG[3]))

		#RENDER COMMANDS
		elif CMD=="water":
			Water=shared.WaterManager.Create((float(PAR[0]),float(PAR[1]),float(PAR[2])),float(PAR[3]),float(PAR[4]))
		elif CMD=="fow":
			import Render.render3dfow
			shared.FOW=Render.render3dfow.FieldOfWar()
		elif CMD=="fow_vision":
			shared.FOW.VisionPos((int(PAR[0]),int(PAR[1])))
		elif CMD=="fow_visionid":
			shared.FOW.VisionIdx(int(PAR[0]))
		elif CMD=="fow_update":
			shared.FOW.Update()
		elif CMD=="fow_get":
			return str(shared.FOW.GetVert(int(PAR[0])))
		elif CMD=="fow_getall":
			return str(shared.FOW.GetVerts())
		elif CMD=="fow_circle":
			shared.FOW.VisionCircle((int(PAR[0]),int(PAR[1])),int(PAR[2]))
		elif CMD=="fcu":
			import Render.render3dfow
			shared.FOW=Render.render3dfow.FieldOfWar()
			shared.FOW.VisionCircle((300,300),2)
			shared.FOW.Update()
		elif CMD=="fow_sq":
			shared.FOW.VisionSquare((int(PAR[0]),int(PAR[1])),(int(PAR[2]),int(PAR[3])))

		else:
			#Check for additional commands:
			if CDict.has_key(CMD):
				if CDict[CMD]["args"]==-1 or CDict[CMD]["args"]==len(PAR):
					return CDict[CMD]["exec"](*PAR)
				else:
					return "Invalid amount of arguments! \n"+CDict[CMD]["info"]
			else:
				return "Invalid Command!"
		return ""

	except:
		return traceback.format_exc()

def ACC(cmd, func, info="", args=-1):
	CDict[cmd]={}
	CDict[cmd]["info"]=info
	CDict[cmd]["args"]=args
	CDict[cmd]["exec"]=func

def RCC(cmd):
	return ParseCommand(cmd)

def TestCommand(hey1=[]):
	print "hay"+str(hey1)

def listCMD():
	Foo=""
	for CMD in sorted(CDict):
		Foo=Foo+CMD+": "+CDict[CMD]["info"]+"\n \n"
	print Foo

ACC("help", listCMD, info="Lists all commands in the console")

ACC("testcmd", TestCommand, info="A Testing Command")

ACC("testcmd2", TestCommand, info="A Testing Command with req!", args=1)