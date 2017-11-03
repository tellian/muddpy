# admin

from util import sTu, getSFChar, sTr, sTup, checkAware, load_new_item
import world as w
import settings as s

def c_loadObj(ch,rawArgs):
	# Check if an item number was provided at all.
	if not (rawArgs and rawArgs.strip()):
		sTu(ch.sId,"You need to include an item number to load.",1)
		return
	# Get just first arg and make sure it is a number
	firstArg = rawArgs.split()[0]
	if firstArg.isdigit():
		if firstArg in w.items:
			load_new_item(firstArg,ch)
			sTu(ch.sId,"Loaded new item.",1)
		else:
			sTu(ch.sId,"There is no object with that number.",1)
	else:
		sTu(ch.sId,"You need to pass a numeric item number.",1)
	
	

