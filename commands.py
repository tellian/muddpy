# Parser
from util import sTu, getSFChar, sTr, sTup, checkAware
import world as w
import settings as s

from dumper import dump

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
class Command:
	
	def __init__(self,character,command):
		# need to make just first word of command be the actual command
		if len(command.split(None, 1)) > 1:
			firstword, rest = command.split(None, 1)
			self.command = firstword.lower()
			self.rawArgs = rest.strip()
		else:
			self.rawArgs = ""
			self.command = command.lower() # First word
		self.cmdStr = command # Whole thing
		self.ch = character
		self.function_list = { 	'look': self.c_look, 'score': self.c_score, 'move': self.c_move,
														'sit': self.c_sit, 'stand': self.c_stand, 'sleep': self.c_sleep,
														'wake': self.c_wake,
		}	
		
	def parse(self):
		# Look up command in alias list. If exists, rewrite to actual command.
		if self.cmdStr == "":
			sTup(self.ch.sId)
			return
		self.rawArgs = self.rawArgs.strip()
		if self.command in alias_list:
			tmpcmd = alias_list[self.command]
			sizearray = tmpcmd.split(" ")
			if len(sizearray) == 2:
				self.rawArgs = str(sizearray[1]) + " " + str(self.rawArgs)
				self.command = sizearray[0]
			else:
				self.command = alias_list[self.command]
		if self.command in command_list:
			self.rawArgs = self.rawArgs.strip()
			func = self.function_list[self.command]
			func()
		else:
			sTu(self.ch.sId,"Command not found",1)
			
	def c_look(self):
		if not checkAware(self.ch.Id):
			sTu(self.ch.sId,"You are not aware enough to do anything.",1)
			return
		# Do Look stuff
		loc = self.ch.loc
		# Build look string. Start with room name,
		displayString = w.locations[loc].name + " ["
		# Add exits
		for exits in w.locations[loc].exits:
			displayString += exits
		# Add description
		displayString += "]\n" + w.locations[loc].desc + "\n"
		# Add other Actors
		for actors in w.locations[loc].actors:
			if actors <> self.ch.Id:
				if w.onlineActors[actors].position == 1:
					displayString += w.onlineActors[actors].name + " is standing here.\n"
				elif w.onlineActors[actors].position == 2:
					displayString += w.onlineActors[actors].name + " is sitting here.\n"
		sTu(self.ch.sId,displayString,1)

	def c_score(self):
		# Do score stuff
		attribs = self.ch.attr
		displayString = self.ch.name + "\nDesc: " + self.ch.desc + "\n"
		displayString += "Attributes: \n"
		displayString += "Str: {0}\n".format(attribs.get("str"))
		displayString += "Con: {0}\n".format(attribs.get("con"))
		displayString += "Dex: {0}\n".format(attribs.get("dex"))
		displayString += "Wis: {0}\n".format(attribs.get("wis"))
		displayString += "Int: {0}\n".format(attribs.get("int"))
		displayString += "Cha: {0}\n".format(attribs.get("cha"))
		sTu(self.ch.sId,displayString,1)
		
	def c_move(self): # Moving
		if not checkAware(self.ch.Id):
			sTu(self.ch.sId,"You are not aware enough to do anything.",1)
			return
		here = w.locations[self.ch.loc]
#		print "here.mv:" + str(here.mv) + " mv:" + str(self.ch.mv.getCur())
		if here.mv > self.ch.mv.getCur():
			sTu(self.ch.sId,"You are too tired to move.",1)
			return
		# Use only the first argument. As this command is only reached via alias,
		# don't have to worry about checking for arguments
		argsSplit = self.rawArgs.split(" ")
		if len(argsSplit) > 1:
			direction = argsSplit[0]
		else:
			direction = self.rawArgs
		# Check to see if that direction can even be moved in
		if direction in here.exits:
			sTr(here,self.ch.name + " has left the room.",self.ch.Id)
			sTu(self.ch.sId,"You move to the " + direction + ".")
			self.ch.mv.setCur(self.ch.mv.getCur() - here.mv)
			here.leaveRoom(self.ch.Id)
			there = w.locations[here.exits[direction].dest]
			there.addRoom(self.ch.Id)
			self.ch.loc = here.exits[direction].dest
			sTr(there,self.ch.name + " has arrived from the " + direction + ".",self.ch.Id)
			comm = Command(self.ch,"look")
			comm.parse()
		else:
			sTu(self.ch.sId,"You cannot go that way.",1)

	def c_sit(self): # Sitting
		if not checkAware(self.ch.Id):
			sTu(self.ch.sId,"You are not aware enough to do anything.",1)
			return
		if self.ch.position == 2:
			sTu(self.ch.sId,"You are already sitting!",1)
		elif self.ch.position == 1:
			self.ch.position = 2
			sTu(self.ch.sId,"You sit down.",1)
			sTr(w.locations[self.ch.loc],self.ch.name + " sits down.",self.ch.Id)
		
	def c_stand(self): # Standing
		if not checkAware(self.ch.Id):
			sTu(self.ch.sId,"You are not aware enough to do anything.",1)
			return
		if self.ch.position == 1:
			sTu(self.ch.sId,"You are already standing!",1)
		elif self.ch.position == 2:
			self.ch.position = 1
			sTu(self.ch.sId,"You stand up.",1)
			sTr(w.locations[self.ch.loc],self.ch.name + " stands up.",self.ch.Id)
		
	def c_sleep(self): # Going to sleep
		if self.ch.position == 3:
			sTu(self.ch.sId,"You are already asleep.",1)
		elif self.ch.position == 4:
			sTu(self.ch.sId,"You are unconscious already and can't sleep.",1)
		elif (self.ch.position == 1 or self.ch.position == 2):
			sTu(self.ch.sId,"You lie down and go to sleep.",1)
			self.ch.position = 3
			sTr(w.locations[self.ch.loc],self.ch.name + " lies down and goes to sleep.",self.ch.Id)

	def c_wake(self): # Waking up
		if (self.ch.position == 1 or self.ch.position == 2):
			sTu(self.ch.sId,"You are already awake.",1)
		elif (self.ch.position == 3):
			sTu(self.ch.sId,"You wake and sit up.",1)
			self.ch.position = 2
			sTr(w.locations[self.ch.loc],self.ch.name + " wakes and sits up.",self.ch.Id)
		elif (self.ch.position == 4):
			sTu(self.ch.sId,"You can't wake up.",1)
			
	
