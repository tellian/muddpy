import json
import yaml

class Attributes:
	def __init__(self):
		self.strength = 10
		self.constitution = 10
		self.dexterity = 10
		self.wisdom = 10
		self.intelligence = 10
		self.charisma = 10
	
	def set(self,type,value):
		if type == "str":
			self.strength = value
		elif type == "con":
			self.constitution = value
		elif type == "dex":
			self.dexterity = value
		elif type == "wis":
			self.wisdom = value
		elif type == "int":
			self.intelligence = value
		elif type == "cha":
			self.charisma = value
		else:
			print "Unknown attribute passed to Attribute.set!"
	
	def get(self,type):
		if type == "str":
			return self.strength
		elif type == "con":
			return self.constitution
		elif type == "dex":
			return self.dexterity
		elif type == "wis":
			return self.wisdom
		elif type == "int":
			return self.intelligence
		elif type == "cha":
			return self.charisma
		else:
			print "Unknown attribute passed to Attribute.set!"
	
class Actor:
	def __init__(self):
		self.attr = Attributes()
		self.max_hp = 100
		self.tmp_hp = 100
		self.cur_hp = 100
		self.max_mp = 100
		self.tmp_mp = 100
		self.cur_mp = 100
		self.max_mv = 100
		self.tmp_mv = 100
		self.cur_mv = 100
		
class PC(Actor):
	def __init__(self,Id,sessionId):
		# Load from characters
		self.attr = Attributes()
		self.Id = Id
		self.desc = characters[Id]["desc"]
		self.loc = characters[Id]["loc"]
		self.sId = sessionId
		self.name = characters[Id]["name"]
		self.max_hp = 100
		self.tmp_hp = 100
		self.cur_hp = 100
		self.max_mp = 100
		self.tmp_mp = 100
		self.cur_mp = 100
		self.max_mv = 100
		self.tmp_mv = 100
		self.cur_mv = 100
		self.position = 1
		# Add character to a room
		locations[self.loc].addRoom(self.Id)

class Location:
	def __init__(self,id):
		self.name = rooms[id]["name"]
		self.desc = rooms[id]["desc"]
		self.exits = {}
		self.objects = {}
		self.actors = {}
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
	global onlinePlayers, onlineActors
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
	onlinePlayers = {}
	onlineActors = {}

