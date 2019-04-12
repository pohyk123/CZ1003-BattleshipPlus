# CZ1003 Battleship+ [Group Project]
# This module handles the entire gameflow from a high-level aspect.

# Import libraries
import pygame
import random
import time
import copy
import sys
from map import Map
from accMgtTools import login, register, unlockAcc
from widgets import Button, InputBox, drawText
from utils import setTextbox, getTextbox
from widgets import drawText

#=================== Configuration & Constant Values ===================
# pygame config
display_width = 950
display_height = 500

# game refresh rate
clock = pygame.time.Clock()
fps = 30

# initialise pygame
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('CZ1003-BattleshipPlus')

# game parameters
# 10 x 10 square grid board
board_dim = 10
# square tile dimension in pixels
tile_size = 40
# top left corner pixel location of map (above sea)
x_sea,y_sea = 50,50
# top left corner pixel location of map (sub sea)
x_sub,y_sub = 500,50

# various color definitions
white = (255,255,255)
dark_white = (220,220,220)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
ready_but_color = (204,204,0)
ready_but_active_color = (255,255,0)

# Import images
# Background images
battle_waterIMG = pygame.image.load('./img/battle_water.png').convert_alpha()
bckgrnd_waterIMG = pygame.image.load('./img/dark_water.png').convert_alpha()
battle_underwaterIMG = pygame.image.load('./img/subsea.png').convert_alpha()
login_welcomeIMG = pygame.image.load('./img/intro_page.png').convert_alpha()
gameover_winIMG = pygame.image.load('./img/game_over_win.png').convert_alpha()
gameover_loseIMG = pygame.image.load('./img/game_over_lose.png').convert_alpha()

# Sprite and effect images
battleshipIMG = pygame.image.load('./img/battleship.png').convert_alpha()
submarineIMG = pygame.image.load('./img/submarine.png').convert_alpha()
hitIMG = pygame.image.load('./img/hit_marker.png').convert_alpha()
missIMG = pygame.image.load('./img/miss_marker.png').convert_alpha()

# Aggregate images as an argument to construct Map object
images = {
		 'bckgrnd_waterIMG':bckgrnd_waterIMG,
		 'battleshipIMG':battleshipIMG,
		 'submarineIMG':submarineIMG,
		 'hitIMG':hitIMG,
		 'missIMG':missIMG
		 }

