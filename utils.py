# Contains useful tools such as to store global variables

import config

def setTextbox(text):
	config.displayText = text

def getTextbox():
	return config.displayText

def setUser(username):
	config.user = username
