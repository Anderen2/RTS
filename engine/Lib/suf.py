#Small useful functions

from twisted.internet import reactor

WhatToCall = []
ArgumentsToCall = []

def WaitOneTick(call, *kwargs):
	global WhatToCall
	global ArgumentsToCall
	WhatToCall.append(call)
	ArgumentsToCall.append(kwargs)
	reactor.callLater(0, _waitedOneTick)

def _waitedOneTick():
	global WhatToCall
	global ArgumentsToCall
	foo = WhatToCall.pop(0)
	bar = ArgumentsToCall.pop(0)

	foo(*bar)