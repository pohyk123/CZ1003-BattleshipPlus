import pygame
import random
from map import Map
from accMgr import login, register, unlockAcc
from widgets import Button, InputBox, drawText
from utils import setTextbox, getTextbox
from widgets import drawText
import time
import copy
import sys
# from player import Player

#========================================================================
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

#========================================================================
# game parameters
#both height and width of board blocks 10x10 board
board_dim = 10
#square tile dimension in pixels
tile_size = 40
#top left corner pixel location of map (above sea)
x_sea,y_sea = 50,50
#top left corner pixel location of map (sub sea)
x_sub,y_sub = 500,50

#various color definitions
white = (255,255,255)
dark_white = (220,220,220)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
ready_but_color = (204,204,0)
ready_but_active_color = (255,255,0)

#Import images
battle_waterIMG = pygame.image.load('./img/battle_water.png').convert_alpha()
bckgrnd_waterIMG = pygame.image.load('./img/dark_water.png').convert_alpha()
battle_underwaterIMG = pygame.image.load('./img/subsea.png').convert_alpha()
login_welcomeIMG = pygame.image.load('./img/intro_page.png').convert_alpha()

gameover_winIMG = pygame.image.load('./img/game_over_win.png').convert_alpha()
gameover_loseIMG = pygame.image.load('./img/game_over_lose.png').convert_alpha()

battleshipIMG = pygame.image.load('./img/battleship.png').convert_alpha()
submarineIMG = pygame.image.load('./img/submarine.png').convert_alpha()

hitIMG = pygame.image.load('./img/hit_marker.png').convert_alpha()
missIMG = pygame.image.load('./img/miss_marker.png').convert_alpha()

images = {
		 'bckgrnd_waterIMG':bckgrnd_waterIMG,
		 'battleshipIMG':battleshipIMG,
		 'submarineIMG':submarineIMG,
		 'hitIMG':hitIMG,
		 'missIMG':missIMG
		 }


#legend for board tile locations. Made so letters/numbers are not continuously rendered.
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

textFont = pygame.font.SysFont('Comic Sans MS', 15)
BASICFONT = pygame.font.Font('freesansbold.ttf', 25)
BIGFONT = pygame.font.Font('freesansbold.ttf', 35)

# Global buttons
BTRestart = Button("Restart", (700, 480), None, bg=(100,200,200), size=(150, 30))
BTLogout = Button("Logout", (855, 480), None, bg=(100,200,200), size=(150, 30))

#========================================================================


def AI_prepfield():
	#instantiate player map (above sea) instance
	m_sea = Map(board_dim,x_sea,y_sea,tile_size,battle_waterIMG,total_ships=1)
	m_sea.images = images
	m_sea.nums = nums
	m_sea.letters = letters

	#instantiate player map (subsea) instance
	m_sub = Map(board_dim,x_sub,y_sub,tile_size,battle_underwaterIMG,total_ships=1)
	m_sub.images = images
	m_sub.nums = nums
	m_sub.letters = letters

	rot = ['H','V']

	# keep adding ships until 2 valid ships are added
	while(len(m_sea.ships) + len(m_sub.ships) < 2):
		i,mouse_x,mouse_y = random.randint(0,1),random.randint(0,display_width),random.randint(0,display_height)
		m_sea.addShip((mouse_x,mouse_y),4,rot[i],battleshipIMG)
		m_sub.addShip((mouse_x,mouse_y),3,rot[i],submarineIMG)

	return m_sea,m_sub

def updateTextbox(display_surface):
	# print(config.displayText)
	pygame.draw.rect(display_surface,(200,200,200),(45,455,865,40),0)
	text = textFont.render(getTextbox(), 1, (0, 0, 0))
	display_surface.blit(text,(50,460))

