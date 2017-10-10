from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
from pprint import pprint
from dumper import dump
import json
import yaml
import commands

class Player:
	'Player information'
	def __init__(self):
		self.uname = "Tellian"
		self.IP = "none"

class Stats:
	def __init__(self):
		self.strength = 14
		self.intelligence = 13
		self.character = 12

class CharData:
	def __init__(self, charId, sId):
		self.name = characters[charId]["name"]
		self.desc = characters[charId]["desc"]
#		self.stats = Stats()
		self.other = "Misc"
		self.sId = sId
		self.loc = characters[charId]["loc"]
#	def parse(self, cmdStr):
		# This will actually parse out commands.
		#sM(self.sessionId,cmdStr + " - is what was given")
		#if cmdStr=="l" or cmdStr=="look":
		#	roomDesc = rooms[self.loc]["desc"]
		#	roomName = rooms[self.loc]["name"]
		#	mainDesc = roomName + "\n" + roomDesc
		#	sM(self.sessionId,mainDesc)


class MudParse(LineReceiver):
	def __init__(self):
		self.state = "SIGNIN"
		self.name = None
				
	def connectionMade(self):
		self.transport.write("Please enter your username.\n")
		dump(onlinePlayers)
		
	def connectionLost(self, reason):
		if self.name:
			del onlinePlayers[self.name]
			del onlineCharacters[self.charId]
			print ("Lost a user")
		else:
			return
	
	def dataReceived(self, line):
		if self.state == "SIGNIN":
			self.handle_LOGIN(line)
		elif self.state == "PASS":
			self.handle_PASS(line)
		else:
			self.handle_BASIC(line)
	
	def handle_LOGIN(self, message):
		message = message.rstrip()
		if message in onlinePlayers:
			self.transport.write("Player with that name already online, please try another.\n")
			return
		if message in users:
			self.transport.write("Enter password:\n")
			self.name = message
			self.state = "PASS"
		else:
			self.transport.write("Player name not found, please try again.\n")
			return

	def handle_PASS(self, message):
		message = message.rstrip()
		if users[self.name]["pw"] == message:
			self.state = "BASIC"
			self.id = self.name
			self.charId = users[self.name]["charId"]
			onlinePlayers[self.name] = self
			onlineCharacters[self.charId] = CharData(self.charId,self.name)
			stu(self.id,"Welcome, %s" % self.name)
		else:
			self.transport.write("Incorrect password. Please try again.\nEnter password:\n")
			return

	def handle_BASIC(self, message):
		message = message.rstrip()
		if message == "showme":
			msg = "Clients: %s\n" % onlinePlayers.keys()
			stu(self.id,msg)
		elif message == "sendtoall":
			for id in onlinePlayers: #.iteritems():
				stu(id,"This is going to everyone")
		elif message == "info":
			dump(onlinePlayers)
			dump(onlineCharacters)
		else:
#			onlineCharacters[self.charId].parse(message)
			# Simple parser time, adding "to" functionality
			parts = message.split(" ")
			comm = commands.Command(onlineCharacters[self.charId],message)
			comm.parse()
			if len(parts) > 1:
				if parts[0] == "to":
					if parts[1] in onlinePlayers:
						stu(parts[1],"The message to you is %s" % parts[2])
						stu(self.id,"The message sent was %s" % parts[2])
					else:
						stu(self.id,"That player is not online.")
			else:
				stu(self.id,"You typed %s\n" % message)
		print ("Sent BASIC message.")

class MudFactory(Factory):
	def __init__(self):
		self.clients = {}
	
	def buildProtocol(self, addr):
		return MudParse()

	# Sends message with line feed 
def stu(id, message): 
	onlinePlayers[id].transport.write(message + "\n")
	# Sends message without line feed	
def stuL(id, message):
	onlinePlayers[id].transport.write(message)

USER_FILE = "data/users.json"
ROOM_FILE = "data/rooms.json"
CHAR_FILE = "data/characters.json"

if __name__ == '__main__':
	# Set up global variables
	with open(USER_FILE) as user_file:
		users = yaml.safe_load(user_file)
	with open(ROOM_FILE) as room_file:
		rooms = yaml.safe_load(room_file)
	with open(CHAR_FILE) as char_file:
		characters = yaml.safe_load(char_file)
	onlinePlayers = {}
	onlineCharacters = {}
	reactor.listenTCP(4000, MudFactory())
	reactor.run()

