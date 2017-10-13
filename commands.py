# Parser
from util import sTu, getSFChar, sTr, sTup
import world as w
from dumper import dump

command_list = {
	'look':"1",
	'score':"1",
	'move':"1",
	'sit':"1",
	'stand':"1"
	}
alias_list = {
	'l':'look',
	'sc':'score',
	'n':'move n',
	's':'move s',
	'e':'move e',
	'w':'move w',
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
		self.function_list = { 'look': self.c_look, 'score': self.c_score, 'move': self.c_move,
													'sit': self.c_sit, 'stand': self.c_stand,
		}
		
	def parse(self):
		# Look up command in alias list. If exists, rewrite to actual command.
		self.rawArgs = self.rawArgs.strip()
		if self.command in alias_list:
			tmpcmd = alias_list[self.command]
			sizearray = tmpcmd.split(" ")
			if len(sizearray) == 2:
				self.rawArgs = str(sizearray[1]) + " " + str(self.rawArgs)
				self.command = sizearray[0]
		if self.command in command_list:
			self.rawArgs = self.rawArgs.strip()
			func = self.function_list[self.command]
			func()
		else:
			sTu(self.ch.sId,"Command not found")
			sTup(self.ch.Id)

	def c_look(self):
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
		sTu(self.ch.sId,displayString)
		sTup(self.ch.Id)

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
		sTu(self.ch.sId,displayString)
		sTup(self.ch.Id)
		
	def c_move(self): # Moving
		# Use only the first argument. As this command is only reached via alias,
		# don't have to worry about checking for arguments
		argsSplit = self.rawArgs.split(" ")
		if len(argsSplit) > 1:
			direction = argsSplit[0]
		else:
			direction = self.rawArgs
		here = w.locations[self.ch.loc]
		# Check to see if that direction can even be moved in
		if direction in here.exits:
			sTr(here,self.ch.name + " has left the room.",self.ch.Id)
			sTu(self.ch.sId,"You move to the " + direction + ".")
			here.leaveRoom(self.ch.Id)
			there = w.locations[here.exits[direction].dest]
			there.addRoom(self.ch.Id)
			self.ch.loc = here.exits[direction].dest
			sTr(there,self.ch.name + " has arrived from the " + direction + ".",self.ch.Id)
			comm = Command(self.ch,"look")
			comm.parse()
		else:
			sTu(self.ch.sId,"You cannot go that way.")
			sTup(self.ch.Id)

	def c_sit(self): # Sitting
		if self.ch.position == 2:
			sTu(self.ch.sId,"You are already sitting!")
			sTup(self.ch)
		elif self.ch.position == 1:
			self.ch.position = 2
			sTu(self.ch.sId,"You sit down.")
			sTr(w.locations[self.ch.loc],self.ch.name + " sits down.",self.ch.Id)
			sTup(self.ch.Id)
	
	def c_stand(self): # Standing
		if self.ch.position == 1:
			sTu(self.ch.sId,"You are already standing!")
			sTup(self.ch)
		elif self.ch.position == 2:
			self.ch.position = 1
			sTu(self.ch.sId,"You stand up.")
			sTr(w.locations[self.ch.loc],self.ch.name + " stands up.",self.ch.Id)
			sTup(self.ch.Id)