def fieldprepLoop(display_surface):
	mouse_x = mouse_y = 0
	#instantiate player map (above sea) instance
	m_sea = Map(board_dim,x_sea,y_sea,tile_size,battle_waterIMG,total_ships=4)
	m_sea.images = images
	m_sea.nums = nums
	m_sea.letters = letters

	#instantiate player map (subsea) instance
	m_sub = Map(board_dim,x_sub,y_sub,tile_size,battle_underwaterIMG,total_ships=4)
	m_sub.images = images
	m_sub.nums = nums
	m_sub.letters = letters

	#main loop for the prep phase
	print('Maps initialised, starting field prep phase.')

	subPhase = 'sea' #sea or subsea mode
	rot = 'H'
	setTextbox('Please place 1 ship in left map! (Above water)')

	pygame.mixer.music.load("./audio/fieldprep.mp3")
	pygame.mixer.music.play(-1,0.0)


	while True:
		#Switch phase when all ships are placed
		if len(m_sea.ships) == 1 and len(m_sub.ships) == 0:
			subPhase = 'subsea'
			setTextbox('Please place 1 submarine in either map!')
		#Move to next phase when all ships are placed
		if (len(m_sea.ships) + len(m_sub.ships) == 2):
			setTextbox('All ships have been placed!')
			break
		# check for user input
		for event in pygame.event.get():
			#Get mouse position
			mouse_x, mouse_y = pygame.mouse.get_pos()
			#check if user wants to quit
			if 	event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type ==  pygame.MOUSEBUTTONDOWN:
				if BTRestart.isPressed((mouse_x,mouse_y)):
					return 'fieldprep', None, None
				if BTLogout.isPressed((mouse_x,mouse_y)):
					return 'login', None, None

				if event.button == 1: # left click to drop ship
					if(subPhase == 'sea'):
						m_sea.addShip((mouse_x,mouse_y),4,rot,battleshipIMG)
					if(subPhase == 'subsea'):
						m_sea.addShip((mouse_x,mouse_y),3,rot,submarineIMG)
						m_sub.addShip((mouse_x,mouse_y),3,rot,submarineIMG)
				if event.button == 3: # right click to switch ship orientation
					if(rot == 'H'):
						rot = 'V'
					else:
						rot = 'H'

		#draw background
		display_surface.fill(white)
		display_surface.blit(bckgrnd_waterIMG,(0,0))

		#draw dynamic elements
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
		clock.tick(fps)

	#include confimration here?
	m_sea.drawMap(display_surface)
	m_sea.drawShips(display_surface)
	m_sub.drawMap(display_surface)
	m_sub.drawShips(display_surface)

	setTextbox('All ships have been placed, please wait while the enemy prepares...')

	updateTextbox(display_surface)
	pygame.display.update()

	time.sleep(0.5)
	# m_sea_enemy,m_sub_enemy = AI_prepfield()
	m_sea_enemy,m_sub_enemy = AI_prepfield()

	return 'battle', (m_sea,m_sub), (m_sea_enemy,m_sub_enemy)

def endgameLoop(display_surface,winner):

	if(winner=='player'):
		pygame.mixer.music.load("./audio/victory.mp3")
		pygame.mixer.music.play(1,0.0)
	else:
		pygame.mixer.music.load("./audio/gameover.mp3")
		pygame.mixer.music.play(1,0.0)

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
				if BTRestart.isPressed((mouse_x,mouse_y)):
					return 'fieldprep'
				if BTLogout.isPressed((mouse_x,mouse_y)):
					return 'login'

		if(winner=='player'):
			display_surface.blit(gameover_winIMG,(0,0))
		else:
			display_surface.blit(gameover_loseIMG,(0,0))

		BTRestart.draw(display_surface)
		BTLogout.draw(display_surface)
		pygame.display.update()
		clock.tick(fps)


