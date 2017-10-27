# Parser
from util import sTu, getSFChar, sTr, sTup, checkAware
import world as w
import settings as s
from commands import movement
from commands import inform

command_list = {
	'look':"1",
	'score':"1",
	'move':"1",
	'sit':"1",
	'stand':"1",
	'sleep':"1",
	'wake':"1",
	}
alias_list = {
	'l':'look',
	'sc':'score',
	'n':'move n',
	's':'move s',
	'e':'move e',
	'w':'move w',
	'sl':'sleep',
	'wa':'wake',
	}

function_list = {	'look': inform.c_look, 'score': inform.c_score, 'move': movement.c_move,
									'sit': movement.c_sit, 'stand': movement.c_stand, 'sleep': movement.c_sleep,
									'wake': movement.c_wake,
}

def cparse(ch, cmdStr): # Full Command String, character object
	if cmdStr == "":
		sTup(ch.sId)
		return
	# split up cmdStr into useful stuff.
	if len(cmdStr.split(None, 1)) > 1:
		firstword, rest = cmdStr.split(None, 1)
		command = firstword.lower()
		rawArgs = rest.strip()
	else:
		rawArgs = ""
		command = cmdStr.lower()
	commandRaw = cmdStr
	if command in alias_list:
		tmpcmd = alias_list[command]
		sizearray = tmpcmd.split(" ")
		if len(sizearray) == 2:
			rawArgs = str(sizearray[1]) + " " + str(rawArgs)
			command = sizearray[0]
		else:
			command = alias_list[command]
	if command in command_list:
		rawArgs = rawArgs.strip()
		func = function_list[command]
		func(ch,rawArgs)
	else:
		sTu(ch.sId,"Command not found",1)

