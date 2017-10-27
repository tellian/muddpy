# informational

from util import sTu, getSFChar, sTr, sTup, checkAware
import world as w
import settings as s

def c_look(ch,rawArgs):
	if not checkAware(ch.Id):
		sTu(ch.sId,"You are not aware enough to do anything.",1)
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
	# Add other Actors
	for actors in w.locations[loc].actors:
		if actors <> ch.Id:
			if w.onlineActors[actors].position == 1:
				displayString += w.onlineActors[actors].name + " is standing here.\n"
			elif w.onlineActors[actors].position == 2:
				displayString += w.onlineActors[actors].name + " is sitting here.\n"
	sTu(ch.sId,displayString,1)

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
	sTu(ch.sId,displayString,1)