# legend for board tile locations. Made so letters/numbers are not continuously rendered.
letters = (
	pygame.font.Font('freesansbold.ttf',25).render('A', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('B', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('C', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('D', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('E', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('F', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('G', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('H', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('I', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('J', False, ready_but_color))

nums = (
	pygame.font.Font('freesansbold.ttf',25).render('1', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('2', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('3', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('4', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('5', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('6', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('7', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('8', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('9', False, ready_but_color),
	pygame.font.Font('freesansbold.ttf',25).render('10', False, ready_but_color))

# In-game font types
textFont = pygame.font.SysFont('Comic Sans MS', 15)
BASICFONT = pygame.font.Font('freesansbold.ttf', 25)
BIGFONT = pygame.font.Font('freesansbold.ttf', 35)

# Global buttons
BTRestart = Button("Restart", (700, 480), None, bg=(100,200,200), size=(150, 30))
BTLogout = Button("Logout", (855, 480), None, bg=(100,200,200), size=(150, 30))

#======================================================================
#============================ Helper functions ========================
def AI_prepfield():
	"""
	Creates an above-sea and sub-sea map, then randomly placing 1 ship object & 1 submarine object respectively

	Returns
	-------
	Tuple of 2 Map objects
		First Map object contains the enemy's above-sea placements & second contains enemy's sub-sea placements

	"""

	# constants
	rot = ['H','V']

	# instantiate enemy map (above sea) instance
	m_sea = Map(board_dim,x_sea,y_sea,tile_size,battle_waterIMG,total_ships=1)
	m_sea.images = images
	m_sea.nums = nums
	m_sea.letters = letters

	# instantiate enemy map (subsea) instance
	m_sub = Map(board_dim,x_sub,y_sub,tile_size,battle_underwaterIMG,total_ships=1)
	m_sub.images = images
	m_sub.nums = nums
	m_sub.letters = letters

	# keep adding ships until 2 valid ships are added
	while(len(m_sea.ships) + len(m_sub.ships) < 2):
		i,mouse_x,mouse_y = random.randint(0,1),random.randint(0,display_width),random.randint(0,display_height)
		m_sea.addShip((mouse_x,mouse_y),4,rot[i],battleshipIMG)
		m_sub.addShip((mouse_x,mouse_y),3,rot[i],submarineIMG)

	return m_sea,m_sub


def updateTextbox(display_surface):
	"""
	Updates in-game description textfield displayed during gameplay.

	Parameters
	----------
	display_surface : pygame.Surface object
		Game screen initialised before start of game.

	"""
	# Gets updated text description and update in-game text field
	pygame.draw.rect(display_surface,(200,200,200),(45,455,865,40),0)
	text = textFont.render(getTextbox(), 1, (0, 0, 0))
	display_surface.blit(text,(50,460))

#======================================================================
#======================= (Looping) Game Phases ========================

def fieldprepLoop(display_surface):
	"""
	Looping function for field preparation phase. Moves onto the next phase when
	all required ships are appropriately placed.

	Parameters
	----------
	display_surface : pygame.Surface object
		Game screen initialised before start of game.

	Returns
	-------
	string
		Title of next chosen phase.
	Tuple of 2 Map objects
		First Map object player's above-sea placements & second contains player's sub-sea placements
.    Tuple of 2 Map objects
		First Map object contains the enemy's above-sea placements & second contains enemy's sub-sea placements

	"""
	# initialise variables
	subPhase = 'sea' # sea or subsea mode; begins with above-sea ship placement
	rot = 'H'
	mouse_x = mouse_y = 0
	setTextbox('Please place 1 ship in left map! (Above water)') # verbose

	# play music
	pygame.mixer.music.load("./audio/fieldprep.mp3")
	pygame.mixer.music.play(-1,0.0)

	# instantiate player map (above sea) instance
	m_sea = Map(board_dim,x_sea,y_sea,tile_size,battle_waterIMG,total_ships=4)
	m_sea.images = images
	m_sea.nums = nums
	m_sea.letters = letters

	# instantiate player map (subsea) instance
	m_sub = Map(board_dim,x_sub,y_sub,tile_size,battle_underwaterIMG,total_ships=4)
	m_sub.images = images
	m_sub.nums = nums
	m_sub.letters = letters

	# verbose
	print('Maps initialised, starting field prep phase.')

	# Begin field preparation loop
	while True:
		# Switch phase when all ships are placed
		if len(m_sea.ships) == 1 and len(m_sub.ships) == 0:
			subPhase = 'subsea'
			setTextbox('Please place 1 submarine in either map!') # verbose
		# Move to next phase when all ships are placed
		if (len(m_sea.ships) + len(m_sub.ships) == 2):
			setTextbox('All ships have been placed!') # verbose
			break
		# check for user input
		for event in pygame.event.get():
			# Get mouse position
			mouse_x, mouse_y = pygame.mouse.get_pos()
			# checks if user wants to quit
			if 	event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type ==  pygame.MOUSEBUTTONDOWN:
				# Checks if user presses restart/logout buttons
				if BTRestart.isPressed((mouse_x,mouse_y)):
					return 'fieldprep', None, None
				if BTLogout.isPressed((mouse_x,mouse_y)):
					return 'login', None, None
				# left click to drop ship on above/sub-sea map
				if event.button == 1:
					if(subPhase == 'sea'):
						m_sea.addShip((mouse_x,mouse_y),4,rot,battleshipIMG)
					if(subPhase == 'subsea'):
						m_sea.addShip((mouse_x,mouse_y),3,rot,submarineIMG)
						m_sub.addShip((mouse_x,mouse_y),3,rot,submarineIMG)
				# right click to switch ship orientation
				if event.button == 3:
					if(rot == 'H'):
						rot = 'V'
					else:
						rot = 'H'

		# draw background
		display_surface.fill(white)
		display_surface.blit(bckgrnd_waterIMG,(0,0))

		# draw dynamic elements
		m_sea.drawMap(display_surface)
		m_sea.drawShips(display_surface)
		m_sub.drawMap(display_surface)
		m_sub.drawShips(display_surface)
		updateTextbox(display_surface)
		BTRestart.draw(display_surface)
		BTLogout.draw(display_surface)

		# make ship follow cursor
		if(subPhase == 'sea'):
			if(rot == 'H'):
				display_surface.blit(battleshipIMG,(mouse_x,mouse_y))
			else:
				display_surface.blit(pygame.transform.rotate(battleshipIMG,90),(mouse_x-5,mouse_y-5))
		else:
			if(rot == 'H'):
				display_surface.blit(submarineIMG,(mouse_x,mouse_y))
			else:
				display_surface.blit(pygame.transform.rotate(submarineIMG,90),(mouse_x-5,mouse_y-5))

		pygame.display.update()
		# pygame refresh rate
		clock.tick(fps)

	# draw final ship placements
	m_sea.drawMap(display_surface)
	m_sea.drawShips(display_surface)
	m_sub.drawMap(display_surface)
	m_sub.drawShips(display_surface)

	setTextbox('All ships have been placed, please wait while the enemy prepares...') # verbose

	updateTextbox(display_surface)
	pygame.display.update()

	time.sleep(0.5)

	# Create enemy maps
	m_sea_enemy,m_sub_enemy = AI_prepfield()

	return 'battle', (m_sea,m_sub), (m_sea_enemy,m_sub_enemy)


def endgameLoop(display_surface,winner):
	"""
	Looping function for end-game phase. Displays whether player has won/lost.
	Player can choose to restart, logout or close window.

	Parameters
	----------
	display_surface : pygame.Surface object
		Game screen initialised before start of game.
	winner : string
		Winner of game - 'player' or 'enemy'.

	Returns
	-------
	string
		Title of next chosen phase.

	"""

	# Plays victory or gameover music
	if(winner=='player'):
		pygame.mixer.music.load("./audio/victory.mp3")
		pygame.mixer.music.play(1,0.0)
	else:
		pygame.mixer.music.load("./audio/gameover.mp3")
		pygame.mixer.music.play(1,0.0)

	# Begin endgame preparation loop
	while True:
		# check for user input
		for event in pygame.event.get():
			#Get mouse position
			mouse_x, mouse_y = pygame.mouse.get_pos()
			#check if user wants to quit
			if 	event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type ==  pygame.MOUSEBUTTONDOWN:
				# Checks if user presses restart/logout buttons
				if BTRestart.isPressed((mouse_x,mouse_y)):
					return 'fieldprep'
				if BTLogout.isPressed((mouse_x,mouse_y)):
					return 'login'

		# display win or lose image
		if(winner=='player'):
			display_surface.blit(gameover_winIMG,(0,0))
		else:
			display_surface.blit(gameover_loseIMG,(0,0))

		# draw dynamic elements
		BTRestart.draw(display_surface)
		BTLogout.draw(display_surface)

		pygame.display.update()
		# pygame refresh rate
		clock.tick(fps)


def battleLoop(display_surface,finalBoardLayout_human, finalBoardLayout_AI):
	"""
	Looping function for battle phase. Player enters a turn-based gameflow against
	the AI enemy, until either party wins the game.

	Parameters
	----------
	display_surface : pygame.Surface object
		Game screen initialised before start of game.
	finalBoardLayout_human : Tuple of 2 Map objects
		First Map object player's above-sea placements & second contains player's sub-sea placements.
	finalBoardLayout_AI : Tuple of 2 Map objects
		First Map object contains the enemy's above-sea placements & second contains enemy's sub-sea placements.

	Returns
	-------
	string
		Title of next chosen phase.
	string
		Winner of game - 'player' or 'enemy'.

	"""

	# initialise variables
	mouse_x = mouse_y = 0
	phase = 'player' #player's or cpu's turn; begins with player
	winner = ''
	turnover = 0
	enemy_turnover = 0

	# unbundle maps
	m_sea,m_sub = finalBoardLayout_human
	m_sea_enemy,m_sub_enemy = finalBoardLayout_AI

	setTextbox('Start of Battle Phase - get prepared!') # verbose
	time.sleep(0.5)

	# play exciting music
	pygame.mixer.music.load("./audio/battle.mp3")
	pygame.mixer.music.play(-1,0.0)

	# Begin endgame preparation loop
	while True:
		if(phase=='player'):
			setTextbox("It's your turn! Start by choosing a target on either maps.") # verbose

			# generate player view
			# draw background
			display_surface.fill(white)
			display_surface.blit(bckgrnd_waterIMG,(0,0))

			# draw dynamic elements
			m_sea_enemy.drawMap(display_surface)
			m_sub_enemy.drawMap(display_surface)
			m_sea_enemy.drawTries(display_surface)
			m_sub_enemy.drawTries(display_surface)
			updateTextbox(display_surface)
			BTRestart.draw(display_surface)
			BTLogout.draw(display_surface)
			pygame.display.update()

			# loop until player makes a valid move
			while(turnover == 0):
				for event in pygame.event.get():
					# Get mouse position
					mouse_x, mouse_y = pygame.mouse.get_pos()
					# check if user wants to quit
					if 	event.type == pygame.QUIT:
						pygame.quit()
						quit()
					if event.type ==  pygame.MOUSEBUTTONDOWN:
						# Checks if user presses restart/logout buttons
						if BTRestart.isPressed((mouse_x,mouse_y)):
							return 'fieldprep', None
						if BTLogout.isPressed((mouse_x,mouse_y)):
							return 'login', None
						if event.button == 1: # left click to target area
							print('\n[Above sea] ', end='')
							valid_hit_sea = m_sea_enemy.hit_xy((mouse_x,mouse_y)) # attempt to hit target area (above sea)
							print('\n[Sub sea] ', end='')
							print()
							valid_hit_subsea = m_sub_enemy.hit_xy((mouse_x,mouse_y)) # attempt to hit target area (sub sea)
							m_sea_enemy.getMapState()
							print()
							m_sub_enemy.getMapState()
							turnover = valid_hit_sea!=-1 or valid_hit_subsea!=-1 # turn is over if player made a valid move

			turnover = 0 # reset turn for next turn

			# update dynamic elements
			m_sea_enemy.drawMap(display_surface)
			m_sub_enemy.drawMap(display_surface)
			m_sea_enemy.drawTries(display_surface)
			m_sub_enemy.drawTries(display_surface)
			updateTextbox(display_surface)

			pygame.display.update()
			time.sleep(1)

			# early stopping if player wins game
			if(len(m_sea_enemy.getAliveShips())==0 and len(m_sub_enemy.getAliveShips())==0):
				winner = 'player'
				break
			phase = 'enemy'

		else:
			#draw background
			display_surface.fill(white)
			display_surface.blit(bckgrnd_waterIMG,(0,0))

			setTextbox("Enemy's turn.") # verbose

			# update dynamic elements
			m_sea.drawMap(display_surface)
			m_sub.drawMap(display_surface)
			m_sea.drawShips(display_surface)
			m_sub.drawShips(display_surface)
			m_sea.drawTries(display_surface)
			m_sub.drawTries(display_surface)
			updateTextbox(display_surface)

			pygame.display.update()
			time.sleep(1)

			# loop until enemy makes a valid move
			while(enemy_turnover == 0):
				# set offensive AI heuristic here
				mouse_x,mouse_y = random.randint(0,display_width),random.randint(0,display_height) # random target generator
				print('\n[Above sea] ', end='')
				valid_hit_sea = m_sea.hit_xy((mouse_x,mouse_y)) # attempt to hit target area (above sea)
				print('\n[Sub sea] ', end='')
				print()
				valid_hit_subsea = m_sub.hit_xy((mouse_x,mouse_y)) # attempt to hit target area (sub sea)
				m_sea.getMapState()
				print()
				m_sub.getMapState()
				enemy_turnover = valid_hit_sea!=-1 or valid_hit_subsea!=-1 # turn is over if enemy made a valid move

			enemy_turnover = 0 # reset for next turn

			# update dynamic elements
			m_sea.drawMap(display_surface)
			m_sub.drawMap(display_surface)
			m_sea.drawShips(display_surface)
			m_sub.drawShips(display_surface)
			m_sea.drawTries(display_surface)
			m_sub.drawTries(display_surface)
			updateTextbox(display_surface)

			pygame.display.update()
			time.sleep(1)

			# early stopping if enemy wins game
			if(len(m_sea.getAliveShips())==0 and len(m_sub.getAliveShips())==0):
				winner = 'enemy'
				break
			phase = 'player'

		# pygame refresh rate
		clock.tick(fps)

	print('Game has ended!') # verbose
	# declare winner
	if(winner=='player'):
		setTextbox('You win!') # verbose
	else:
		setTextbox('You lose! Try again next time.') # verbose

	# update dyanmic elements
	updateTextbox(display_surface)

	pygame.display.update()
	time.sleep(0.5)

	return 'endgame',winner


def displayCreateAcc(display_surface):
	"""
	Allows user to create new account.

	Parameters
	----------
	display_surface : pygame.Surface object
		Game screen initialised before start of game.

	Returns
	-------
	string
		Title of next chosen (login) phase.

	"""
	# instantiate widgets
	# BT = button, IB = input (text) box
	BTRegister = Button("Create Account", (700, 250), register, bg=(100,200,200))
	BTBack = Button("Back", (700, 150), None, bg=(100,200,200))
	IBUsername = InputBox(320, 125, 200, 40)
	IBPassword = InputBox(320, 195, 200, 40)
	IBDob = InputBox(320, 265, 200, 40)

	buttons = [BTBack,BTRegister]
	inputBoxes = [IBUsername,IBPassword,IBDob]

	# Loop page until user makes a valid option
	while True:
		mouse_pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# gets username, password & dob (registration details) from input text fields & check for validity before
				# confirming sign up
				success = BTRegister.mousebuttondown(mouse_pos,usr=IBUsername.text,pwd=IBPassword.text,date=IBDob.text)
				if(success == 0):
					setTextbox('Password is too weak!') # verbose
				elif(success == 1):
					return 'login' # return to login screen if successful registration
				elif(success == 2):
					setTextbox('User already exists!') # verbose
				elif(success == -1):
					setTextbox('Invalid DoB!') # verbose
				else:
					pass
				if(BTBack.isPressed(mouse_pos)):
					return 'login' # return to login screen if back button pressed
			for box in inputBoxes:
				box.handle_event(event)

		# update screen display
		# draw background & static elements
		display_surface.fill(white)
		display_surface.blit(login_welcomeIMG,(0,0))
		drawText('\xa9 CZ1003 FS1 NG-19_POH-20_SUTANTYO-21',textFont,display_surface,600,470,black)
		drawText('Password must have the following:',textFont,display_surface,600,300,black)
		drawText('1. >8 chars',textFont,display_surface,600,320,black)
		drawText('2. At least 1 upper & 1 lower case',textFont,display_surface,600,340,black)
		drawText('3. At least 1 digit and special symbol',textFont,display_surface,600,360,black)
		drawText('4. Cannot contain username',textFont,display_surface,600,380,black)
		drawText('Username:',BASICFONT,display_surface,160,125,black)
		drawText('Password:',BASICFONT,display_surface,160,195,black)
		drawText('DOB (DD/MM/YYYY):',BASICFONT,display_surface,50,265,black)
		for button in buttons:
			button.draw(display_surface)
		for box in inputBoxes:
			box.draw(display_surface)

		# update dynamic elements
		drawText(getTextbox(),BASICFONT,display_surface,160,335,red)

		pygame.display.update()
		# pygame refresh rate
		clock.tick(fps)


def displayUnlockAcc(display_surface):
	"""
	Allows user to unlock account

	Parameters
	----------
	display_surface : pygame.Surface object
		Game screen initialised before start of game.

	Returns
	-------
	string
		Title of next chosen (login) phase.

	"""

	# instantiate widgets
	# BT = button, IB = input (text) box
	BTUnlockAcc = Button("Unlock Account", (700, 250), unlockAcc, bg=(100,200,200))
	BTBack = Button("Back", (700, 150), None, bg=(100,200,200))
	IBUsername = InputBox(320, 125, 200, 40)
	IBDob = InputBox(320, 195, 200, 40)

	buttons = [BTBack,BTUnlockAcc]
	inputBoxes = [IBUsername,IBDob]

	# Loop page until user makes a valid option
	while True:
		mouse_pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# gets username & dob (account details) from input text fields & check for validity before
				# confirming unlock
				success = BTUnlockAcc.mousebuttondown(mouse_pos,usr=IBUsername.text,date=IBDob.text)
				if(success == 1):
					setTextbox('Your account is now unlocked!') # verbose
				elif(success == -1):
					setTextbox('User does not exist!') # verbose
				else:
					pass
				if(BTBack.isPressed(mouse_pos)):
					return 'login'
			for box in inputBoxes:
				box.handle_event(event)

		# update screen display
		# draw background & static elements
		display_surface.fill(white)
		display_surface.blit(login_welcomeIMG,(0,0))
		drawText('\xa9 CZ1003 FS1 NG-19_POH-20_SUTANTYO-21',textFont,display_surface,600,470,black)
		drawText('Username:',BASICFONT,display_surface,160,125,black)
		drawText('DOB (DD/MM/YYYY):',BASICFONT,display_surface,50,195,black)
		for button in buttons:
			button.draw(display_surface)
		for box in inputBoxes:
			box.draw(display_surface)

		# update dynamic elements
		drawText(getTextbox(),BASICFONT,display_surface,160,335,red)

		pygame.display.update()
		# pygame refresh rate
		clock.tick(fps)


def displayLogin(display_surface):
	"""
	Allows user to login.

	Parameters
	----------
	display_surface : pygame.Surface object
		Game screen initialised before start of game.

	Returns
	-------
	string
		Title of next chosen (login) phase.

	"""
	# define widgets used in this function
	# instantiate widgets
	# BT = button, IB = input (text) box
	BTLogin = Button("Login", (700, 150), login, bg=(100,200,200))
	BTCreateAcc = Button("Create Account", (700, 250), None, bg=(100,200,200))
	BTUnlockAcc = Button("Unlock Account", (700, 350), None, bg=(100,200,200))
	IBUsername = InputBox(320, 125, 200, 40)
	IBPassword = InputBox(320, 195, 200, 40)

	buttons = [BTLogin,BTCreateAcc,BTUnlockAcc]
	inputBoxes = [IBUsername,IBPassword]
	setTextbox('Welcome to BattleshipPlus!') # verbose

	tries = 0

	# Loop page until user successfully logs in or changes page
	while True:
		mouse_pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# gets username & pw (account details) from input text fields & check for validity before
				# confirming login
				success = BTLogin.mousebuttondown(mouse_pos,usr=IBUsername.text,pwd=IBPassword.text,tries=tries)
				if(success == 0):
					setTextbox('Your account is locked!') # verbose
				elif(success == 1):
					return 'startGame'
				elif(success == 2):
					tries+=1
					setTextbox('Password wrong!') # verbose
				elif(success == -1):
					setTextbox('User does not exist!') # verbose
				else:
					pass

				# Options to go other pages
				if(BTCreateAcc.isPressed(mouse_pos)):
					print('createAcc')
					return 'createAcc'
				if(BTUnlockAcc.isPressed(mouse_pos)):
					print('unlockAcc')
					return 'unlockAcc'

			for box in inputBoxes:
				box.handle_event(event)

			# update screen display
			# draw background
			display_surface.fill(white)
			display_surface.blit(login_welcomeIMG,(0,0))
			drawText('\xa9 CZ1003 FS1 NG-19_POH-20_SUTANTYO-21',textFont,display_surface,600,470,black)
			drawText('Username:',BASICFONT,display_surface,160,125,black)
			drawText('Password:',BASICFONT,display_surface,160,195,black)

			# update dynamic elements
			drawText(getTextbox(),BASICFONT,display_surface,160,335,red)

			for button in buttons:
				button.draw(display_surface)
			for box in inputBoxes:
				box.draw(display_surface)

			pygame.display.update()
			# pygame refresh rate
			clock.tick(fps)


def loginLoop(display_surface):
	"""
	Overarching loop handling login, create account & unlock account functions

	Parameters
	----------
	display_surface : pygame.Surface object
		Game screen initialised before start of game.

	Returns
	-------
	string
		Title of next chosen phase.

	"""
	screen = 'login' # initial screen

	# play exciting music
	pygame.mixer.music.load("./audio/menu.mp3")
	pygame.mixer.music.play(-1,0.0)

	# state transition between different screens
	while True:
		print(screen)
		if(screen == 'login'):
			screen = displayLogin(display_surface)
		if(screen == 'createAcc'):
			screen = displayCreateAcc(display_surface)
		if(screen == 'unlockAcc'):
			screen = displayUnlockAcc(display_surface)
		if(screen == 'startGame'):
			return 'fieldprep'

#======================================================================
#==================== Actual Gameplay starts here =====================
phase = 'login' # initial phase

# main loop that transitions between 5 different game phases
while(True):
	print('Entering phase {}'.format(phase))
	if(phase=='login'):
		phase = loginLoop(gameDisplay)
	if(phase=='fieldprep'):
		phase, finalBoardLayout_human, finalBoardLayout_AI = fieldprepLoop(gameDisplay)
	if(phase=='battle'):
		phase, battleResult = battleLoop(gameDisplay,finalBoardLayout_human, finalBoardLayout_AI)
	if(phase=='endgame'):
		phase = endgameLoop(gameDisplay,battleResult)

pygame.quit()