def battleLoop(display_surface,finalBoardLayout_human, finalBoardLayout_AI):
	mouse_x = mouse_y = 0
	# unbundle maps
	m_sea,m_sub = finalBoardLayout_human
	m_sea_enemy,m_sub_enemy = finalBoardLayout_AI
	phase = 'player' #player or cpu
	winner = ''
	turnover = 0
	enemy_turnover = 0

	setTextbox('Start of Battle Phase - get prepared!')
	time.sleep(0.5)

	pygame.mixer.music.load("./audio/battle.mp3")
	pygame.mixer.music.play(-1,0.0)

	while True:
		if(phase=='player'):
			#generate player view
			#draw background
			display_surface.fill(white)
			display_surface.blit(bckgrnd_waterIMG,(0,0))
			setTextbox("It's your turn! Start by choosing a target on either maps.")
			m_sea_enemy.drawMap(display_surface)
			m_sub_enemy.drawMap(display_surface)
			m_sea_enemy.drawTries(display_surface)
			m_sub_enemy.drawTries(display_surface)
			updateTextbox(display_surface)
			BTRestart.draw(display_surface)
			BTLogout.draw(display_surface)
			pygame.display.update()
			while(turnover == 0):
				for event in pygame.event.get():
				#Get mouse position
					mouse_x, mouse_y = pygame.mouse.get_pos()
					#check if user wants to quit
					if 	event.type == pygame.QUIT:
						pygame.quit()
						quit()
					if event.type ==  pygame.MOUSEBUTTONDOWN:
						if BTRestart.isPressed((mouse_x,mouse_y)):
							return 'fieldprep', None
						if BTLogout.isPressed((mouse_x,mouse_y)):
							return 'login', None
						if event.button == 1: # left click to drop ship
							print('\n[Above sea] ', end='')
							valid_hit_sea = m_sea_enemy.hit_xy((mouse_x,mouse_y))
							print('\n[Sub sea] ', end='')
							print()
							valid_hit_subsea = m_sub_enemy.hit_xy((mouse_x,mouse_y))
							m_sea_enemy.getMapState()
							print()
							m_sub_enemy.getMapState()
							turnover = valid_hit_sea!=-1 or valid_hit_subsea!=-1 #turn is over if player choose to hit either map

			turnover = 0
			m_sea_enemy.drawMap(display_surface)
			m_sub_enemy.drawMap(display_surface)
			m_sea_enemy.drawTries(display_surface)
			m_sub_enemy.drawTries(display_surface)
			updateTextbox(display_surface)
			pygame.display.update()
			time.sleep(1)
			if(len(m_sea_enemy.getAliveShips())==0 and len(m_sub_enemy.getAliveShips())==0):
				winner = 'player'
				break
			phase = 'enemy'

		else:
			#draw background
			display_surface.fill(white)
			display_surface.blit(bckgrnd_waterIMG,(0,0))

			setTextbox("Enemy's turn.")
			m_sea.drawMap(display_surface)
			m_sub.drawMap(display_surface)
			m_sea.drawShips(display_surface)
			m_sub.drawShips(display_surface)
			m_sea.drawTries(display_surface)
			m_sub.drawTries(display_surface)
			updateTextbox(display_surface)
			pygame.display.update()

			time.sleep(1)

			while(enemy_turnover == 0):
				# set offensive AI heuristic here
				mouse_x,mouse_y = random.randint(0,display_width),random.randint(0,display_height)
				print('\n[Above sea] ', end='')
				valid_hit_sea = m_sea.hit_xy((mouse_x,mouse_y))
				print('\n[Sub sea] ', end='')
				print()
				valid_hit_subsea = m_sub.hit_xy((mouse_x,mouse_y))
				m_sea.getMapState()
				print()
				m_sub.getMapState()
				enemy_turnover = valid_hit_sea!=-1 or valid_hit_subsea!=-1 #turn is over if player choose to hit either map

			enemy_turnover = 0

			m_sea.drawMap(display_surface)
			m_sub.drawMap(display_surface)
			m_sea.drawShips(display_surface)
			m_sub.drawShips(display_surface)
			m_sea.drawTries(display_surface)
			m_sub.drawTries(display_surface)
			updateTextbox(display_surface)
			pygame.display.update()
			time.sleep(1)
			if(len(m_sea.getAliveShips())==0 and len(m_sub.getAliveShips())==0):
				winner = 'enemy'
				break
			phase = 'player'

		clock.tick(fps)

	print('Game has ended!')
	if(winner=='player'):
		setTextbox('You win!')
	else:
		setTextbox('You lose! Try again next time.')

	updateTextbox(display_surface)
	pygame.display.update()
	time.sleep(0.5)

	return 'endgame',winner

###############################################

def displayCreateAcc(display_surface):
	# instantiate widgets
	# BT = button, IB = input (text) box
	BTRegister = Button("Create Account", (700, 250), register, bg=(100,200,200))
	BTBack = Button("Back", (700, 150), None, bg=(100,200,200))
	IBUsername = InputBox(320, 125, 200, 40)
	IBPassword = InputBox(320, 195, 200, 40)
	IBDob = InputBox(320, 265, 200, 40)

	buttons = [BTBack,BTRegister]
	inputBoxes = [IBUsername,IBPassword,IBDob]
	while True:
		mouse_pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				success = BTRegister.mousebuttondown(mouse_pos,usr=IBUsername.text,pwd=IBPassword.text,date=IBDob.text)
				if(success == 0):
					setTextbox('Password is too weak!')
				elif(success == 1):
					return 'login'
				elif(success == 2):
					setTextbox('User already exists!')
				elif(success == -1):
					setTextbox('Invalid DoB!')
				else:
					pass
				if(BTBack.isPressed(mouse_pos)):
					return 'login'
			for box in inputBoxes:
				box.handle_event(event)

		# update screen display
		#draw background
		display_surface.fill(white)
		display_surface.blit(login_welcomeIMG,(0,0))
		drawText('\xa9 CZ1003 FS1 NG-19_POH-20_SUTANTYO-21',textFont,display_surface,600,470,black)
		drawText(getTextbox(),BASICFONT,display_surface,160,335,red)

		drawText('Username:',BASICFONT,display_surface,160,125,black)
		drawText('Password:',BASICFONT,display_surface,160,195,black)
		drawText('DOB (DD/MM/YYYY):',BASICFONT,display_surface,50,265,black)
		for button in buttons:
			button.draw(display_surface)
		for box in inputBoxes:
			box.draw(display_surface)

		pygame.display.update()
		clock.tick(fps)

