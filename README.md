# muddpy
Simple mud in python

Run _new.py_ to start mud

_utility.py_ contains miscellaneous functions
* sTu(sessionID,message,[1]) (optional if you want a prompt sent)
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

All locations and actors are currently loaded from json files in data/

_world.onlineSessions_ holds player sessions and is where communication via twisted takes place.
_world.py_ is where it is created as an empty dict(), but it is modified elsewhere (mostly _new.py_)
Its parts:
* name = player Name, also is the key by which it is found in the dict.
* state = for now, controls which twisted handler parses session input
* charId = character ID that this session is affiliated with
* id = duplicate of Name (probably use this in the end, as it is shorter to type) 
* transport = actual twisted session

_world.onlineCharacters_ holds character info of PCs that are currently online.
_world.py_ is where it is created as an empty dict(), but it is modified elsewhere.
Contains entries of Class PC, which extends class Actor.

Class _PC_ will contain the following:
* attr = Attributes class (str, dex, con, wis, int, cha)
* hp = Stats class (max, tmp, cur)
* mv = Stats class (max, tmp, cur)
* mp = Stats class (max, tmp, cur)
* Id = id
* loc
* desc (soon to be ldesc and sdesc)
* sId
* name
* position
