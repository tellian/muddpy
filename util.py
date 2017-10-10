from 

def stu(id, message): 
	onlinePlayers[id].transport.write(message + "\n")
	# Sends message without line feed	
def stuL(id, message):
	onlinePlayers[id].transport.write(message)

