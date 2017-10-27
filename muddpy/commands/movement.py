# Movement related commands

from util import sTu, getSFChar, sTr, sTup, checkAware
import world as w
import settings as s
import inform

def c_wake(ch,rawArgs): # Waking up
	if (ch.position == 1 or ch.position == 2):
		sTu(ch.sId,"You are already awake.",1)
	elif (ch.position == 3):
		sTu(ch.sId,"You wake and sit up.",1)
		ch.position = 2
		sTr(w.locations[ch.loc],ch.name + " wakes and sits up.",ch.Id)
	elif (ch.position == 4):
		sTu(ch.sId,"You can't wake up.",1)

def c_move(ch,rawArgs): # Moving
		if not checkAware(ch.Id):
			sTu(ch.sId,"You are not aware enough to do anything.",1)
			return
		here = w.locations[ch.loc]
		if here.mv > ch.mv.getCur():
			sTu(ch.sId,"You are too tired to move.",1)
			return
		# Use only the first argument. As this command is only reached via alias,
		# don't have to worry about checking for arguments
		argsSplit = rawArgs.split(" ")
		if len(argsSplit) > 1:
			direction = argsSplit[0]
		else:
			direction = rawArgs
		# Check to see if that direction can even be moved in
		if direction in here.exits:
			sTr(here,ch.name + " has left the room.",ch.Id)
			sTu(ch.sId,"You move to the " + direction + ".")
			ch.mv.setCur(ch.mv.getCur() - here.mv)
			here.leaveRoom(ch.Id)
			there = w.locations[here.exits[direction].dest]
			there.addRoom(ch.Id)
			ch.loc = here.exits[direction].dest
			sTr(there,ch.name + " has arrived from the " + direction + ".",ch.Id)
			inform.c_look(ch,"")
		else:
			sTu(ch.sId,"You cannot go that way.",1)

def c_sit(ch,rawArgs): # Sitting
	if not checkAware(ch.Id):
		sTu(ch.sId,"You are not aware enough to do anything.",1)
		return
	if ch.position == 2:
		sTu(ch.sId,"You are already sitting!",1)
	elif ch.position == 1:
		ch.position = 2
		sTu(ch.sId,"You sit down.",1)
		sTr(w.locations[ch.loc],ch.name + " sits down.",ch.Id)

def c_stand(ch,rawArgs): # Standing
	if not checkAware(ch.Id):
		sTu(ch.sId,"You are not aware enough to do anything.",1)
		return
	if ch.position == 1:
		sTu(ch.sId,"You are already standing!",1)
	elif ch.position == 2:
		ch.position = 1
		sTu(ch.sId,"You stand up.",1)
		sTr(w.locations[ch.loc],ch.name + " stands up.",ch.Id)

def c_sleep(ch,rawArgs): # Going to sleep
	if ch.position == 3:
		sTu(ch.sId,"You are already asleep.",1)
	elif ch.position == 4:
		sTu(ch.sId,"You are unconscious already and can't sleep.",1)
	elif (ch.position == 1 or ch.position == 2):
		sTu(ch.sId,"You lie down and go to sleep.",1)
		ch.position = 3
		sTr(w.locations[ch.loc],ch.name + " lies down and goes to sleep.",ch.Id)
