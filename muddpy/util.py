#from twisted.protocols.basic import LineReceiver
import world as w
from dumper import dump
from random import randrange

# Sends message with line feed, passed a sessionID
def sTu(sessionID, message, p = False):
	w.onlineSessions[sessionID].transport.write(message + "\n")
	if p:
		charID = w.onlineSessions[sessionID].charId
		actor = w.onlineActors[charID]
		displayString = actor.prompt()
		w.onlineSessions[sessionID].transport.write(displayString)
	
# Sends message without line feed, passed a sessionID
def sTuL(sessionID, message):
	w.onlineSessions[sessionID].transport.write(message)

# Returns player session from actor ID
def getSFChar(id):
	player = w.onlineSessions[id]
	return player
	
# Send a message to the room, passed a room object, message, and ActorIDs of exceptions
def sTr(where,message,exceptions):
	actorList = where.actors
	for id in actorList:
		if id in exceptions:
			pass
		else:
			sTu(w.onlineActors[id].sId,message)

# Send a Actor prompt
# Default to hp/hp mp/mp mv/mv
def sTup(sessionID):
	charID = w.onlineSessions[sessionID].charId
	actor = w.onlineActors[charID]
	displayString = actor.prompt()
	w.onlineSessions[sessionID].transport.write(displayString)

# Check to see if Actor is aware (not asleep or unconscious)
def checkAware(id):
	actor = w.onlineActors[id]
	if (actor.position == 3 or actor.position == 4):
		return 0
	else:
		return 1

def doRegen():
	# Loop through onlineActors
	for ID in w.onlineActors:
		pc = w.onlineActors[ID]
		if (pc.hp.getCur() < pc.hp.getMax()):
			randHp = randrange(1,100)
			if randHp > 70:
				print "Trigger +HP"
				pc.hp.setCur(pc.hp.getCur() + 1)
		
		if (pc.mp.getCur() < pc.mp.getMax()):
			randMp = randrange(1,100)
			if randMp > 80:
				print "Trigger +MP"
				pc.mp.setCur(pc.mp.getCur() + 1)
		
		if (pc.mv.getCur() < pc.mv.getMax()):
			randMv = randrange(1,100)
			if randMv > 70:
				print "Trigger +MV"
				diff = pc.mv.getMax() - pc.mv.getCur()
				if diff > 5:
					diff = 5
				pc.mv.setCur(pc.mv.getCur() + diff)

def load_new_item(itemNum,ch):
	itemKey = w.misc.highobj + 1
	w.misc.highobj = itemKey + 1
	w.onlineObjects[itemKey] = w.Item(itemNum)
	here = w.locations[ch.loc]
	here.addObject(itemKey)

def isVowel(checkString):
	vowels = ["a","e","i","o","u"]
	if checkString.lower() in vowels:
		return 1
	else:
		return 0

def returnArgInfo(text):
	info = {}
	info["args"] = text.split()
	info["num"] = len(info["args"])
	return info
