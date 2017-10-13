from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
from pprint import pprint
from dumper import dump
import commands
import world as w
from util import sTu, sTuL, sTup, sTr

class MudParse(LineReceiver):
	def __init__(self):
		self.state = "SIGNIN"
		self.name = None
				
	def connectionMade(self):
		self.transport.write("Please enter your username.\n")
#		dump(w.onlinePlayers)
		
	def connectionLost(self, reason):
		if self.name:
			del w.onlinePlayers[self.name]
			del w.onlineActors[self.charId]
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
		if message in w.onlinePlayers:
			self.transport.write("Player with that name already online, please try another.\n")
			return
		if message in w.users:
			self.transport.write("Enter password:\n")
			self.name = message
			self.state = "PASS"
		else:
			self.transport.write("Player name not found, please try again.\n")
			return

	def handle_PASS(self, message):
		message = message.rstrip()
		if w.users[self.name]["pw"] == message:
			self.state = "BASIC"
			self.id = self.name
			self.charId = w.users[self.name]["charId"]
			w.onlinePlayers[self.name] = self
			w.onlineActors[self.charId] = w.PC(self.charId,self.name)
			sTu(self.id,"Welcome, %s" % self.name)
			sTr(w.locations[w.onlineActors[self.charId].loc],w.onlineActors[self.charId].name + " has entered the game.",w.onlineActors[self.charId].Id)
			comm = commands.Command(w.onlineActors[self.charId],"look")
			comm.parse()
		else:
			self.transport.write("Incorrect password. Please try again.\nEnter password:\n")
			return

	def handle_BASIC(self, message):
		message = message.rstrip()
		if message == "showme":
			msg = "Clients: %s\n" % w.onlinePlayers.keys()
			sTu(self.id,msg)
		elif message == "sendtoall":
			for id in w.onlinePlayers: 
				sTu(w.onlinePlayers[id].id,"This is going to everyone")
		elif message == "info":
			dump(w.onlinePlayers)
			dump(w.onlineActors)
		elif message == "loc":
			dump(w.locations)
		else:
			comm = commands.Command(w.onlineActors[self.charId],message)
			comm.parse()

class MudFactory(Factory):
	def __init__(self):
		self.clients = {}
	
	def buildProtocol(self, addr):
		return MudParse()

if __name__ == '__main__':
	# Set up global variables
	w.init()
	reactor.listenTCP(4000, MudFactory())
	reactor.run()