def displayUnlockAcc(display_surface):
	# instantiate widgets
	# BT = button, IB = input (text) box
	BTUnlockAcc = Button("Unlock Account", (700, 250), unlockAcc, bg=(100,200,200))
	BTBack = Button("Back", (700, 150), None, bg=(100,200,200))
	IBUsername = InputBox(320, 125, 200, 40)
	IBDob = InputBox(320, 195, 200, 40)

	buttons = [BTBack,BTUnlockAcc]
	inputBoxes = [IBUsername,IBDob]
	while True:
		mouse_pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				success = BTUnlockAcc.mousebuttondown(mouse_pos,usr=IBUsername.text,date=IBDob.text)
				if(success == 1):
					setTextbox('Your account is now unlocked!')
				elif(success == -1):
					setTextbox('User does not exist!')
				else:
					pass
				if(BTBack.isPressed(mouse_pos)):
					return 'login'
			for box in inputBoxes:
				box.handle_event(event)

		# update screen display
		#draw background
		display_surface.fill(white)
		display_surface.blit(login_welcomeIMG,(0,0))
		drawText('\xa9 CZ1003 FS1 NG-19_POH-20_SUTANTYO-21',textFont,display_surface,600,470,black)
		drawText(getTextbox(),BASICFONT,display_surface,160,335,red)

		drawText('Username:',BASICFONT,display_surface,160,125,black)
		drawText('DOB (DD/MM/YYYY):',BASICFONT,display_surface,50,195,black)
		for button in buttons:
			button.draw(display_surface)
		for box in inputBoxes:
			box.draw(display_surface)

		pygame.display.update()
		clock.tick(fps)


# instantiate widgets
# BT = button, IB = input (text) box
# BTLogin = Button("Login", (700, 150), login, bg=(100,200,200))
# BTCreateAcc = Button("Create Account", (700, 250), displayCreateAcc, bg=(100,200,200))
# BTUnlockAcc = Button("Unlock Account", (700, 350), displayUnlockAcc, bg=(100,200,200))
# BTBack = Button("Back", (700, 150), None, bg=(100,200,200))
# IBUsername = InputBox(320, 125, 200, 40)
# IBPassword = InputBox(320, 195, 200, 40)
# IBDob = InputBox(320, 265, 200, 40)

def displayLogin(display_surface):
	# define widgets used in this function
	# instantiate widgets
	# BT = button, IB = input (text) box
	BTLogin = Button("Login", (700, 150), login, bg=(100,200,200))
	BTCreateAcc = Button("Create Account", (700, 250), None, bg=(100,200,200))
	BTUnlockAcc = Button("Unlock Account", (700, 350), None, bg=(100,200,200))
	IBUsername = InputBox(320, 125, 200, 40)
	IBPassword = InputBox(320, 195, 200, 40)

	# define widgets used in this function
	buttons = [BTLogin,BTCreateAcc,BTUnlockAcc]
	inputBoxes = [IBUsername,IBPassword]
	setTextbox('Welcome to BattleshipPlus!')

	tries = 0

	while True:
		mouse_pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				success = BTLogin.mousebuttondown(mouse_pos,usr=IBUsername.text,pwd=IBPassword.text,tries=tries)
				if(success == 0):
					setTextbox('Your account is locked!')
				elif(success == 1):
					return 'startGame'
				elif(success == 2):
					tries+=1
					setTextbox('Password wrong!')
				elif(success == -1):
					setTextbox('User does not exist!')
				else:
					pass
				if(BTCreateAcc.isPressed(mouse_pos)):
					print('createAcc')
					return 'createAcc'
				if(BTUnlockAcc.isPressed(mouse_pos)):
					print('unlockAcc')
					return 'unlockAcc'

			for box in inputBoxes:
				box.handle_event(event)

			# update screen display
			#draw background
			display_surface.fill(white)
			display_surface.blit(login_welcomeIMG,(0,0))
			drawText('\xa9 CZ1003 FS1 NG-19_POH-20_SUTANTYO-21',textFont,display_surface,600,470,black)
			drawText(getTextbox(),BASICFONT,display_surface,160,335,red)

			drawText('Username:',BASICFONT,display_surface,160,125,black)
			drawText('Password:',BASICFONT,display_surface,160,195,black)
			for button in buttons:
				button.draw(display_surface)
			for box in inputBoxes:
				box.draw(display_surface)
			pygame.display.update()
			clock.tick(fps)

#############################

def loginLoop(display_surface):
	screen = 'login'
	pygame.mixer.music.load("./audio/menu.mp3")
	pygame.mixer.music.play(-1,0.0)

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

phase = 'login'

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
	if(phase=='quit'):
		break

pygame.quit()
