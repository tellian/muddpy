# informational

from util import sTu, getSFChar, sTr, sTup, checkAware, isVowel, returnArgInfo
import world as w
import settings as s

def c_look(ch,rawArgs):
	if not checkAware(ch.Id):
		ch.stu("You are not aware enough to do anything.")
		return
	# Do Look stuff
	loc = ch.loc
	# Build look string. Start with room name,
	displayString = w.locations[loc].name + " ["
	# Add exits
	for exits in w.locations[loc].exits:
		displayString += exits
	# Add description
	displayString += "]\n" + w.locations[loc].desc + "\n"
	# Add items in room
	for items in w.locations[loc].objects:
		if not w.onlineObjects[items].rdesc:
			if isVowel(w.onlineObjects[items].sdesc[:1]):
				displayString += "An "
			else:
				displayString += "A "
			displayString += w.onlineObjects[items].sdesc + " is sitting on the ground here.\n"
		else:
			displayString += w.onlineObjects[items].rdesc + "\n"
	# Add other Actors
	for actors in w.locations[loc].actors:
		if actors <> ch.Id:
			if w.onlineActors[actors].position == 1:
				displayString += w.onlineActors[actors].name + " is standing here.\n"
			elif w.onlineActors[actors].position == 2:
				displayString += w.onlineActors[actors].name + " is sitting here.\n"
	ch.stu(displayString)

def c_score(ch,rawArgs):
	# Do score stuff
	attribs = ch.attr
	displayString = ch.name + "\nDesc: " + ch.desc + "\n"
	displayString += "Attributes: \n"
	displayString += "Str: {0}\n".format(attribs.stre.getCur())
	displayString += "Con: {0}\n".format(attribs.cons.getCur())
	displayString += "Dex: {0}\n".format(attribs.dext.getCur())
	displayString += "Wis: {0}\n".format(attribs.wisd.getCur())
	displayString += "Int: {0}\n".format(attribs.inte.getCur())
	displayString += "Cha: {0}\n".format(attribs.char.getCur())
	ch.stu(displayString)

def c_keys(ch,rawArgs):
	args = returnArgInfo(rawArgs)
	if args["num"] == 0:
		ch.stu("This would be a key command.",0)
		# First check for keys in actors in the room
		here = w.locations[ch.loc]
		for charId in here.actors:
			ch.stu(w.onlineActors[charId].getFirstKey() + " - " + w.onlineActors[charId].sdesc,0)
		# Then check for keys in objects in the room
		# Then check for keys on objects in the character's inventory
		ch.stu("")
	else:
		ch.stu("Don't need any extra args.")
	
