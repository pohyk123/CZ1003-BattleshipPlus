# from map import Map
from time import sleep
import pygame

from ship import Ship
import pygame

class Map:
#constructor and attribute declaration
    def __init__(self,dim,x,y,tile_size):
        self.dim = dim
        self.x = x
        self.y = y
        self.ts = tile_size
        self.coo_mapper = self.idx2coord()
        self.ships = []
        self.tries = []
        self.map = self.createEmptyMap()
        self.letters = ()
        self.nums = ()
        self.images = {}

    def createEmptyMap(self):
        mapArray = []
        for i in range(self.dim):
            mapArray.append([])
            for j in range(self.dim):
                mapArray[i].append('O')
        return mapArray

    def idx2coord(self):
        coo_map = {}
        for i in range(self.dim):
            for j in range(self.dim):
                # define top-left & bottom-right coord
                coo_map[(i,j)] = (self.x + i*self.ts, self.y + j*self.ts),(self.x + (i+1)*self.ts, self.y + (j+1)*self.ts)
        return coo_map

    def coord2idx(self,tar):
        tar_x,tar_y = tar
        tar_x = tar_x - self.x
        tar_y = tar_y - self.y
        i,j = tar_x//self.ts,tar_y//self.ts
        return i,j

    def hit(self,ij):
        i,j = ij
        if (x,y) not in self.tries:
            self.tries.append((i,j))
            for ship in self.ships:
                if(ship.hit((x,y))):
                    return True #hit
            return False #no hit

    def addShip(self,head_xy,shipType,rot,img):
        # head is in (x,y) coordinates
        head_ij = self.coord2idx(head_xy)
        newShip = Ship(len=shipType,img=img,rot=rot,head=head_ij)
        #check for valid placement (within bounds)
        for idx in newShip.body:
            if(idx[0]<0 or idx[1]<0 or idx[0]>=self.dim or idx[1]>=self.dim):
                print('Add failed! Illegal idx: {}; out of map bounds.'.format(idx))
                return False

        #check for ship collision; shipType is the length of ship
        for ship in self.ships:
            for idx in newShip.body:
                if(idx in ship.body):
                    print('Add failed! Illegal idx: {}; another ship has already been placed here.'.format(idx))
                    return False

        #if all else passes, successfully add new ship
        self.ships.append(newShip)
        print('Ship added')
        return True

    def dropShip(self,xy):
        x,y = xy
        idx = self.coord2idx((x,y))
        #match coordinate to ship
        for ship in self.ships:
            if(idx in ship.body):
                self.ships.remove(ship)
                print('Ship removed!')
                break

    def getMapState(self):
        self.map = self.createEmptyMap() #refresh map
        for i,j in self.tries: #returns set of coordinates of each prev made attempt
            self.map[i][j] = 'X'

        #successful attempts
        for ship in self.ships:
            for i,j in ship.body:
                if((i,j) in ship.damaged):
                    self.map[i][j] = 'D'
                else:
                    self.map[i][j] = 'S'

        for row in self.map:
            print(row)
        return self.map

    def getAliveShips(self):
        aliveShips = []
        for ship in self.ships:
            if(ship.life>0):
                aliveShips.append(ship)
        return aliveShips

    def drawMap(self,display_surface):
        print('Drawing map...')
        #starting x and y coordinate
        x = self.x
        y = self.y

        nums = self.nums
        letters = self.letters

        #margin size and board legend x location for player board are both 50
        delta_margin = player_letter_ref_x = 50

        #board legend x location for enemy board is at 500
        enemy_letter_ref_x = 500

        #max y location for board legend
        y_max = 411

        #max x location for board legend of player and enemy board
        x_player_max = 411
        x_enemy_max = 861

        print('Drawing bg...')
        #draw background
        display_surface.fill(white)
        display_surface.blit(self.images['bckgrnd_waterIMG'],(0,0))
        display_surface.blit(self.images['battle_waterIMG'],(x,y))
        print('Done.  ')

        #draw individual tile outlies
        #410 is max y coordinate
        #410 and 860 are max x coordinates for respective boards
        #left board (player board)
        curr_num = 0
        curr_letter = 0
        while (x < x_player_max):

            print('inhere')
        	#draw number legend with slight location offsets
            display_surface.blit(nums[curr_num],(x+10,y-30))
            print('inhere2')
            curr_num += 1
            while (y < y_max):#draw tiles and only draw letter legend only once
                print('inhere3')
                pygame.draw.rect(display_surface,green,(x,y,self.ts,self.ts),1)
                print('inhere4')
                if x == player_letter_ref_x:
                    print('inhere5')
                    display_surface.blit(letters[curr_letter],(x-30,y+5))
                    print('inhere6')
                    curr_letter += 1
                y += self.ts
            x += self.ts
            y = delta_margin

        curr_num = 0
        curr_letter = 0

        #account for middle barrier of 50 pixels
        x += delta_margin

        #draw enemy side backrgound of board
        display_surface.blit(battle_waterIMG,(x,y))

        #right board(enemy/attacking board)
        while (x < x_enemy_max):
            display_surface.blit(nums[curr_num],(x+10,y-30))
            curr_num += 1
            while (y < y_max):
                pygame.draw.rect(display_surface,green,(x,y,self.ts,self.ts),1)
                if x == enemy_letter_ref_x:
                    display_surface.blit(letters[curr_letter],(x-30,y+5))
                    curr_letter += 1
                y += self.ts
            x += self.ts
            y = delta_margin

    def drawTries():
        pass


# pygame config
display_width = 950
display_height = 500

# game refresh rate
clock = pygame.time.Clock()
fps = 30

pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('CZ1003-Batlleship')

dim = 10
x=50
y=50
tile_size = 40

m = Map(dim,x,y,tile_size)

head_xy = (100,250)
shipType = 4
rot = 'H'
img = None

# m.addShip(head_xy,shipType,rot,img)
# m.getMapState()
# print(len(m.getAliveShips()))
# sleep(1)
#
# m.addShip(head_xy,shipType,rot,img)
# m.getMapState()
#
# sleep(1)
# m.dropShip((200,250))
# print(len(m.getAliveShips()))
# m.getMapState()

#various color definitions
white = (255,255,255)
dark_white = (220,220,220)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
ready_but_color = (204,204,0)
ready_but_active_color = (255,255,0)

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

#Import images
battle_waterIMG = pygame.image.load('./img/battle_water.png').convert_alpha()
bckgrnd_waterIMG = pygame.image.load('./img/dark_water.png').convert_alpha()

carrierIMG = pygame.image.load('./img/carrier.png').convert_alpha()
battleshipIMG = pygame.image.load('./img/battleship.png').convert_alpha()
cruiserIMG = pygame.image.load('./img/cruiser.png').convert_alpha()
submarineIMG = pygame.image.load('./img/submarine.png').convert_alpha()
destroyerIMG = pygame.image.load('./img/destroyer.png').convert_alpha()

images = {'battle_waterIMG':battle_waterIMG,'bckgrnd_waterIMG':bckgrnd_waterIMG,'carrierIMG':carrierIMG,'battleshipIMG':battleshipIMG,'cruiserIMG':cruiserIMG,'submarineIMG':submarineIMG,'destroyerIMG':destroyerIMG}

m.images = images
m.nums = nums
m.letters = letters
#main loop for the prep phase
while True:
    # check for user input
    for event in pygame.event.get():
        #check if user wants to quit
        if event.type == pygame.QUIT:
            conn.close()
            pygame.quit()
            quit()
    print('loop')
    m.drawMap(gameDisplay)
    print('loop2')
    pygame.display.update()
    clock.tick(fps)
