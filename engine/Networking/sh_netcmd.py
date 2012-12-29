#NetworkCommands Shared - What to do and when!

#COMMAND OPTIONS:
CDict={}

def ParseCommand(Txt):
	CmdPar=split(Txt," ")
	CMD=CmdPar[0].lower()
	PAR=CmdPar[1:]
	try:
		if CDict.has_key(CMD):
			return CDict[CMD]["exec"](*PAR)
		return ""
	except:
		return traceback.format_exc()

#Add Networked Command
def ANC(cmd, func, info="", args=-1):
	CDict[cmd]={}
	CDict[cmd]["exec"]=func

#Run Networked Command
def RNC(cmd):
	return ParseCommand(cmd)

def TestCommand(hey1):
	print "hay"+str(hey1)

ANC("test", TestCommand)