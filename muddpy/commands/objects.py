# object interaction

from util import sTu, getSFChar, sTr, sTup, checkAware, isVowel, returnArgInfo
import world as w
import settings as s

def c_get(ch, rawArgs):
	args = returnArgInfo(rawArgs)
	if args["num"] == 0:
		ch.stu("You have to include what to get.")
	elif args["num"] > 1:
		ch.stu("I don't yet support getting from bags.")
	else:
		here = w.locations[ch.loc]
		ch.stu("This would have been a successful get.")
		
def c_drop(ch, rawArgs):
	args = returnArgInfo(rawArgs)
	if args["num"] == 0:
		ch.stu("You have to include what to drop.")
	elif args["num"] > 1:
		ch.stu("You can only drop one object at a time.")
	else:
		ch.stu("This would have been a successful drop.")

def c_inventory(ch, rawArgs):
	pass
