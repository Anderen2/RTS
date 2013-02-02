#Networking - Commands
#This declares commands to use towards the networking module

from engine import debug, shared
from string import split

Type=None

# Type 0: Shared
# Type 1: Server
# Type 2: Client

def Init(arg):
	global Type
	Type==arg

#COMMAND OPTIONS:
CDict={}

def ParseCommand(*Txt):
	if type(ParseCommand)!=str:
		foo=""
		for x in Txt:
			foo=foo+x+" "
		Txt=foo

	CmdPar=split(Txt," ")
	CMD=CmdPar[0].lower()
	PAR=CmdPar[1:]
	try:
		if CDict.has_key(CMD):
			return CDict[CMD]["exec"](*PAR)
		else:
			return "Invalid Command!"
		return "Wth"
	except:
		return traceback.format_exc()

#Add Networked Command
def ANC(Typ, cmd, func, info="", args=-1):
	CDict[cmd]={}
	if Typ==Type or Typ==0:
		CDict[cmd]["exec"]=func
	else:
		Shared.DPrint("sv_netcmd", 0, "Networked command rejected because of wrong type!")

#Run Networked Command
def RNC(cmd):
	return ParseCommand(cmd)

def TestCommand(hey1):
	print "hay"+str(hey1)

ANC(0, "test", TestCommand)

debug.ACC("net_rnc", ParseCommand, info="Simulate networked command")