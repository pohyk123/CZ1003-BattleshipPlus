# CZ1003 Battleship+ [Group Project]
# Contains useful tools such as to store global variables
import config

def setTextbox(text):
	# stores global string variable
	config.displayText = text

def getTextbox():
	# returns global string variable
	return config.displayText

def setUser(username):
	config.user = username
