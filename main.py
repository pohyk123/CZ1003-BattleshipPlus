import pygame
import random
from map import Map
from utils import setTextbox, getTextbox
import time
import copy
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
pygame.display.set_caption('CZ1003-Batlleship')

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

carrierIMG = pygame.image.load('./img/carrier.png').convert_alpha()
battleshipIMG = pygame.image.load('./img/battleship.png').convert_alpha()
cruiserIMG = pygame.image.load('./img/cruiser.png').convert_alpha()
submarineIMG = pygame.image.load('./img/submarine.png').convert_alpha()
destroyerIMG = pygame.image.load('./img/destroyer.png').convert_alpha()

hitIMG = pygame.image.load('./img/hit_marker.png').convert_alpha()
missIMG = pygame.image.load('./img/miss_marker.png').convert_alpha()

images = {
		 'bckgrnd_waterIMG':bckgrnd_waterIMG,
		 'carrierIMG':carrierIMG,
		 'battleshipIMG':battleshipIMG,
		 'cruiserIMG':cruiserIMG,
		 'submarineIMG':submarineIMG,
 		 'destroyerIMG':destroyerIMG,
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

#========================================================================

def AI_prepfield():
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

	rot = ['H','V']

	# keep adding ships until 4 valid ships are added
	while(len(m_sea.ships) < 4 or len(m_sub.ships) < 4):
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
	setTextbox('Please place 4 ships in left map! (Above water)')

	while True:
		#Switch phase when all ships are placed
		if len(m_sea.ships) == 4 and len(m_sub.ships) == 0:
			subPhase = 'subsea'
			setTextbox('Please place 4 ships in either map!')
		#Move to next phase when all ships are placed
		if (len(m_sea.ships) + len(m_sub.ships) == 8):
			setTextbox('All ships have been placed!')
			break
		# check for user input
		for event in pygame.event.get():
			#Get mouse position
			mouse_x, mouse_y = pygame.mouse.get_pos()
			#check if user wants to quit
			if 	event.type == pygame.QUIT:
				conn.close()
				pygame.quit()
				quit()
			if event.type ==  pygame.MOUSEBUTTONDOWN:
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

	time.sleep(1)
	# m_sea_enemy,m_sub_enemy = AI_prepfield()
	m_sea_enemy,m_sub_enemy = AI_prepfield()

	return 'battle', (m_sea,m_sub), (m_sea_enemy,m_sub_enemy)

	# placing_ships = True
    #
	# #string to hold current selected ship during prep phase
	# curr_ship = None
	# num_ships_placed = 0
    #
	# #upper left and upper right corner of ready button
	# ready_but_min = (210,455)
	# ready_but_max = (290,495)
    #
	# #varibale to hold the final player field layout
	# final_player_field = None
    #
	# #position variables when drawing
	# pos_x = 0
	# pos_y = 0
    #
	# #flag to check if there is a placement conflict
	# #rectangle to check when user clicks the reayd button
	# collision = False
	# ready_but_rect = None
    #
	# #pre-render button and notification texts
	# ready_text_surface = pygame.font.Font('freesansbold.ttf',15).render('Ready Up!', False, black)
	# enemy_prep_msg = pygame.font.Font('freesansbold.ttf',30).render('Enemy Preparing...', False, red)
    #
	# #main loop for the prep phase
	# while placing_ships:
	# 	# check for user input
	# 	for event in pygame.event.get():
	# 		#check if user wants to quit
	# 		if event.type == pygame.QUIT:
	# 			conn.close()
	# 			pygame.quit()
	# 			quit()
	# 		#check if user clicks a mouse button
	# 		elif event.type == pygame.MOUSEBUTTONDOWN:
	# 			#record mouse position
	# 			pos_x, pos_y = event.pos
	# 			#if user right clicks, rotate selected ship
	# 			if event.button == 3:
	# 				if curr_ship is not None:
	# 					curr_ship.rotate_ship(display_surface)
	# 			#if user left clicks
	# 			elif event.button == 1:
	# 				#check if user is ready and clicks ready button
	# 				#if so, set final field and return that field, ending prep phase
	# 				if ready_but_rect is not None:
	# 					if ready_but_rect.collidepoint(pos_x,pos_y):
	# 						final_player_field = set_final_field(ship_list)
	# 						placing_ships = False
	# 						return final_player_field
	# 					ready_but_rect = None
	# 				#select a ship for placement, otherwise place down current ship
	# 				if curr_ship is None:
	# 					curr_ship = chosen_ship(pos_x,pos_y,ship_list)
	# 				else:
	# 					error = curr_ship.place_ship(pos_x,pos_y,ship_list)
	# 					#if successful placement, prepare for next ship selection
	# 					if error != -1:
	# 						curr_ship.placed = True
	# 						curr_ship = None
	# 		#if mouse motion detected, record position and check for placement collision
	# 		elif event.type == pygame.MOUSEMOTION:
	# 			pos_x, pos_y = event.pos
	# 			collision = check_collision(curr_ship,pos_x,pos_y,ship_list)

    	# #draw the game board
    	# draw_board(display_surface)
        #
    	# # #draw notification on enemy board to show that enemy is preparing
    	# # enemy_prep_surface = pygame.draw.rect(display_surface,white,(500+60,50+(40*3),280,40))
    	# # gameDisplay.blit(enemy_prep_msg,(enemy_prep_surface.x+5,enemy_prep_surface.y+5))
        # #
    	# # #illuminate tiles to show valid placement locations and then draw the ships
    	# # if curr_ship is not None:
    	# # 	illuminate_tiles(gameDisplay,curr_ship,pos_x,pos_y,collision)
    	# # draw_setup_ships(display_surface,pos_x,pos_y,curr_ship,ship_list,True)
        # #
    	# # #check if all ships are placed down, if so display the ready button
    	# # if all_ships_placed(ship_list):
    	# # 	if ready_but_min[0] < pos_x < ready_but_max[0] and ready_but_min[1] < pos_y < ready_but_max[1]:
    	# # 		ready_but_rect = draw_finish_prep_button(gameDisplay,ready_but_active_color,ready_text_surface)
    	# # 	else:
    	# # 		ready_but_rect = draw_finish_prep_button(gameDisplay,ready_but_color,ready_text_surface)
        #
    	# pygame.display.update()
    	# clock.tick(fps)

def endgameLoop(display_surface,winner):
	setTextbox('And the winner is... {}!'.format(winner))
	updateTextbox(display_surface)
	pygame.display.update()
	while True:
		clock.tick(fps)
		time.sleep(1)


def battleLoop(display_surface,finalBoardLayout_human, finalBoardLayout_AI):
	# unbundle maps
	m_sea,m_sub = finalBoardLayout_human
	m_sea_enemy,m_sub_enemy = finalBoardLayout_AI
	phase = 'player' #player or cpu
	winner = ''
	turnover = 0
	enemy_turnover = 0

	setTextbox('Start of Battle Phase - get prepared!')
	time.sleep(1)

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
			pygame.display.update()
			while(turnover == 0):
				for event in pygame.event.get():
				#Get mouse position
					mouse_x, mouse_y = pygame.mouse.get_pos()
					#check if user wants to quit
					if 	event.type == pygame.QUIT:
						conn.close()
						pygame.quit()
						quit()
					if event.type ==  pygame.MOUSEBUTTONDOWN:
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
			time.sleep(2)
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

			time.sleep(2)

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
			time.sleep(2)
			if(len(m_sea.getAliveShips())==0 and len(m_sub.getAliveShips())==0):
				winner = 'enemy'
				break
			phase = 'player'

		# m_sea.drawMap(display_surface)
		# m_sea.drawShips(display_surface)
		# m_sub.drawMap(display_surface)
		# m_sub.drawShips(display_surface)

		clock.tick(fps)

	print('Game has ended!')
	if(winner=='player'):
		setTextbox('You win!')
	else:
		setTextbox('You lose! Try again next time.')

	updateTextbox(display_surface)
	pygame.display.update()

	return 'endgame',winner

phase = 'fieldprep'

# main loop that transitions between 5 different game phases
while(True):
    if(phase=='login'):
        pass
    if(phase=='fieldprep'):
        phase, finalBoardLayout_human, finalBoardLayout_AI = fieldprepLoop(gameDisplay)
    if(phase=='battle'):
        phase, battleResult = battleLoop(gameDisplay,finalBoardLayout_human, finalBoardLayout_AI)
    if(phase=='endgame'):
        phase = endgameLoop(gameDisplay,battleResult)
    if(phase=='quit'):
        break

pygame.quit()
