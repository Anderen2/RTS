#Networking - Responses
#This declares what the engine should do at the different networked responses

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
			return "Invalid Response!"
		return "Wth"
	except:
		return traceback.format_exc()

#Add Networked Response
def ANR(Typ, cmd, func, info="", args=-1):
	CDict[cmd]={}
	if Typ==Type or Typ==0:
		CDict[cmd]["exec"]=func
	else:
		shared.DPrint("sv_netcmd", 0, "Networked response rejected because of wrong type!")

#Run Networked Response
def RNR(cmd):
	return ParseCommand(cmd)

def TestCommand(hey1):
	print "hay"+str(hey1)

ANR(0, "test", TestCommand)

debug.ACC("net_rnr", ParseCommand, info="Simulate networked response")