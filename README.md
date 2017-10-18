# muddpy
Simple mud in python

Run _new.py_ to start mud

_utility.py_ contains miscellaneous functions
* sTu(sessionID,message) 
* sTuL(sessionID,message)
* sTr(where,message,exceptions)
* sTup(sessionID)

_world.py_ inits stuff and currently contains lots of classes:
* Attributes
* Actor
* PC
* Location
* Exits

_commands.py_ parses commands and runs appropriate. All command functions started with c_
* Command.parse
* c_look
* c_score
* c_sit
* c_stand
* c_move

