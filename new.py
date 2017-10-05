from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
from pprint import pprint
from dumper import dump
import random

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
	def __init__(self):
			self.stats = Stats()
			self.other = "Misc"

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
		if users[self.name] == message:
			self.transport.write("Welcome, %s\n" % self.name)
			self.state = "BASIC"
			onlinePlayers[self.name] = self
		else:
			self.transport.write("Incorrect password. Please try again.\nEnter password:\n")
			return

	def handle_BASIC(self, message):
		message = message.rstrip()
		if message == "showme":
			msg = "Clients: %s\n" % onlinePlayers.keys()
			self.transport.write(msg)
		elif message == "sendtoall":
			for name, protocol in onlinePlayers.iteritems():
				protocol.transport.write("This is going to everyone\n")
		elif message == "info":
			dump(onlinePlayers)
		else:
			# Simple parser time, adding "to" functionality
			parts = message.split(" ")
			if len(parts) > 1:
				if parts[0] == "to":
					if parts[1] in onlinePlayers:
						onlinePlayers[parts[1]].transport.write("The message to you is %s\n" % parts[2])
						self.transport.write("The message sent was %s\n" % parts[2])
					else:
						self.transport.write("That player is not online.\n")
			else:
				self.transport.write("You typed %s\n" % message)
		print ("Sent BASIC message.")

	def sM(id, message) # Sends message with line feed 
		onlinePlayers[id].transport.write(message + "\n")
		
	def sMN(id, message) # Sends message without line feed
		onlinePlayers[id].transport.write(message)
	
	
class MudFactory(Factory):
	def __init__(self):
		self.clients = {}
	
	def buildProtocol(self, addr):
		return MudParse()

if __name__ == '__main__':
	# Set up global variables
	users = {'tarrenn' : 'tarrenn', 'tellian':'tellian'}
	onlinePlayers = {}
	reactor.listenTCP(4000, MudFactory())
	reactor.run()

