from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
from pprint import pprint
from dumper import dump

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
	def __init__(self, factory):
		self.factory = factory
		#self.player = Player()
		#self.character = CharData()
		self.state = "INTRO"
		#self.cclass = "Coercer"
		#dump(self)
				
	def connectionMade(self):
		#self.transport.write("Welcome to the New Mud!")
		#print ("Gained a user")
		#dump(self)
		#dump(self.transport)
		self.factory.clients.append(self)
		dump(self)
		print("Connection made from %s" % self.getPeer())
		pass
		
	def connectionLost(self, reason):
		print ("Lost a user")
	
	def dataReceived(self, line):
		if self.state == "INTRO":
			self.handle_INTRO(line)
		else:
			self.handle_BASIC(line)
	
	def handle_INTRO(self, message):
		self.sendLine("Intro line")
		print ("Sent Intro Line")
		self.state = "BASIC"
	
	def handle_BASIC(self, message):
		self.sendLine("You typed %s" % message)
		print ("Sent BASIC message.")

class MudFactory(Factory):
	def __init__(self):
		self.clients = []
	
	def buildProtocol(self, addr):
		return MudParse(self)

if __name__ == '__main__':
	
	reactor.listenTCP(4000, MudFactory())
	reactor.run()

