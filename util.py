#from twisted.protocols.basic import LineReceiver
import world as w

# Sends message with line feed, passed a player sessionID
def sTu(sessionID, message): 
	w.onlinePlayers[sessionID].transport.write(message + "\n")

# Sends message without line feed, passed a player session
def sTuL(sessionID, message):
	w.onlinePlayers[sessionID].transport.write(message)

# Returns player session from actor ID
def getSFChar(id):
	player = w.onlinePlayers[id]
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
def sTup(id):
	actor = w.onlineActors[id]
	displayString = "{}/{} {}/{} {}/{}> ".format(actor.cur_hp,actor.max_hp,actor.cur_mp,actor.max_mp,actor.cur_mv,actor.max_mv)
	sTuL(actor.sId,displayString)
