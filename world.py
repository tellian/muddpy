import json
import yaml
import settings as s

class Item
	def __init__(self):
		# weight, name, keywords, sdesc, ldesc
		# type, light
		# wearable flag, what slots
		# IF WEAP
		# wtype, damage, tohit
		# speed, num_dice, size_dice, mod
		# crit
		# IF ARMOR
		# 
		# IF CONTAINER
		# 
		# IF MONEY
		
class Attributes:
	def __init__(self):
		self.stre = Stats(20)
		self.cons = Stats(20)
		self.dext = Stats(20)
		self.wisd = Stats(20)
		self.inte = Stats(20)
		self.char = Stats(20)
	
class Stats:
	def __init__(self,val):
		self.max_ = val
		self.cur = val
		self.tmp = val
	def getMax(self):
		return self.max_
	def setMax(self,val):
		self.max_ = val
	def getCur(self):
		return self.cur
	def setCur(self,val):
		self.cur = val
	def getTmp(self):
		return self.tmp
	def setTmp(self,val):
		self.tmp = val
	
class Actor:
	def __init__(self):
		self.attr = Attributes()
		self.hp = Stats(100)
		self.mp = Stats(100)
		self.mv = Stats(100)
		
class PC(Actor):
	def __init__(self,Id,sessionId):
		# Load from characters
		self.attr = Attributes()
		self.Id = Id
		self.desc = characters[Id]["desc"]
		self.loc = characters[Id]["loc"]
		self.sId = sessionId
		self.name = characters[Id]["name"]
		self.hp = Stats(100)
		self.mp = Stats(100)
		self.mv = Stats(100)
		self.position = 1   # 1 = stand, 2 = sit, 3 = sleep, 4 = unconscious
		self.pformat = "%h/%H %m/%M %v/%V >"
		# Add character to a room
		locations[self.loc].addRoom(self.Id)
	
	def prompt(self):
		# iterate through and populate format string with appropriate numbers
		output = self.pformat[:]
		output = output.replace("%h",str(self.hp.getCur()))
		output = output.replace("%H",str(self.hp.getMax()))
		output = output.replace("%m",str(self.mp.getCur()))
		output = output.replace("%M",str(self.mp.getMax()))
		output = output.replace("%v",str(self.mv.getCur()))
		output = output.replace("%V",str(self.mv.getMax()))
		return output
		
class Location:
	def __init__(self,id):
		self.name = rooms[id]["name"]
		self.desc = rooms[id]["desc"]
		self.exits = {}
		self.objects = {}
		self.actors = {}
		self.mv = int(rooms[id]["mv"])
		for exitNames in rooms[id]["exits"]:
			self.exits[exitNames] = Exits(exitNames,rooms[id]["exits"][exitNames])
	
	def leaveRoom(self,id):
		self.actors.pop(id, None)
	
	def addRoom(self,id):
		self.actors[id] = 1
	
class Exits:
	def __init__(self,direction,destination):
		self.dir = direction
		self.dest = destination
		
def init():
	global users, rooms, characters, locations
	global onlineSessions, onlineActors
	USER_FILE = "data/users.json"
	ROOM_FILE = "data/rooms.json"
	CHAR_FILE = "data/characters.json"
	with open(USER_FILE) as user_file:
		users = yaml.safe_load(user_file)
	with open(ROOM_FILE) as room_file:
		rooms = yaml.safe_load(room_file)
	# Now populate locations dict with necessary stuff from rooms
	locations = {}
	for id in rooms:
		locations[id] = Location(id)
	with open(CHAR_FILE) as char_file:
		characters = yaml.safe_load(char_file)
	onlineSessions = {}
	onlineActors = {}

