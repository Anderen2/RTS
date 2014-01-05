#Worldmodule - Movetypes
#Module for calculating different types of movement across the world

from engine import shared, debug

def Move(source, destination, speed, movetype):
	MOVETYPE_AB = -2
	MOVETYPE_NONE = -1
	MOVETYPE_AIR = 0
	MOVETYPE_GROUND = 1
	MOVETYPE_WATER = 2

	if len(destination) == 3:
		destination = (destination[0], destination[2])

	if movetype==MOVETYPE_NONE:
		return 0, source

	if movetype==MOVETYPE_AIR:
		return MoveAIR(source, destination, speed)

	if movetype==MOVETYPE_GROUND:
		return MoveGND(source, destination, speed)

def MoveAIR(source, destination, speed):
	src2d = (source[0], source[2])
	x, z, dist = shared.Pathfinder.ABPath.GetNextCoord(src2d, destination, speed)
	if shared.side == "Client" or shared.side=="Tool":
		y = shared.render3dTerrain.getHeightAtPos(x, z) + 100
	else:
		y = shared.Map.Terrain.getHeightAtPos(x, z) + 100
	return dist, (x, y, z)

def MoveGND(source, destination, speed):
	src2d = (source[0], source[2])
	x, z, dist = shared.Pathfinder.ABPath.GetNextCoord(src2d, destination, speed)
	if shared.side == "Client" or shared.side=="Tool":
		y = shared.render3dTerrain.getHeightAtPos(x, z)+1
	else:
		y = shared.Map.Terrain.getHeightAtPos(x, z)+1
	return dist, (x, y, z)

def Path(source, destination, movetype):
	MOVETYPE_AB = -2
	MOVETYPE_NONE = -1
	MOVETYPE_AIR = 0
	MOVETYPE_GROUND = 1
	MOVETYPE_WATER = 2

	start = (source[0], source[2])
	end = (destination[0], destination[2])

	if movetype == MOVETYPE_GROUND:
		return shared.Pathfinder.aStarPath.Search2(start, end, allowedtypes=[0])

	elif movetype == MOVETYPE_AIR or movetype == MOVETYPE_AB:
		return end

	elif movetype == MOVETYPE_WATER:
		return shared.Pathfinder.aStarPath.Search2(start, end, allowedtypes=[1])

	elif movetype == MOVETYPE_NONE:
		return None