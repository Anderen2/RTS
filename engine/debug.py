import traceback
from string import split
from twisted.internet.reactor import stop
import shared

#DEBUG OPTIONS:
AABB=True
GUISTATS=True
GHOST_SYNC=True

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
		elif CMD=="exit" or CMD=="stop":
			stop()

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
			shared.renderGUI.GuiStats(GUISTATS)
			return str(GUISTATS)

		#UNIT HANDLER COMMANDS
		elif CMD=="u_create":
			shared.unitHandeler.CreateMov(3,1,1,"robot")
			#Type, Faction, Team, SubType
		elif CMD=="u_cs":
			shared.unitHandeler.Create(int(PAR[0]),PAR[1])
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

def listCMD():
	Foo=""
	for CMD in sorted(CDict):
		Foo=Foo+CMD+": "+CDict[CMD]["info"]+"\n \n"
	print Foo

def findCMD(src):
	Foo=""
	for CMD in sorted(CDict):
		if src in CMD:
			Foo=Foo+CMD+": "+CDict[CMD]["info"]+"\n \n"
	return Foo

def whichCMD(cmd):
	return str(CDict[cmd]["exec"])

def manCMD(cmd):
	return str(CDict[cmd]["info"])

def runFile(filesrc):
	with open(filesrc, "r") as foofile:
		for command in foofile:
			command=command.replace("\n", "")
			if command[0]!="#" and command[0]!=" " and command[0]!="/":
				shared.DPrint("debug",0,"EXE: "+command)
				shared.DPrint("debug",1,ParseCommand(command))

def runCLI(args):
	foo=" ".join(args)
	for x in split(foo, "--"):
		if x!="" and x!=" ":
			shared.DPrint("debug",0,"CLI: "+x)
			shared.DPrint("debug",1,ParseCommand(x))

def echo(*kwargs):
	foovar=""
	for x in kwargs:
		foovar=foovar+" "+x
	return(foovar)

#EXTRA COMMANDS
ACC("man", manCMD, info="Prints the commands manual/infostring\nUsage: ex. man man", args=1)
ACC("help", listCMD, info="Lists all commands in the console", args=0)
ACC("find", findCMD, info="Searchs for a command with the letters in it \nUsage: find something, ex. find gui", args=1)
ACC("which", whichCMD, info="Returns the name of the function which the command executes\nUsage: ex. which which", args=1)
ACC("echo", echo, info="Prints the arguments")